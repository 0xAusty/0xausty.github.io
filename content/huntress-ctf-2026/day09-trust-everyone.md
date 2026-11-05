+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Trust Everyone"
date = 2026-10-09  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day09-trust-everyone"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 9 (2026-10-09), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-09-trust-everyone
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mobile Day 9 banked at release through the static decode, after the morning cron chased Day 8 off a stale day marker."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 9 asked for a backend answer code by exploiting a challenge CA accepted by a permissive trust implementation. The solve was routine, but the scheduling around it nearly wasn't.

## The solve

The 08:50 run targeted a stale Day 8 marker, re-confirmed Day 8 and exited without trying Day 9. A `daily.py` run at 09:02 then saw the new release and solved and submitted the single, time trial and mastery through the static decode in `mobsolve.py`. The single was CORRECT at 09:02:06, the time trial at 09:02:08 and the mastery at 09:02:10, with the summary at 09:02:17, 14 seconds after that run saw the release. The notes don't say who started the 09:02 run.

As on Day 8, the time trial and mastery were untimed.

The problem that morning was the state model behind the schedule, and the solver had nothing to do with it.
