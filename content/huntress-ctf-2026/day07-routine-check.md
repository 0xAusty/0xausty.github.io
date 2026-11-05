+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Routine Check"
date = 2026-10-07  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day07-routine-check"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 7 (2026-10-07), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-07-kotlin-staging-logic
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Kotlin jar hid its config blob among thousands of stdlib classes, and the day the binary lane for Days 1 to 7 closed at 100%."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "homebase"]

tools  = ["binsolve.py", "python"]
tags   = ["reverse-engineering", "kotlin", "java"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 7 asked 56 fields: Days 1 to 6 plus eight for a Kotlin jar. The jar was about 5 MB, and the config sat base64-encoded in one class's constant pool, among more than 3,000 stdlib classes. Routine once you know where to look, and notable mostly as the day the lane closed.

## The solve

The challenge was released at 09:00:08 on 7 October and the binary lane was skipped at release. Claude Code changed `binsolve.py` to scan every class in the jar for the base64 blob rather than assuming one, which gave 55 of 56 with only the Day 1 symbol list open.

That field came from the event's Homebase AI (GPT-6 Luna), and the agent then swept every cumulative single, time trial and mastery for Days 3 to 7. The lane stood at 100% for Days 1 to 7 by the 11:43 commit. The single went CORRECT at 11:00:58, the time trial at 11:02:41 and the mastery at 11:06:57.

In the mastery, a second set shipped the config binaries as byte-patched Windows PE copies, so the solver dispatches by day prefix, not file extension.
