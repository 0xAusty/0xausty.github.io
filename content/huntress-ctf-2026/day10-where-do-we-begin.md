+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Where Do We Begin?"
date = 2026-10-10  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day10-where-do-we-begin"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 10 (2026-10-10), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-10-where-do-we-begin
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "On the first parallel-subagent release, the entry-point RVA from the PE optional header had to be padded to the declared width; the grader rejected the minimal hex form."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["forensics", "metadata", "pe", "time-trial", "mastery"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Each mode asked for the PE entry-point RVA as a hex pattern field, for one executable in the single, another in the time trial, and two in the mastery. The technique is small, and the day is more notable for how it was run.

## The solve

The release sweep left the day unsolved. It was the first real run of the "Auto, all lanes" routine: one Claude Code subagent per open lane, four in parallel, about 10 minutes of wall-clock. The metadata subagent finished all modes CORRECT, and its handler commit is stamped 09:08. The scoreboard puts the single at 09:05:52, the time trial at 09:07:17 and the mastery at 09:08:17.

The handler reads the little-endian 32-bit AddressOfEntryPoint at `e_lfanew` + 40 in `mfsolve.py`. That afternoon the agent generalised the PE header reads into a table of spec offsets, so new header questions resolve without new code.

Masteries were timed again from this day, after two untimed days.

The first spelling tried, the minimal hex form, was rejected. The grader encodes to the field's declared width, so the accepted form was `0x` plus eight zero-padded digits.
