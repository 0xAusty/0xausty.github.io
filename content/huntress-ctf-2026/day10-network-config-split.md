+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Network Config Split"
date = 2026-10-10  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day10-network-config-split"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 10 (2026-10-10), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-10-network-config-split
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mobile Day 10 was banked by the cron sweep within seconds of release, and its timers returned after two untimed days."

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

Day 10 asked for a backend answer code by diffing manifest and Network Security Config variants to find the true transport exception. Routine: the APKs were slightly larger than the usual template, and the notes do not say what the extra bytes hold. The answer still came from the static puzzle decode.

## The solve

The cron sweep solved and submitted all three modes through `mobsolve.py`, each about a second after starting. All three were CORRECT by 09:00:21, the summary time, 20 seconds after the release was seen. That is an upper bound for each mode, since the log gives offsets rather than clock times.

The time trial and mastery had deadlines again after two untimed days (09:00:18 and 09:00:17), so the runner had to read the live deadline on every start. Both came back CORRECT inside them.

This was also the first release run with one subagent per open lane. Mobile needed none, because the deterministic sweep had already banked it.
