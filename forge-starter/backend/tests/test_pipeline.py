"""No network, no API key: the LLM is faked with httpx.MockTransport."""
import json

import httpx
import pytest

from app.agents.orchestrator import Orchestrator
from app.core.config import Settings
from app.domain.example import DOMAIN
from app.guardrails.validators import forbid_patterns, max_words, numeric_limit, run_all
from app.llm.client import LLMClient, parse_json, strip_think
from app.memory.store import KNOWLEDGE, VectorStore


@pytest.fixture(scope="module")
def store():
    from pathlib import Path

    st = VectorStore()
    st.seed_dir(Path(__file__).parent.parent / "data" / "knowledge")
    return st


def fake_llm(answers: list[str], route="crop_advice") -> LLMClient:
    """First call = router JSON, then each call returns the next answer (last repeats)."""
    calls = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        body = json.loads(req.content)
        if body.get("response_format"):
            content = json.dumps({"intent": route, "language": "en", "reason": "test"})
        else:
            content = answers[min(calls["n"], len(answers) - 1)]
            calls["n"] += 1
        return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})

    return LLMClient(Settings(llm_api_key="k"), transport=httpx.MockTransport(handler))


# ------------------------------------------------------------- utilities
def test_parse_json_and_think():
    assert parse_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json('sure! {"a": 2} done') == {"a": 2}
    assert parse_json("nope") is None
    assert strip_think("<think>hmm</think>Hello") == "Hello"


def test_validators():
    v = [numeric_limit("dose", r"([\d.]+)\s*ml per litre", hi=5), forbid_patterns({"badword": "bad"}), max_words(5)]
    assert run_all(v, "use 3 ml per litre") == []
    assert any("above" in m for m in run_all(v, "use 20 ml per litre"))
    assert run_all(v, "badword") == ["bad"]
    assert run_all(v, "one two three four five six")


def test_retrieval(store):
    hits = store.search(KNOWLEDGE, "brown spots on tomato leaves")
    assert hits and "blight" in hits[0].text.lower()


# ---------------------------------------------------------- orchestrator
def test_offline_mode_never_raises(store):
    llm = LLMClient(Settings(llm_api_key=""))
    r = Orchestrator(DOMAIN, llm, store).run("tomato leaves have brown spots")
    assert r.degraded and r.answer.startswith("(offline mode)")
    assert r.intent == "crop_advice"  # keyword fallback routed it


def test_happy_path_with_trace(store):
    r = Orchestrator(DOMAIN, fake_llm(["Remove infected leaves and spray neem oil."]), store).run("tomato blight?")
    assert r.answer.startswith("Remove") and not r.degraded
    agents = [t.agent for t in r.trace]
    assert agents[:2] == ["Router", "Retriever"] and "Guardrail" in agents


def test_self_correction_then_pass(store):
    bad, good = "Spray 20 ml per litre of pesticide.", "Spray 3 ml per litre of neem oil."
    r = Orchestrator(DOMAIN, fake_llm([bad, good]), store).run("tomato blight?")
    assert r.answer == good
    assert [t.action for t in r.trace if t.agent == "Guardrail"] == ["REJECTED", "passed"]


def test_persistent_violation_returns_safe_fallback(store):
    r = Orchestrator(DOMAIN, fake_llm(["Spray 20 ml per litre."]), store).run("tomato blight?")
    assert r.answer == DOMAIN.safe_fallback and r.warnings


def test_tools_run_for_intent(store):
    r = Orchestrator(DOMAIN, fake_llm(["Wait for the rain to pass."], route="weather_plan"), store).run("will it rain?")
    assert any(t.agent == "Tool" and t.action == "weather" for t in r.trace)


# ------------------------------------------------------------------- API
def test_api(monkeypatch):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        h = c.get("/api/health").json()
        assert h["status"] == "ok" and h["knowledge_chunks"] > 0
        assert c.get("/api/domain").json()["suggested_prompts"]
        r = c.post("/api/chat", json={"message": "PM-KISAN eligibility?"}).json()
        assert r["answer"] and r["trace"]
        raw = c.post("/api/chat/stream", json={"message": "hi"}).text
        assert raw.count("data: ") >= 2 and '"type": "final"' in raw
