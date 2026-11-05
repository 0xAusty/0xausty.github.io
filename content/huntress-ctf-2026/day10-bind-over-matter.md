+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Bind Over Matter"
date = 2026-10-10  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day10-bind-over-matter"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 10 (2026-10-10), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-10-wmi-persistence-reconstruction
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "WMI MOF polyglots needed no solver change; the work was finishing a mastery that the parallel sweep's own rate limiting had knocked over."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["polysolve.py", "timed.py", "python"]
tags   = ["malware-analysis", "obfuscation", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 10 added WMI MOF polyglots and two more advanced bash fixtures. The prompt framed MOF filter and consumer bindings with decoy relationships, and the single asked 753 fields. No code changed.

## The solve

The new polyglot families and hosts went through the existing `polysolve.py` and `scriptsolve` dispatch. The supervisor solved the single and the Time Trial at release, resolving the ambiguous loop-expansion fields with the capped two-try, and they were CORRECT at 09:00:09 and 09:00:14.

The mastery (two sets, 1,506 fields) failed at 9:00 with HTTP 429, because the parallel sweep was contending with itself. A per-lane Claude Code subagent finished it by running `timed.py --two-try`, which cleared 12 loop-expansion fields. It was CORRECT at 09:11:47.

Timers returned on this day, with a script window of about 31 to 32 seconds, so the live deadline had to be read on every start. The two-try wasn't automatic without its flag, and `scripttimed.py` did not un-nest the zip-of-zips masteries.

The analysis was routine for the lane. What was new was the pipeline: this was the first release where subagents took over what the sweep left.
