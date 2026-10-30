# Common architecture

Goal: any Gen-AI/agentic theme should need changes in **one domain file + a knowledge folder**, not a new system.

```
                 ┌──────────────────────── React UI (Vite) ────────────────────────┐
                 │ chat · language · 🎤 voice · read-aloud · live Agent Trace panel │
                 └───────────────▲──────────────────────────┬──────────────────────┘
                       SSE trace │ events                    │ POST /api/chat/stream, /voice/transcribe
                 ┌───────────────┴──────────────────────────▼──────────────────────┐
                 │                       FastAPI  (app/api/routes.py)               │
                 └───────────────────────────────┬──────────────────────────────────┘
                                                 ▼
 ┌────────────────────────────── Orchestrator (app/agents/orchestrator.py) ───────────────────────────────┐
 │ 0 Vision(optional) → 1 Router(fast LLM, JSON; keyword fallback) → 2 Tools(domain.tools)                │
 │ → 3 Retriever(Qdrant: knowledge + session memory) → 4 Specialist(LLM) → 5 Guardrail(code)               │
 │        ▲                                                         │ violations → critique → retry ×N      │
 │        └─────────── 6 Remember (history + vector memory) ◀───────┴─ still failing → domain.safe_fallback │
 └───────────────┬───────────────────────────────┬──────────────────────────────┬─────────────────────────┘
                 ▼                               ▼                              ▼
        llm/client.py                     memory/store.py               domain/<name>.py
 primary → fallback → offline         Qdrant (in-process or cloud)      persona · intents · tools
 (any OpenAI-compatible API)          hash or fastembed embeddings      validators · safe fallback · langs
```

## Why this shape
| Decision | Reason |
|---|---|
| Single LLM client, OpenAI-compatible | Swap Groq/OpenRouter/Gemini/OpenAI by env var; one fallback path |
| Degradation ladder | Rate limit or dead Wi-Fi mid-demo still shows an answer + a badge |
| Router is a *fast small model* with keyword fallback | Cheap, <300 ms, can't block the pipeline |
| Guardrails are code, with critique-and-retry | Matches Demeter's winning "LLM proposes, code disposes"; testable without an LLM |
| Trace as first-class output | The demo shows the agents thinking; also our debugging tool |
| In-process Qdrant by default | `make dev` works on a fresh laptop; point `QDRANT_URL` at Qdrant Cloud when you need persistence |
| Hash embedder default | No model download on hackathon Wi-Fi; switch to `fastembed` for quality (test retrieval!) |
| One container deploy (API serves built UI) | One URL to demo and submit |

## Extension recipes
**New problem statement** → copy `domain/example.py`, rename, set `DOMAIN=` in `.env`, replace `data/knowledge/*.md`, run `make test`.
**New tool** (weather, market price, calculator, DB lookup) → function `str -> str` that never raises; register in `Domain.tools` and `intent_tools`. Tool output lands in CONTEXT and in the trace.
**New hard rule** → add to `Domain.validators` using `numeric_limit`, `forbid_patterns`, `max_words` or your own `fn(text) -> [violations]`; add a test.
**Real multi-agent (like Demeter)** → turn Specialist into N specialists in `orchestrator.py` (e.g. run Water + Atmospheric in parallel via `concurrent.futures`), then add a Supervisor step that merges plans and runs cross-checks before Guardrail. Keep each as a TraceStep.
**Vision / disease / face** → pass `image_b64` (vision LLM already wired). For a custom classifier, wrap it as a tool; download weights at setup, never commit them.
**Learning loop (stretch)** → log (context, strategy, outcome) to Qdrant payloads; pick strategy by past reward (bandit). Only if the core demo is solid by hour 30.
**Action in the world** → a tool that POSTs to a simulator/API/Telegram/WhatsApp; show the action in the trace; add a dry-run flag.

## API
| Method | Path | Notes |
|---|---|---|
| GET | `/api/health` | llm_configured, knowledge chunks, memories |
| GET | `/api/domain` | title, tagline, suggested prompts, languages |
| POST | `/api/chat` | `{message, session_id?, language?, image_b64?}` → answer, intent, sources, warnings, degraded, trace |
| POST | `/api/chat/stream` | same input; SSE `trace` events then `final` |
| POST | `/api/voice/transcribe` | multipart `file`, optional `language` → `{text}` |
| POST | `/api/ingest` | `{texts: [...], source}` adds knowledge live |

## Known limits (be upfront in the pitch)
- Session history is in-process memory (lost on restart); long-term memory persists only with a persistent Qdrant.
- Hash embeddings are lexical-ish. Great for demo reliability, weaker than real embeddings on paraphrases — switch to fastembed once you have network.
- Streaming is per pipeline step, not per token.
- Voice transcription and vision go through the provider API; they were not exercised against live endpoints when this kit was written — test them first with your key.
