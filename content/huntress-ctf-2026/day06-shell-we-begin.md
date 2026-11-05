+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Shell We Begin"
date = 2026-10-06  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day06-shell-we-begin"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 6 (2026-10-06), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-06-bash-behavior-graphs
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The first 399-field challenge: submitting by language family and bisecting rejections turned the grader's remaining counter into a debugger."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["homebase", "agent"]

tools  = ["bashsolve.py", "scriptsolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["malware-analysis", "bash", "xor", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 6 added six Bash behaviour graphs and took the challenge to 399 fields. Each script asks for a role, a technique, an adapter, a campaign, a stage count, the ordered steps and an indicator. It is where the "grader as a debugger" habit began.

## The solve

`bashsolve.py` reproduces each `Recover_` function's representation and transform in Python and checks the result against the descriptor marker, never running the script. A later fallback tries every known representation and transform pair and keeps only one that yields a valid descriptor. Stage count is an explicit descriptor field, not the number of steps.

The Claude Code session submitted per language family and bisected the rejected ones, reaching 386 of 399 on 6 October. The last thirteen were generator labels for the Batch and VBScript wrappers, and the compound guesses at the Batch one were all rejected. The labels that finished the single on 7 October came from the event's Homebase AI (GPT-6 Luna), which also solved the mastery at 22:13:49 on 7 October. The time trial was correct at 15:54:23 on 7 October.

Teaching the shared decoder these codecs also lifted the still-open Day 4 and 5 singles.

Submit by family: one wrong field rejects the whole call, but the accepted fields stay banked.
