# 48-hour plan (30 Oct 7:30 PM → 1 Nov 11:59 PM IST)

Before kickoff (now → 30 Oct): do the **Prep list** below so hour 0 is spent on the problem, not setup.

## Prep (this week, ~3 h total)
- [ ] All teammates: accounts + keys — Groq, one fallback (OpenRouter/Gemini), Qdrant Cloud (free), GitHub org/repo, Render/Railway/HF Spaces
- [ ] Clone this kit; `make setup && make test && make dev` green on **every** laptop
- [ ] Deploy the untouched kit once to your host → proves the pipeline end-to-end, gives you a URL early
- [ ] Attend workshops 27–28 Oct; note which tools/APIs organisers push (judges like seeing them used)
- [ ] Read the themes + rubric the moment they're published; paste into CLAUDE.md
- [ ] Pre-collect knowledge sources (govt PDFs, datasets, guidelines) for your likely domains
- [ ] Roles: **A** backend/agents · **B** frontend/demo UX · **C** data/knowledge + pitch/README/video

## Hour-by-hour
| Hours | Goal | Exit criteria |
|---|---|---|
| 0–2 | Pick theme + problem; fill CLAUDE.md header; write the 30-s demo moment | One user, one pain, one demo moment, agreed by all |
| 2–6 | New `domain/<name>.py`, knowledge seeded, deploy skeleton live | Ask a real question on the deployed URL, grounded answer + trace |
| 6–16 | **The core wow**: the one differentiating capability (vision / agent loop / action / multilingual voice) | Demo moment works E2E, even if ugly |
| 16–24 | Guardrails, tools, error paths, offline mode check; first full demo run-through | `make test` green, kill Wi-Fi → still answers |
| 24–32 | UX polish for the user (language, voice, big touch targets), second feature **only if** core is solid | A stranger can use it without explanation |
| 32–40 | Evaluation: 15-20 test questions with expected behaviour; fix worst failures; measure latency | Table of results you can show |
| 40–44 | **Feature freeze.** Bug-bash, README + architecture diagram + screenshots | Fresh-clone test: `make setup && make dev` works |
| 44–47 | Record demo video (backup for live), pitch slides/one-pager | Video ≤ 2–3 min, 1 take that works |
| 47–48 | Submit early (buffer for upload/portal issues), tag release | Confirmation received |

## Rules of thumb
- Deployed URL by hour 6, always. Demo from the deployment *and* keep a recorded video.
- Cut scope at hour 24 and 40 — write the cut list down, don't re-litigate.
- Sleep in shifts; a rested teammate finds the bug that kills the demo.
- Commit at least hourly. If CI is red, fix before anything else.
