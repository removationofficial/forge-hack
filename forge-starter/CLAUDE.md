# CLAUDE.md — FORGE '26 Gen-AI Buildathon (48h, team of 2–3)

You are pair-programming in a **48-hour hackathon repo**. Judges see a demo and a repo, not our effort.
Optimise for: **(1) a live demo that never dies, (2) a real problem with a clear user, (3) a repo a stranger can run in 5 minutes.**
Speed matters, but a broken demo loses to a simple working one. When in doubt: ship the smaller thing that works.

## Fill this in at kickoff (first 30 min) — keep it current
- **Problem / theme:** _TODO_
- **User (one specific person):** _TODO e.g. "Sunita, 45, small-holder farmer in Nashik, speaks Marathi, low literacy"_
- **One-sentence pitch:** _TODO_
- **The one demo moment (≤ 30 s) that must work:** _TODO_
- **Team / owners:** _TODO (backend+agents · frontend+demo · data+docs/pitch)_

## Commands
```bash
make setup      # venv + pip + npm install, copies .env.example -> .env
make dev        # API :8000 (reload) + UI :5173 (proxies /api)
make test       # backend pytest — must be green before every push
make seed       # (re)load backend/data/knowledge into the vector DB
make build      # build UI -> served by the API from one container
make demo-check # hits /api/health + one chat; prints PASS/FAIL (run before presenting)
```
Runs with **no API keys** (offline mode: retrieval-only answers). Add `LLM_API_KEY` in `.env` for real answers.

## Architecture (details: docs/ARCHITECTURE.md)
```
React UI ──SSE──▶ FastAPI /api/chat/stream ──▶ Orchestrator
                                   Router → Tools → Retriever(Qdrant RAG + memory)
                                   → Specialist(LLM) → Guardrail(code) ⟲ self-correct → Remember
```
- `backend/app/domain/<name>.py` — **the problem-specific file**: persona, intents, tools, hard-limit validators, safe fallback, prompts, languages. *Most of our work happens here + `data/knowledge/`.*
- `backend/app/agents/orchestrator.py` — pipeline. Generic. Change only to add a step.
- `backend/app/llm/client.py` — the ONLY place that talks to an LLM (OpenAI-compatible; primary → fallback → offline).
- `backend/app/memory/store.py` — the ONLY place that talks to Qdrant.
- `backend/app/guardrails/validators.py` — deterministic safety rules.
- `frontend/src/api.js` — the ONLY place the UI calls the network.

## Rules (non-negotiable)
1. **Never crash the demo.** Every external call (LLM, tool, DB, network) is wrapped; failure degrades visibly (offline answer, `degraded` badge) — it never raises to the user. New tools must follow `domain.tools` contract: `str -> str`, never raise.
2. **LLM proposes, code disposes.** Safety/legal/medical/numeric limits go in `guardrails/validators.py`, not just in the prompt.
3. **Ground answers.** Facts and numbers come from `CONTEXT` (RAG/tools). If context is empty the agent says it's unsure. No invented schemes, prices, dosages, names.
4. **Secrets:** only in `.env` (git-ignored). Read config ONLY via `app/core/config.py`. Never print/log keys (not even prefixes). Never commit `.env`, keys, or tokens. `.env.example` has placeholders only.
5. **No big binaries in git** (>5 MB: model weights, datasets, videos). Download at setup via a script, or use Git LFS / a release asset / HF hub. Keep the repo small and clonable in seconds.
6. **One backend, one frontend.** Do not add a second framework/language "just for this feature". No dead code, no `debug_*.py`, no stray folders — delete before commit.
7. **README must match reality.** Only document endpoints/features that exist and were run. Every claimed number (accuracy, latency) needs a way to reproduce it or gets removed.
8. **Tests:** every new validator, tool and route gets a test in `backend/tests/` using the fake-LLM pattern in `test_pipeline.py` (no network, no keys). Run `make test` before each push.
9. **Small commits, feature branches, one PR per feature**, merged by a teammate. Conventional messages (`feat:`, `fix:`, `docs:`). `main` always runs.
10. **Indic/multilingual by default** when the user is Indian: reply in the user's language, plain text (no markdown symbols — output may be read aloud), short sentences.

## Conventions
- Python 3.10+, type hints, `pydantic` models at API boundaries, `logging` not `print`. Format with `ruff format` if installed.
- Prompts live in `backend/app/llm/prompts/*.md` or in the domain file — not scattered in code.
- React: function components, state local, styles in `styles.css`. No UI library unless it saves >1h.
- Every pipeline step must add a `TraceStep` — the UI shows it live; it is our demo's "wow".
- Keep functions small; comment *why*, not *what*.

## Workflow for you (Claude)
- Before big changes: read `docs/ARCHITECTURE.md` and the file you're editing; propose the smallest change that works.
- After any change: run `make test`; for UI changes, say what to click to verify. Don't claim something works unless you ran it.
- If a requested change conflicts with a Rule above, say so and offer the compliant alternative.
- Prefer extending `domain/` over editing generic modules. Prefer deleting code over adding it.
- Time-box: if something takes >45 min, stop, report options, and cut scope. Scope cuts are decisions for humans — ask.
- Slash commands in `.claude/commands/`: `/new-domain`, `/add-tool`, `/demo-check`, `/submit`.

## Definition of Done (per feature)
- Works end-to-end in the UI **and** in offline mode (doesn't crash without keys).
- Test added/updated and green. Trace step visible. README/docs updated if user-facing.
- Committed on a branch, reviewed, merged. Demo script (`docs/DEMO_SCRIPT.md`) still works.

## Do NOT
- Add auth/payments/admin panels/settings pages unless the theme demands it.
- Train models from scratch in the 48h. Use hosted LLMs + pretrained models + RAG.
- Spend the last 6 hours on features. Last 6 hours = freeze, bug-bash, README, video, submission (docs/SUBMISSION_CHECKLIST.md).
