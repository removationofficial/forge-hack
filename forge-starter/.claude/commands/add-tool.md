---
description: Add a tool (external API / calculator / lookup) to the active domain
argument-hint: <tool_name> "<what it does>" <intent_name>
---
Add tool `$1` ("$2") to the active domain and attach it to intent `$3`.

- Contract: `def $1(text: str) -> str`, must never raise, must time out ≤ 5 s, returns a short factual string for the CONTEXT block.
- Use `httpx` with a timeout; on failure return a clear "unavailable" string. Config/keys via `app/core/config.py` only.
- Register in `Domain.tools` and `Domain.intent_tools`.
- Add a test with a mocked transport (no network). Run `make test`. Show the trace step it produces.
