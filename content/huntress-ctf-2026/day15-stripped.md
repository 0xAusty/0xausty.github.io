+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Stripped"
date = 2026-10-15  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day15-stripped"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 15 (2026-10-15), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-15-assembly-and-symbol-loss
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A symbolised and a stripped build of one program needed a tagged-variant branch; 7 of 15 modes were automatic, and the fix taught that the last solve sets the rank."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python", "Claude Code"]
tags   = ["reverse-engineering", "elf", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 15 shipped two builds of one program, a symbolised ELF and a stripped one, and asked 150 fields: Days 1 to 14 plus tagged fields such as the architecture, format, machine and config for each build. The two-build tagging was routine; the ranking lesson was not.

## The solve

At release the supervisor resolved 141 of 150 fields and banked each earlier day's group. The nine tagged Day 15 fields were left unresolved, so only 7 of 15 modes were automatic at 09:00:31. The agent fixed it in the session: a tagged-variant branch in `binsolve.py` runs the generic handler once per build and maps the tag into the field name. The SHA-256 numbering follows zip order, so `_1` is the symbolised build and `_2` the stripped one. The single was CORRECT by 09:14:03, the time trial by 09:14:19 and the mastery by 09:14:47, and the day was 15 of 15 at 09:18:56.

That gap is what made the ranking click. Ties are broken by the time of the day's last CORRECT, so one 14-minute miss outweighs any amount of shaved latency.

A miss costs far more than slow solving.
