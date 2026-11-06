+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Compiler Says What"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-compiler-says-what"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-27-compiler-attribution
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Compiler and toolchain attribution across builds on Day 27 was solved by the pipeline alone, with nothing in the notes beyond timings."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["binsolve.py"]
tags   = ["reverse-engineering", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 27 asked 324 fields: Days 1 to 26 plus 12 about compiler and toolchain attribution across builds. The notes don't describe the builds or the new questions.

## The solve

The pipeline solved everything on its own. The single and the time trial each resolved 324 of 324, and the mastery resolved 3,564 of 3,564 over eleven sets, with a 15.5 second fetch and a 1.8 second solve. The single's 324 fields were resolved about 9 seconds after release, and the time trial's about 7 seconds after.

By the bench timings the three modes were CORRECT 11.3, 19.8 and 42.3 seconds after release, so all were confirmed by 09:00:43. The status note for the morning says all five deterministic lanes had solved themselves by then.

It was routine, and beyond those timings the notes have nothing on this day.
