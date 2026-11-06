+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Pascal's Wager"
date = 2026-10-12  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day12-pascal-s-wager"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 12 (2026-10-12), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-12-pascal-archive-stager
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Pascal binary with its config as a plain constant byte array in .data; the generic handler answered the single at release and the timed modes waited two days."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["binsolve.py", "binmastery.py", "python"]
tags   = ["reverse-engineering", "elf", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 12 asked 120 fields, Days 1 to 11 plus ten for a Pascal ELF. Its raw config blob sits in `.data` as a plain constant byte array, which made it a routine day for the solver.

## The solve

The generic handler from Day 10 did it again. The single resolved all 120 fields and was CORRECT at 09:00:13, while the other lanes' submits, starts and practice calls were being rate-limited around it. The shared limiter from the day before was in place, but the 09:00 burst still drew 429s: the binary time trial's submit was one, and the mastery found no live or practice window.

Both ran in the morning catch-up session on 14 October with the solver unchanged. The time trial resolved 120 of 120 and went CORRECT at 09:20:20; the mastery resolved 360 of 360 inside a window of about 30 seconds and went CORRECT at 09:20:38.

The solver had the answers on release day. Getting a window to submit them took two more.
