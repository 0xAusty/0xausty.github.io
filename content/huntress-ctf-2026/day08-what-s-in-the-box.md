+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "What’s in the Box?"
date = 2026-10-08  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day08-what-s-in-the-box"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 8 (2026-10-08), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-08-whats-in-the-box
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 8 turned the metadata lane cumulative: every earlier day's question returned in one bundle, and one field's declared order later turned out to be graded alphabetically."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "metaengine.py", "python"]
tags   = ["forensics", "metadata", "zip"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

This was the lane's first cumulative inventory. Single and time trial asked 12 fields about one bundle, repeating the earlier days' questions (identity hashes, a byte prefix, image sizes, the PDF version, the ZIP entry count) and adding the central-directory member names as a JSON array. The mastery asked the same 12 for five sets.

## The solve

The 8 October cron did not fire because the laptop was asleep, so the day was solved in a Claude Code session. The agent extended `mfsolve.py` with member size and the three hashes, parsed the member names from the `PK 01 02` central-directory records, and added a filename handler that takes the first matching member's basename. The untimed mastery was solved in full and submitted once.

The notes do not record the solve times; the supervisor's run on 9 October only found all three modes already CORRECT.

The gotcha came later. The field is declared as an array with exact values and order, and Day 8 accepted central-directory order. On Day 23 and Day 24 the grader accepted only the alphabetical listing, and the parser now emits that.
