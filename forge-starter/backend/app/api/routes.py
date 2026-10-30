import json

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.agents.orchestrator import get_orchestrator
from app.core.config import get_settings
from app.llm.client import get_llm
from app.memory.store import KNOWLEDGE, MEMORY, get_store

router = APIRouter(prefix="/api")


class ChatIn(BaseModel):
    message: str = Field("", max_length=4000)
    session_id: str = "default"
    language: str | None = None
    image_b64: str | None = None  # optional base64 JPEG (no data: prefix)


@router.get("/health")
def health():
    s = get_settings()
    st = get_store()
    return {
        "status": "ok",
        "domain": s.domain,
        "llm_configured": bool(s.llm_api_key),
        "fallback_configured": bool(s.fallback_api_key),
        "knowledge_chunks": st.count(KNOWLEDGE),
        "memories": st.count(MEMORY),
    }


@router.get("/domain")
def domain():
    d = get_orchestrator().domain
    return {"title": d.title, "tagline": d.tagline, "suggested_prompts": d.suggested_prompts, "languages": d.languages}


@router.post("/chat")
def chat(body: ChatIn):
    return get_orchestrator().run(body.message, body.session_id, body.language, body.image_b64).dict()


@router.post("/chat/stream")
def chat_stream(body: ChatIn):
    """Server-sent events: one `trace` event per pipeline step, then one `final`."""
    orch = get_orchestrator()

    def gen():
        for ev in orch.stream(body.message, body.session_id, body.language, body.image_b64):
            if ev["type"] == "final":
                ev = {"type": "final", "result": ev["result"].dict()}
            yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.post("/voice/transcribe")
async def transcribe(file: UploadFile = File(...), language: str | None = Form(None)):
    try:
        text = get_llm().transcribe(await file.read(), file.filename or "audio.webm", language)
        return {"text": text}
    except Exception as e:
        return {"text": "", "error": f"{type(e).__name__}: {e}"}


@router.post("/ingest")
def ingest(payload: dict):
    """POST {"texts": ["...", "..."], "source": "name"} to add knowledge live (great demo moment)."""
    texts = [t for t in payload.get("texts", []) if isinstance(t, str) and t.strip()]
    n = get_store().add(KNOWLEDGE, texts, [{"source": payload.get("source", "live-upload")} for _ in texts])
    return {"added": n}
