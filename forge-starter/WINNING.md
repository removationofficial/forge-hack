# What the three winning repos actually have in common (and what to avoid)

Read straight from the code and READMEs of **KisaanSetu** (1st prize, Agri-Tech Hackathon 2025, 24h offline, 1200+ participants per its README), **Masthishq** (dementia memory assistant) and **Demeter** (autonomous hydroponics multi-agent system). Observations below are verified in those repos; the "why they won" part is inference, because none of them publish judging notes.

> **Be honest with yourself:** no repo layout wins a hackathon. Problem choice, a demo that works live, and a clear story do. This kit removes the engineering risks so your 48 hours go into those three things.

## Pattern 1 — A specific, high-stakes human problem, not "a chatbot"
| Repo | User | Why it lands |
|---|---|---|
| KisaanSetu | Indian farmer, low literacy, 8 languages | Voice-first, Hindi-default prompt, "10+ features" in one app |
| Masthishq | Alzheimer's patient + caregiver | Emotional; "Who is this?" / "Where are my keys?" is a 20-second demo |
| Demeter | Hydroponic grower | Closed loop: sense → reason → act in a simulator, with safety rules |
**Do:** name one person, one pain, one moment. Put it in CLAUDE.md and the README's first line.

## Pattern 2 — Multimodal, not text-in/text-out
Voice (Whisper/STT/TTS), vision (face recognition, YOLOv8, CLIP, plant-disease CNN), sensors/time-series. Every winner used at least two modalities. The starter ships voice-in (Whisper via Groq), browser read-aloud, and an image path to a vision LLM.

## Pattern 3 — Fast hosted LLM + vector memory
Masthishq and Demeter use **Groq** (Llama / Qwen) + **Qdrant**; KisaanSetu uses Google generative AI. Fast inference makes agent loops feel live; Qdrant gives memory/RAG that is visibly *grounded*. Starter: OpenAI-compatible client (Groq default, any fallback), Qdrant with zero-setup in-process mode.

## Pattern 4 — Agents with roles, and a deterministic safety layer
Demeter's Supervisor merges Atmospheric + Water plans, runs `check_cross_domain_conflicts` and `validate_hard_limits` (pH, EC, humidity) in plain code, and rejects with a critique. That "LLM proposes, code disposes" loop is what makes it feel *industrial*, not a toy. Starter: `guardrails/validators.py` + self-correction in the orchestrator.

## Pattern 5 — Graceful degradation
Masthishq's `LLMService._fallback_response` answers rule-based when the LLM is down. Live demos die on rate limits and venue Wi-Fi. Starter: primary → fallback provider → offline retrieval answer, with a visible `degraded` badge.

## Pattern 6 — Persona engineering for the real user
KisaanSetu's prompt: pure simple Hindi, numbered lists instead of bullets, no asterisks (it's read aloud), 3–5 points. Masthishq's: 1–2 warm sentences, never say "database". Starter's orchestrator enforces plain text + user language and keeps persona in the domain file.

## Pattern 7 — Something that *learns* or *remembers* (optional, high-impact)
Demeter: contextual-bandit strategy selection + Mem0/Qdrant "plant biography". Masthishq: enrolled faces/objects as memory. Starter: per-session long-term memory in Qdrant; a bandit is a stretch goal, not a requirement.

## Pattern 8 — Presentation
Demeter: badges, architecture diagram, 3 screenshots, agent-role table, docs link. KisaanSetu: prize claim, team, feature list. Judges skim READMEs; both made the story scannable in 30 seconds. See `docs/SUBMISSION_CHECKLIST.md`.

---

## Anti-patterns found in those repos (don't copy)
These didn't stop them winning, but they cost credibility on closer inspection — and in an online buildathon judges *will* open the repo.

| Found | Fix in this kit |
|---|---|
| KisaanSetu repo ≈ **300 MB** (4 model files of 94–104 MB committed) | CLAUDE.md rule 5, `.gitignore` blocks `*.h5 *.keras *.pkl *.pt`; download-at-setup script |
| Masthishq prints the first 4 chars of the API key (`DEBUG LLM: Key starts with…`), has `allow_origins=["*"]` with credentials, `.env.example` has two vars on one line (broken), 20 ad-hoc `scripts/debug_*.py`, model binaries in repo root | Rule 4 (never log keys), explicit CORS list, clean `.env.example`, rule 6 (no debug files) |
| Demeter README documents `/api/farms`, a WebSocket `/ws/farm-updates` and `CONTRIBUTING.md` that **don't exist** in the code; hard-coded ngrok simulator URL in `main_agent.py`; two frontends (React + Next) and two backends (FastAPI + Node); stray `.cph/` and `runs/` folders | Rule 7 (README = reality), config only via `config.py`, rule 6 (one backend, one frontend) |
| Tests are print-scripts that need local datasets | `tests/test_pipeline.py`: real asserts, fake LLM, no network/keys |
| Placeholder `git clone your-username/...` in READMEs | Fill real URL; `make setup` is the only setup step |

## What this implies for FORGE '26 (what I don't know)
The announcement gives: 48 h build (30 Oct 7:30 PM → 1 Nov 11:59 PM IST), online, teams of 2–3, **2 themes**, rewards ₹2 lakh+, Gen-AI focus, workshops 27–28 Oct. **Judging criteria and the two themes are not in the message** — check the Discord/Launchpad page tonight and paste them into CLAUDE.md. Optimise the repo and demo for whatever rubric they publish (typically: problem relevance, technical depth, working demo, UX, scalability/impact).
