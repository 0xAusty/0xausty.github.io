+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Big Entrance"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-big-entrance"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-20
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine day: the UTF-16 detector folded in for Day 19 apparently covered the big-endian follow-up, and the pipeline banked all three modes at release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py","python"]
tags   = ["encoding","time-trial","mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

The same bar as Day 19, and the prompt said the big one goes first. That points to big-endian UTF-16. Nothing here needed fixing, so this note is short.

## The solve

The pipeline solved all three modes on its own at release, with the catalog recording them at 09:00:04, 09:00:06 and 09:00:09. The notes do not name Day 20's encoding. My reading is an inference from the prompt and the code: the UTF-16 detector in `wusolve.py` already accepted a big-endian byte-order mark or an all-zero high-byte plane, and `wusolve.py` had no commits between the Day 19 fold-in and 21 October, so Day 20 ran on that code.

I can't show the decode step from the logs, only that the day ran unattended and came out correct.

The fix for the previous day's miss generalised to its mirror image the next morning.
