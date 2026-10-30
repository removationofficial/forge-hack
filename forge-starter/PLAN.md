# FORGE '26 — Our Plan

**Event:** Gen-AI Buildathon by NxtWave Launchpad · online · teams of 2–3 · 48 h
**Key dates (IST):** Registration closes 30 Oct 7:30 PM · Workshops 27 & 28 Oct · Build 30 Oct 7:30 PM → 1 Nov 11:59 PM
**Goal:** Ship a working, reliable demo of a real problem, with a clean repo a judge can run in 5 minutes.
**Our approach:** Prepare a reusable starter (`forge-starter`) now, so on hackathon day we spend time on the *problem* and the *demo*, not setup.

> What we don't know yet: the 2 themes and the judging rubric. Finding them is task #1 below.

---

## 1. What we have
| Item | What it is |
|---|---|
| `forge-starter` repo | FastAPI backend + React UI. Agent pipeline: Router → Tools → Retriever (Qdrant) → LLM → Guardrail → Memory |
| Offline mode | Runs with no API keys; falls back provider → offline answer so the demo never dies |
| `CLAUDE.md` | Working rules for Claude Code and for us |
| `WINNING.md` | What KisaanSetu, Masthishq and Demeter have in common, and mistakes to avoid |
| `docs/` | Architecture, 48-hour timeline, demo script, submission checklist |
| `.claude/commands/` | `/new-domain`, `/add-tool`, `/demo-check`, `/submit` |

Not yet verified: full `make test`, `npm run build`, live voice and vision calls (sandbox had no PyPI/npm access).

---

## 2. Roles (fill in names)
| Role | Owner | Responsibilities |
|---|---|---|
| A — Backend & agents | ______ | domain file, tools, guardrails, deployment |
| B — Frontend & demo | ______ | UI polish, voice, mobile view, demo run-through |
| C — Data, docs & pitch | ______ | knowledge files, evaluation questions, README, video, slides |

If we are 2 people, B and C merge. Everyone can run the project and give the demo.

---

## 3. Before the hackathon (now → 30 Oct 7:30 PM)

### Tonight (27 Oct early / 26 Oct)
- [ ] Register on https://tinyurl.com/FORGE-026-LP (closes 30 Oct 7:30 PM — do it now, all members)
- [ ] Join the Discord https://discord.gg/pFShT3kJgn and find the themes, rules, judging criteria, submission format
- [ ] Unzip `forge-starter`, run `make setup`, `make test`, `make dev`, `cd frontend && npm run build`
- [ ] Fix anything that fails (ask Claude with the error text)
- [ ] Push to a shared GitHub repo; all 3 teammates have access

### By 28 Oct
- [ ] Each teammate: clone, `make setup`, `make dev` works on their laptop
- [ ] Get keys: Groq (primary), OpenRouter or Gemini (fallback), Qdrant Cloud (optional). Put in `.env` only — never commit
- [ ] Test with a real key: normal answer, a voice question, an image question
- [ ] Attend workshops 27 & 28 Oct; note any tools/APIs the organisers recommend
- [ ] Read together: `CLAUDE.md`, `WINNING.md`, `docs/TIMELINE_48H.md`

### By 29 Oct
- [ ] Deploy the unchanged kit (Render / Railway / HF Spaces via `Dockerfile`) → we have a live URL
- [ ] Decide roles above; set up a group chat and a call time for kickoff
- [ ] Shortlist likely data sources (government guidelines, FAQs, datasets) for the themes once known
- [ ] Sleep schedule: who sleeps when during the 48 h

---

## 4. During the hackathon (30 Oct 7:30 PM → 1 Nov 11:59 PM)

| Hours | Do | Done when |
|---|---|---|
| 0–2 | Pick problem. Fill top of `CLAUDE.md`: user, pain, pitch, 30-second demo moment | All 3 agree in one sentence |
| 2–6 | `/new-domain`, add knowledge files, set `DOMAIN=`, `make test`, deploy | Real question on the live URL gets a grounded answer + trace |
| 6–16 | Build the one feature that makes us different (vision, extra agents, action, multilingual voice) | Demo moment works end to end, even if ugly |
| 16–24 | Guardrails, error handling, first full demo rehearsal. Cut scope if behind | Network off → still answers |
| 24–32 | UX polish for the real user. Second feature only if core is solid | A stranger can use it without help |
| 32–40 | 15–20 test questions, fix worst failures, record latency | Results table we can show |
| 40 | **Feature freeze** | No new features after this |
| 40–44 | Bug-bash, README, architecture diagram, screenshots | Fresh clone runs |
| 44–47 | Record demo video (2–3 min), write one-page pitch | Video done in one good take |
| 47–48 | Submit (aim 1 hour before deadline) | Confirmation saved |

---

## 5. Rules we follow
1. Demo must never crash: every external call has a fallback.
2. Safety rules in code (guardrails), not only in prompts.
3. Answers come from our knowledge/tools; if unsure, say so.
4. No secrets in git. No big files (>5 MB) in git.
5. README says only what actually exists and works.
6. Small commits, branches, `main` always runs, tests before push.
7. Stop adding features at hour 40.

---

## 6. Risks and how we handle them
| Risk | Plan |
|---|---|
| LLM rate limit / API down | Fallback provider, offline mode, recorded video |
| Venue/home Wi-Fi fails | Phone hotspot; deployed URL + local copy |
| Scope creep | Cut list written at hours 24 and 40 |
| Teammate unavailable | Everyone can run and present the demo |
| Wrong problem chosen | Decide by hour 2; no switching after hour 6 |
| Hallucination in front of judges | Grounded answers + guardrails + prepared safe prompts |

---

## 7. Open questions (answer on Discord)
- [ ] What are the 2 themes?
- [ ] What is the judging rubric and weighting?
- [ ] Submission format (repo link, demo video, deck, live URL)?
- [ ] Are specific tools/APIs required or rewarded?
- [ ] Is a deployed link required, or is a video enough?

---

## 8. Final submission checklist
See `docs/SUBMISSION_CHECKLIST.md`. Minimum: working live URL, clean public repo, README with screenshot, 2–3 min video, pitch one-pager, submitted early.
