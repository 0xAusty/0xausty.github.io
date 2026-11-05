+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Encrypted Strings"
date = 2026-10-18  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day18-encrypted-strings"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 18 (2026-10-18), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-18-encrypted-strings
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine Android day: the static decode answered single, time trial and mastery within seconds of release, with nothing to fix afterwards."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "daily.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asked for only the strings that reach security-sensitive Android and backend APIs. The answer format was the usual single `answer` field. This was a routine day with nothing to fix.

## The solve

`daily.py` ran `mobsolve.py`'s static decode on all three modes, about 0.7 to 1.6 s after each started, and submitted all three. The submissions were correct at 09:00:03, 09:00:05 and 09:00:07, with the supervisor's summary at 09:00:44. The notes count it among the nine modes the pipeline took on its own that morning, alongside the warmups and binary lanes.

The notes do not record the codec the puzzle used, so there is nothing more to say about the mechanism.

An unattended day is the result the solver was built for.
