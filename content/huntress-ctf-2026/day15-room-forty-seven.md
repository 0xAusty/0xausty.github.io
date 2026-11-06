+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Room Forty-Seven"
date = 2026-10-15  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day15-room-forty-seven"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 15 (2026-10-15), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-15
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Punctuation that went for a spin pointed to ROT47, and that afternoon's speed work turned a 73-blob mastery into one search plus direct decodes."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["kpa.py", "wusolve.py", "python"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 15 was the standard decode-the-blob question. The prompt said even the punctuation went for a spin, and the title was Forty-Seven, which points to ROT47 (it rotates all printable ASCII). The notes never name the encoding, so that is my inference.

## The solve

The existing decoder solved all three modes at release. ROT47 had been added to `kpa.py`'s extra steps the day before, which is the likely reason, though no note says so. The single was CORRECT at 09:00:07, the time trial at 09:00:11 and the mastery at 09:00:19.

The speed work that afternoon mattered more. Every warmups mastery blob shares one encoding schedule, so one full search teaches the path for the rest. The speed loop's second iteration made the mastery schedule-driven: later blobs decode directly with `wusolve.decode_with`, which accepts only the exact prefix and an all-dictionary slug and otherwise falls back to the search. Days 13 to 15 mastery solves went from 2.4-4.4s to 0.06-0.09s.

That evening the Game Master's API description also showed that regular play is untimed and that a ranked attempt needs `run_for_time`. My runners had never asked for one.
