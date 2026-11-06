+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Ashes to Assets"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-ashes-to-assets"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-25-phoenix-stage-chain
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Elixir polyglots and a Phoenix-hosted stage, 1,571 fields in the single, all three modes banked at release by the new long-running supervisor, daily.py, on its first day."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["daily.py"]
tags   = ["malware-analysis", "elixir", "mastery", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 25 added Elixir polyglots and a Phoenix-hosted Elixir stage. The prompt asked for configuration to be followed from the Elixir source to an inert Phoenix stage, ending at the setting that did not survive. The single asked 1,571 fields, the Time Trial 1,625 and the mastery nine sets, 14,625. The solve itself was routine.

## The solve

Day 25 was the first day under the long-running supervisor, `daily.py`, which hot-reloads the solvers and writes progress checkpoints. From this day the catalog's confirmed source switches to those checkpoints. The notes say it banked the automatic lanes and polled across the 09:00 drop.

The single was confirmed at 09:00:06, the Time Trial at 09:00:09 and the mastery at 09:00:18, and the log shows all three correct at release. No solver change is recorded for the script lane.

The solver modules were the same ones. Only the loop running them was new.
