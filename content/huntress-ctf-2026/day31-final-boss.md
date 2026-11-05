+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Final Boss"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-final-boss"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-31-reversing-gauntlet
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The finale added one more config-record variant (HGAU), and the morning turned on recovery from a wedged worker, an escalator killed at its wait limit and a crashed session."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["reverse-engineering", "xor", "crc32", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 31 asked for 14 new fields built around an **HGAU** record, with the config and trace objects asked under a `gauntlet` prefix. The questions read as explicit instructions throughout. The reversing was one more variant of the HCFG record, and the trouble that day was in the infrastructure.

## The solve

The pipeline banked 423 of 434 fields at release, with closest-name guesses for some earlier machine fields. A warmups worker stuck in a deep search had blocked the supervisor from reopening work. The escalator launched five agents at 09:01:38, but all were killed at the 600-second background-wait ceiling and the coordinating session crashed.

Recovery used three fresh general-purpose subagents. The one for this binary reconnected to the open attempt instead of starting another. The fold-in added HGAU to the config-record magics and flattened nested objects into `analysis_config_*` and `analysis_gauntlet_*` fields in `binsolve.py`. The single was correct at 09:11:25, the time trial at 09:18:23 and the mastery at 09:33:08.

The mastery download took about 374 seconds, and then the submit failed twice with an SSL error. `binmastery` didn't retry a dropped submit and exited with nothing sent.

Reconnect to the open attempt rather than starting a second one.
