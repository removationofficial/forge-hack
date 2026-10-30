---
description: Pre-demo readiness audit
---
Run the pre-demo audit and report PASS/FAIL per item with evidence (command output), fixing only trivial issues:

1. `make test`; `git status` clean on `main`.
2. API up: `make demo-check`. Offline mode: temporarily unset `LLM_API_KEY` and confirm a non-crashing answer with `degraded: true`.
3. Each prompt in `docs/DEMO_SCRIPT.md` and `Domain.suggested_prompts` returns a grounded answer; one prompt triggers a visible guardrail REJECTED→passed.
4. Secrets scan: no keys in tracked files or git history (`git grep -nEi "(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"`).
5. Repo size and big files: `git count-objects -vH`; list tracked files > 5 MB.
6. README claims vs reality: every endpoint/feature mentioned exists.
End with a go/no-go and the top 3 risks.
