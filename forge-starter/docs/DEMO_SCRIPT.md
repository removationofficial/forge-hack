# Demo script (fill in; rehearse 3×; keep to 3 minutes)

**0:00–0:20 — The person.** One sentence about the user and the pain, with a real number or story. _TODO_
**0:20–0:50 — The moment.** Do the one thing that shows the product's magic. Speak in the user's language if relevant. Keep the Agent Trace panel visible. _TODO exact input:_
**0:50–1:40 — Under the hood.** Point at the trace: router → retrieval (sources shown) → guardrail rejecting something unsafe and the system correcting itself. _TODO: prepare one prompt that triggers a REJECTED → passed trace._
**1:40–2:10 — Resilience.** Disable network (or set a bad key) → answer still appears with the "degraded" badge. "It never goes dark for the user."
**2:10–2:40 — Impact & what's next.** Who benefits, how many, how it scales, what you'd add with another month. Be specific and honest about limits.
**2:40–3:00 — Ask.** Repo + live URL on screen.

## Pre-flight (10 min before)
- [ ] `make demo-check` PASS against the deployed URL
- [ ] Keys have quota (check Groq console); fallback provider key set
- [ ] Browser: mic permission granted, volume up, zoom 110–125%, notifications off
- [ ] 3 backup prompts + recorded video open in another tab
- [ ] Clear session (new tab) so history doesn't leak into the demo
