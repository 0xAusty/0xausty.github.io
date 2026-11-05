+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "BOM Voyage"
date = 2026-10-03  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day03-bom-voyage"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 3 (2026-10-03), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-03-bom-voyage
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A true-or-false check for a UTF-8 byte-order mark, whose one wrinkle was that the grader declares its accepted values in the start response, not the status call."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["metadata", "forensics", "encoding"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 3 asked one enum question per mode: does a named text member start with a UTF-8 byte-order mark? The files look identical in an editor and differ only at the byte level. It was routine.

## The solve

The check in `mfsolve.py` looks for the three bytes EF BB BF at the start of the member and answers true or false. From Day 3 on, each day's new metadata question took the form "Determine format.field for member", which the later metadata engine was built around.

The accepted values are the lowercase strings true and false. They appear in the `answer_format` of the start and submit response, not in the status call. The agent's memory file lists this field among the solved examples whose format was confirmed.

The scoreboard dates the single to 11:09:25 on 4 October, the day after release, and the time trial and mastery to 18:07:16 and 18:07:46 that evening. The notes say that all metadata time trials and masteries were solved in the 4 October Claude Code session, and that all three modes were correct by the 14 October corpus backfill. No per-day note names who solved the single.

Read the declared format from the start response, not from the status.
