+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Debug Me If You Can"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-debug-me-if-you-can"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-21-debug-me-if-you-can
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An anti-debug state-machine puzzle that needed no human or agent on the day: the pipeline's static decode banked all three modes at release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "anti-debug"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 21 asked for one `answer` per mode, the exact backend code for a case and app package. The prompt talked about neutralising a clean-room anti-debug state machine while keeping the intended app flow. For the pipeline it was routine, the fourth of five unattended mobile mornings in a row, Days 18 to 22.

## The solve

`daily.py` solved and submitted the single, the time trial and the five-APK mastery through `mobsolve.py`'s static decode, and the supervisor's summary at 09:00:21 shows all three correct. As on the neighbouring days, the puzzle sat in `assets/huntress_puzzle.json`, and the notes do not record the codec it used.

The handoff file sums the morning up in one line: script and mobile, three of three, automatic.

There was nothing to flag, and nothing in the solve I would claim as mine.
