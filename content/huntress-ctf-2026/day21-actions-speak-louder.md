+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Actions Speak Louder"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-actions-speak-louder"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-21-github-actions-persistence
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine GitHub Actions persistence morning: the 09:00 cron banked a 1,373-field single and both timed modes without any change to the solver."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = []
tags   = ["malware-analysis", "github-actions", "mastery", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

The Day 21 bundle added GitHub Actions workflow polyglots. The single asked 1,373 fields about triggers, trust boundaries and the job that keeps coming back, and the Time Trial repeated that count. It was routine, because the script solver already covered the shape.

## The solve

Nobody touched it. The 09:00 cron ran the pipeline, which read the new bundle, derived the answers with the existing script modules and submitted them. The single was confirmed at 09:00:06, the Time Trial at 09:00:09 and the mastery at 09:00:13, with the supervisor's summary at 09:00:21. The mastery was five sets and 6,865 fields, and it went in the same way.

No change to the solver is recorded for the day. The hand-off note for the morning says only that the script and mobile lanes banked three of three automatically.

Once the solver covers a shape, the day itself costs nothing; the work was done on earlier days.
