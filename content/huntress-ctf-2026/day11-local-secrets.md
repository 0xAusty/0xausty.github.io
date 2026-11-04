+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Local Secrets"
date = 2026-10-11  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day11-local-secrets"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 11 (2026-10-11), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-11-local-secrets
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mobile Day 11 was solved unattended within the release window while the binary lane was losing its timed modes to rate limiting."

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

Day 11 asked for a backend answer code by separating active credentials from decoys across generated local stores. Routine for mobile.

## The solve

`daily.py` solved each mode about 0.65 seconds after starting it and submitted all three CORRECT through the static decode in `mobsolve.py`. The summary time was 09:00:30, 29 seconds after the release was seen. The time trial and mastery had deadlines of 09:00:10 and 09:00:12 and came back CORRECT inside them, so the summary time overstates the lane's time. It is an upper bound only.

The same morning the parallel sweep hit its own rate limit (HTTP 429) and the binary lane lost its timed modes. Mobile banked all three regardless, while transient GET and start retries filled the log.

Nothing about the day was specific to mobile; the deterministic solver simply wasn't affected by the noise around it.
