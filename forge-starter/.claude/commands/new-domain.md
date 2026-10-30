---
description: Create a new problem domain from the example and wire it in
argument-hint: <domain_name> "<one-line problem + user>"
---
Create a new domain `$1` for: $2

1. Read `CLAUDE.md`, `docs/ARCHITECTURE.md`, `backend/app/domain/example.py`.
2. Copy `example.py` to `backend/app/domain/$1.py`. Rewrite: title, tagline, persona (grounded, brief, plain text, user's language), 3–5 intents with keywords, tools (stubs that never raise), validators for the domain's hard safety limits, `safe_fallback`, 3 suggested prompts, languages.
3. Create 2–3 realistic knowledge files in `backend/data/knowledge/` (mark any content you could not verify as SAMPLE in the file).
4. Set `DOMAIN=$1` in `.env.example` and `.env`.
5. Add tests mirroring `backend/tests/test_pipeline.py` for the new validators and one intent route.
6. Run `make test`. Report what passed, what you couldn't verify, and 3 prompts to try in the UI.
