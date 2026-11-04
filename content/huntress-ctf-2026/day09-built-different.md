+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Built Different"
date = 2026-10-09  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day09-built-different"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 9 (2026-10-09), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-09-built-different
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "One new PE header word on top of the Day 8 inventory, and the reminder that the declared field type, not a lane-wide habit, decides the hex spelling."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["forensics", "metadata", "pe"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

A reuse day. The bundle held executables for several architectures, plus decoys wearing executable extensions, next to the Day 8 inventory. The only new field was the COFF machine type of one executable; the single and time trial asked 13 fields and the mastery 65 across five sets.

## The solve

The release sweep fetched all 13 ids but left the single unsolved, and the other modes were not attempted. Claude Code solved it in session by the 09:25 commit that reports Day 9 complete (15 of 15). The new handler reads `e_lfanew` at offset 0x3c, then the 16-bit machine value at the PE signature plus 4. Everything else came from the Day 8 toolkit. The notes do not record per-mode times.

The next day the agent turned PE header reads into a table in `mfsolve.py`, taking the hex width from the field name's suffix, so later header questions needed no new code.

The `_u16_hex` field wanted a `0x` prefix and four digits, unlike the Day 2 prefix field, which is lowercase hex with no prefix. The field's declared type sets the spelling.
