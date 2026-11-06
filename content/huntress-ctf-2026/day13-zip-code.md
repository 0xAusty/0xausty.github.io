+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Zip Code"
date = 2026-10-13  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day13-zip-code"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 13 (2026-10-13), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-13-archive-delivery-chain
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "All three modes solved automatically at release, each banking its confirmed fields in one submit before the capped two-try resolved the few ambiguous loop-expansion fields."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["polysolve.py", "python"]
tags   = ["malware-analysis", "zip", "obfuscation", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 13 added AppleScript polyglots and two more advanced bash fixtures. The prompt asked to trace a nested archive delivery chain and find the member that was never supposed to be delivered. The single asked 913 fields, and nothing needed fixing.

## The solve

All three modes solved automatically at release. Each one banked its confirmed fields in one submit, then the capped two-try resolved the loop-expansion fields one at a time: 4 in the single, 3 in the Time Trial and 11 in the mastery. The summary logged all three CORRECT at 09:00:44, 41 seconds after the release was seen.

No rate limit got in the way, nothing hit a dead end and no session work was needed. The pipeline just ran.

This kind of quiet day is what the earlier fixes were for.
