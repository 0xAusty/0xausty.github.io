+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Backup Spill"
date = 2026-10-05  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day05-backup-spill"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 5 (2026-10-05), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-05-backup-spill
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The first mobile miss on record: the release came early, the runner waited for the wrong day, and the new split-and-reorder codec returned nothing, so it declined to guess."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = []

tools  = ["python", "mobsolve.py"]
tags   = ["android", "encoding", "time-trial"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asks for application state admitted by a flawed backup boundary. Day 5 is where the puzzle encoding changed to a split: the answer comes as `parts` plus an `order` list. This was the first mobile miss on record, on the first morning the supervisor log covers.

## The solve

Day 5 was released before 09:00 and the runner only saw it at 09:05:15, because it was waiting for the wrong day. At release the mobile solver returned no value and the runner declined to submit. Time trial and mastery stayed unattempted because the single gates them. That early release led to the fix of remembering the last processed day and polling every 10 seconds.

The `order` list is ambiguous: it could be a sequence of part indices or the target position of each part. `mobsolve.py` joins the parts under both readings and returns a result only if exactly one gives a valid answer code. That branch is in the first committed `mobsolve.py`, from 5 October. All three modes were correct that morning, the single at 09:06:51, the time trial at 09:06:53 and the mastery at 09:06:55, but the notes do not record who solved them.

When the solver cannot be sure, it should refuse rather than guess.
