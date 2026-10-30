"""Orchestrator: the whole 'agentic' pipeline in one readable file.

    guard_in -> route -> tools -> retrieve -> specialist -> validate (self-correct x N) -> remember

Every step appends a TraceStep. The UI renders the trace live (the demo 'wow').
`stream()` yields events as they happen; `run()` just collects them.
Nothing here raises to the caller: every failure degrades to something shown.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterator

from app.core.config import get_settings
from app.domain import Domain, Intent, load_domain
from app.guardrails.validators import run_all
from app.llm.client import LLMClient, get_llm
from app.memory.store import KNOWLEDGE, MEMORY, VectorStore, get_store

ROUTER_PROMPT = (Path(__file__).parent.parent / "llm" / "prompts" / "router.md").read_text(encoding="utf-8")
LANG_NAMES = {"en": "English", "hi": "Hindi", "mr": "Marathi", "ta": "Tamil", "te": "Telugu", "bn": "Bengali", "gu": "Gujarati", "pa": "Punjabi", "kn": "Kannada", "ml": "Malayalam"}


@dataclass
class TraceStep:
    agent: str
    action: str
    detail: str = ""
    ms: int = 0
    ok: bool = True


@dataclass
class ChatResult:
    answer: str
    intent: str
    language: str
    sources: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    degraded: bool = False
    trace: list[TraceStep] = field(default_factory=list)

    def dict(self) -> dict:
        return asdict(self)


class Orchestrator:
    def __init__(self, domain: Domain | None = None, llm: LLMClient | None = None, store: VectorStore | None = None):
        self.domain = domain or load_domain()
        self.llm = llm or get_llm()
        self.store = store or get_store()
        self.s = get_settings()
        self.history: dict[str, deque] = defaultdict(lambda: deque(maxlen=self.s.history_turns * 2))

    # ------------------------------------------------------------------ API
    def run(self, text: str, session_id: str = "default", language: str | None = None, image_b64: str | None = None) -> ChatResult:
        final = None
        for ev in self.stream(text, session_id, language, image_b64):
            if ev["type"] == "final":
                final = ev["result"]
        assert final is not None
        return final

    def stream(self, text: str, session_id: str = "default", language: str | None = None, image_b64: str | None = None) -> Iterator[dict]:
        trace: list[TraceStep] = []

        def step(agent, action, detail="", t0=None, ok=True) -> dict:
            st = TraceStep(agent, action, detail[:300], int((time.time() - t0) * 1000) if t0 else 0, ok)
            trace.append(st)
            return {"type": "trace", "step": asdict(st)}

        degraded = False
        text = (text or "").strip()[:2000]
        if not text and not image_b64:
            res = ChatResult("Please type or speak your question.", "general", language or "en", trace=trace)
            yield {"type": "final", "result": res}
            return

        # 1) Vision (optional) --------------------------------------------------
        if image_b64:
            t0 = time.time()
            v = self.llm.vision(image_b64, "Describe what is visible, focusing on anything abnormal. Be factual and brief.")
            if v.text:
                text = f"{text}\n[Image analysis: {v.text}]".strip()
            degraded |= v.degraded
            yield step("Vision", "analyze image", v.text or v.error, t0, ok=bool(v.text))

        # 2) Route ---------------------------------------------------------------
        t0 = time.time()
        intent, lang, why, r_deg = self._route(text, language)
        degraded |= r_deg
        yield step("Router", f"intent={intent.name}", f"lang={lang}; {why}", t0)

        # 3) Tools ---------------------------------------------------------------
        tool_ctx = []
        for name in self.domain.intent_tools.get(intent.name, []):
            t0 = time.time()
            try:
                out = self.domain.tools[name](text)
                tool_ctx.append(f"{name.upper()}: {out}")
                yield step("Tool", name, out, t0)
            except Exception as e:  # tools never take the pipeline down
                yield step("Tool", name, f"failed: {e}", t0, ok=False)

        # 4) Retrieve (RAG + long-term memory) ----------------------------------
        t0 = time.time()
        try:
            kb = self.store.search(KNOWLEDGE, text)
            mem = self.store.search(MEMORY, text, k=2, session_id=session_id)
        except Exception as e:
            kb, mem = [], []
            yield step("Retriever", "search", f"failed: {e}", t0, ok=False)
        else:
            yield step("Retriever", f"{len(kb)} facts, {len(mem)} memories", ", ".join(sorted({h.source for h in kb})), t0)
        sources = sorted({h.source for h in kb})
        context = "\n---\n".join([h.text for h in kb] + tool_ctx) or "(no relevant context found)"
        memory_ctx = "\n".join(h.text for h in mem)

        # 5) Specialist + validation loop ---------------------------------------
        messages = self._build_messages(intent, lang, context, memory_ctx, session_id, text)
        answer, warnings = "", []
        for attempt in range(self.s.max_self_corrections + 1):
            t0 = time.time()
            res = self.llm.chat(messages, offline=self._offline_answer(kb))
            degraded |= res.degraded
            answer = res.text
            yield step("Specialist", f"draft #{attempt + 1}", f"{res.provider}:{res.model or '-'}", t0, ok=res.provider != "offline")
            if res.provider == "offline":
                break  # nothing to critique; offline text is already safe
            t0 = time.time()
            violations = run_all(self.domain.validators, answer)
            if not violations:
                yield step("Guardrail", "passed", "", t0)
                warnings = []
                break
            warnings = violations
            yield step("Guardrail", "REJECTED", "; ".join(violations), t0, ok=False)
            messages = messages + [
                {"role": "assistant", "content": answer},
                {"role": "user", "content": "Your answer violated these rules:\n- " + "\n- ".join(violations) + "\nRewrite it fixing every violation. Keep the same language."},
            ]
        else:
            answer = self.domain.safe_fallback
            yield step("Guardrail", "fallback", "violations persisted; returned safe answer", None, ok=False)

        # 6) Remember ------------------------------------------------------------
        self.history[session_id].extend([{"role": "user", "content": text}, {"role": "assistant", "content": answer}])
        try:
            self.store.remember(session_id, f"User asked: {text[:200]}")
        except Exception:
            pass

        yield {"type": "final", "result": ChatResult(answer, intent.name, lang, sources, warnings, degraded, trace)}

    # -------------------------------------------------------------- internals
    def _route(self, text: str, language: str | None) -> tuple[Intent, str, str, bool]:
        intents = {i.name: i for i in self.domain.intents}
        listing = "\n".join(f"- {i.name}: {i.description}" for i in self.domain.intents)
        data, res = self.llm.chat_json(
            [{"role": "system", "content": ROUTER_PROMPT.replace("{intents}", listing)}, {"role": "user", "content": text}],
            fast=True, temperature=0, max_tokens=80, offline="",
        )
        if data and data.get("intent") in intents:
            lang = language or data.get("language") or "en"
            return intents[data["intent"]], lang, str(data.get("reason", "")), res.degraded
        # keyword fallback: never block on the router
        low = text.lower()
        best, score = self.domain.intents[-1], 0
        for i in self.domain.intents:
            sc = sum(1 for k in i.keywords if k in low)
            if sc > score:
                best, score = i, sc
        return best, language or "en", "keyword fallback", True

    def _build_messages(self, intent: Intent, lang: str, context: str, memory_ctx: str, session_id: str, text: str) -> list[dict]:
        lang_name = LANG_NAMES.get(lang, lang)
        system = (
            f"{self.domain.persona}\n\nTask guidance: {intent.instructions}\n"
            f"Reply in {lang_name}. Plain text only, no markdown symbols (the reply may be read aloud).\n\n"
            f"CONTEXT:\n{context}\n" + (f"\nWHAT YOU REMEMBER ABOUT THIS USER:\n{memory_ctx}\n" if memory_ctx else "")
        )
        return [{"role": "system", "content": system}, *list(self.history[session_id]), {"role": "user", "content": text}]

    @staticmethod
    def _offline_answer(kb) -> str:
        if kb:  # even with no LLM, show the best retrieved fact -- a demo that degrades, not dies
            return "(offline mode) Most relevant information I have:\n" + kb[0].text[:400]
        return "I'm offline right now and have no stored information on that. Please try again shortly."


_orch: Orchestrator | None = None


def get_orchestrator() -> Orchestrator:
    global _orch
    if _orch is None:
        _orch = Orchestrator()
    return _orch
