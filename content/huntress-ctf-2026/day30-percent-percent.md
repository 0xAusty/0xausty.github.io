+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Percent Percent"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-percent-percent"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-30
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine warmup: URL percent-encoding applied twice, reachable by chaining the solver's existing url step, banked automatically in under half a minute."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["encoding"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 30's warmup was a 972-byte blob. It was routine, and the autopilot solved it on its own.

## The solve

The single was banked at 09:00:07, the Time Trial at 09:00:09 and the Mastery at 09:00:16. The notes do not name the encoding. The prompt, about an address bar problem that "happened twice", points to URL percent-encoding applied twice, which was Day 7's encoding. The `url` step is in the first-step set of `wusolve.py`, so the per-chunk search could chain it with itself. That is an inference from the prompt and the solver, not a logged fact.

The first-pass report at 09:00:31 ran with the new 90-second wait. It listed binary, metadata, mobile and web, but not warmups.

The prompt did the work of naming the encoding, and the solver already had it.
