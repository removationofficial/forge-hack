# FORGE '26 Starter — grounded, guard-railed, never-dies Gen-AI agent

> **TODO (replace at kickoff):** one-sentence pitch for _your user_ and _their problem_. Add screenshot/GIF and live URL here.

A reusable base for the 48-hour FORGE '26 Gen-AI Buildathon: multi-step agent pipeline, RAG + long-term memory (Qdrant), deterministic guardrails with self-correction, live agent trace UI, voice in / read-aloud out, and a three-level degradation ladder so the demo never dies.

Start here → [`CLAUDE.md`](CLAUDE.md) (working agreement) · [`WINNING.md`](WINNING.md) (what the winning repos share) · [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · [`docs/TIMELINE_48H.md`](docs/TIMELINE_48H.md)

## Run it (no API keys needed)
```bash
make setup     # venv, pip, npm, .env
make dev       # API http://localhost:8000  ·  UI http://localhost:5173
make test
```
Add `LLM_API_KEY` (free Groq key) to `.env` for real LLM answers. Without it the app answers from the knowledge base in **offline mode**.

## Make it yours (≈10 minutes)
1. `cp backend/app/domain/example.py backend/app/domain/<yours>.py` → edit persona, intents, tools, validators, languages
2. Replace `backend/data/knowledge/*.md` with your sources
3. `DOMAIN=<yours>` in `.env` → `make test` → `make dev`

## Layout
```
backend/app/{domain,agents,llm,memory,guardrails,api}   frontend/src   docs/   .claude/commands/
```

## Status of this kit
Backend orchestration logic (routing, retrieval flow, self-correction, offline fallback, tools, stream events) was verified with a stub harness; the full pytest suite and the frontend build **have not been run** — they need PyPI/npm access. Run `make setup && make test && npm run build` first thing and fix anything that surfaces. Voice transcription and vision calls are untested against live provider endpoints.

MIT License.
