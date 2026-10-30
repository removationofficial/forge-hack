# Submission checklist (do at hour 40+, submit before hour 47)

## Repo (judges open this)
- [ ] `git clone` → `make setup` → `make dev` works on a clean machine (test on a teammate's laptop)
- [ ] Repo < 20 MB; no `.env`, keys, weights, datasets, videos (`git count-objects -vH`; `git log -p | grep -i "api_key"`)
- [ ] No `debug_*`, scratch scripts, stray folders, commented-out blocks, `print` debugging
- [ ] README first screen: **name · one-line pitch · screenshot/GIF · live URL · demo video link**
- [ ] README sections: Problem & user · Solution · Architecture diagram · Tech stack · Run it · Env vars · Evaluation results · Limitations · Team
- [ ] README only claims what exists (every endpoint, every number reproducible)
- [ ] LICENSE (MIT), real clone URL, team names
- [ ] CI badge green; `make test` passes
- [ ] Release tag `v1.0-forge26` at submission commit

## Demo
- [ ] Deployed URL works from a phone on mobile data
- [ ] Offline-mode answer verified (unset key → still responds)
- [ ] 2–3 min video: problem → live demo → architecture → impact (captions if multilingual)
- [ ] Backup: screen recording of the full demo moment

## Story
- [ ] One-page pitch / slides: user, problem (with a number + source), solution, why Gen-AI, architecture, results, impact, roadmap
- [ ] "Why now / why us / why this is hard" answered in one sentence each
- [ ] Anticipated Q&A (hallucinations → guardrails + grounding; data privacy; cost; scale; bias; what if the API is down)
- [ ] Evaluation table (15–20 test questions: pass rate, p50/p95 latency, guardrail catches)

## Portal
- [ ] Team names/emails match registration; track/theme selected correctly
- [ ] All links open in an incognito window
- [ ] Submitted ≥ 1 hour before deadline; confirmation screenshot saved
