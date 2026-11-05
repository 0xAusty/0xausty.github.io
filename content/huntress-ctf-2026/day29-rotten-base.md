+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Rotten Base"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-rotten-base"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-29
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine warmup: Base64 combined with ROT13 was already in the solver's step set, so all three modes were banked automatically within seconds."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["encoding", "base64", "rot13"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 29's warmup was a 148-byte blob, routine and solved by the autopilot without help.

## The solve

The single was banked at 09:00:06, the Time Trial at 09:00:11 and the Mastery at 09:00:18. The notes do not name the encoding. The prompt points to Base64 combined with ROT13, and both are in the first-step set of `wusolve.py`, so the per-chunk search can chain them. That is an inference from the prompt and the solver, not a logged fact.

The day did leave one pipeline lesson. The supervisor's first-pass report at 09:00:04 listed warmups among the misses about 16 seconds before the lane banked, because it counted singles that were still running as missed. That morning the line only printed a notice. A commit on 29 October made the same line start the escalator, so before Day 30 it was fixed with a 90-second first-pass wait.

A report that counts "running" as "missed" is a bug even when the run turns out fine.
