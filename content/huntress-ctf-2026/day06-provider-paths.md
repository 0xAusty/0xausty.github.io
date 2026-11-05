+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Provider Paths"
date = 2026-10-06  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day06-provider-paths"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 6 (2026-10-06), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-06-provider-paths
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 6 was cleared unattended: the pipeline solved the mobile single, time trial and mastery within about 13 seconds of seeing the release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["python", "mobsolve.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asks you to abuse an overbroad content-provider path and correlate its records with earlier intent evidence. This is the first mobile day on record that the pipeline cleared with no person involved.

## The solve

At release the daily runner took the mobile single, then the time trial, then mastery, each through `mobsolve.py`'s static puzzle decode, and each one came back correct. The log puts every solve at about one second from its start. The release was logged at 09:00:09. The single was correct at 09:00:11, the time trial at 09:00:13 and the mastery at 09:00:19, ahead of the sweep summary at 09:00:21. The notes don't record which codec Day 6 used.

The time trial and mastery still carried server deadlines on Day 6. The log shows 09:00:18 and 09:00:24, and both were met. The timers went away on Days 8 and 9 and came back on Day 10.

It was a routine day, and the pipeline made it look like one.
