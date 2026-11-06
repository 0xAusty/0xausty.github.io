+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Crash Course"
date = 2026-10-26  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day26-crash-course"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 26 (2026-10-26), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-26-crash-triage
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Crash triage on a jar's synthetic stack trace: the agent read method names straight from the class file's constant pool, with no JDK needed."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "Claude Code", "python"]
tags   = ["reverse-engineering", "java", "crash-triage"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 26 asked 312 fields. The 12 new ones covered crash triage on a jar holding a synthetic stack trace (`crash/trace.json`) and its compiled class file. Two questions mattered: which method faulted, and whether every stack frame names a method of the primary class file.

## The solve

310 of 312 resolved at release. The misses were those two fields, and the agent fixed them in session. The faulting method is the first string in the trace's frames. For the predicate, the solver compares every frame against the method names of the primary, non-inner class, read straight from the constant pool and methods table, so no JDK is involved. It went in as `_fill_crash_from_members`.

The single was CORRECT by 09:06:55. The time trial stayed at 310 of 312 across four supervisor passes until the edited solver was hot-reloaded, then banked at 09:13:59, with the mastery following at 09:14:16, a quarter of an hour after release.

That day's retro was the backdrop. Rank had slipped from 5th to 66th on late finishes, and my correction was that the lever is solver coverage, not infrastructure.

Two unfamiliar fields held the timed modes for a quarter of an hour, on a day when late finishes had already cost rank.
