+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "By Any Other Name"
date = 2026-10-11  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day11-by-any-other-name"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 11 (2026-10-11), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-11-native-api-semantics
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "No new analysis was needed; the day's lesson was that five lane processes hitting the Game Master at once caused 429s, which cost this lane its mastery download."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["timed.py", "python"]
tags   = ["malware-analysis", "obfuscation", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 11 added TypeScript polyglots and two more advanced bash fixtures. The prompt asked to map native-API references to the behaviour they model and flag the unsupported claim. The single asked 811 fields, and nothing in the solver changed.

## The solve

The supervisor solved the single and the Time Trial at release, resolving the ambiguous loop-expansion fields with the capped two-try, and they were CORRECT at 09:00:06 and 09:00:12.

The mastery (two sets, 1,622 fields) never downloaded. Its GET failed with HTTP 429 after retries, because five lane processes had hit the Game Master at once. A Claude Code subagent banked 1,614 deterministic fields in one submit, then cleared the 8 ambiguous loop-expansion fields with the capped two-try, 6 on the first label and 2 on the second, about 10.4 seconds inside the window. It was CORRECT at 09:06:31, before the 09:27 results commit.

The same burst failed the binary lane's Time Trial outright. The fix, in a later commit, was a shared cross-process token bucket plus waiting and resending when a POST returns 429, since a 429 is rejected before processing.

The parallel sweep had rate-limited itself, and this lane only paid for it with the mastery.
