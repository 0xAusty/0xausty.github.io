+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Keystore Misuse"
date = 2026-10-13  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day13-keystore-misuse"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 13 (2026-10-13), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-13-keystore-misuse
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine Android day: the pipeline's static decode answered single, time trial and mastery at release, and fresh variants passed again a few days later."

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

Every Android day asked the same thing in a new coat: one `answer` field, exact match, a backend answer code for a named case and app package. Day 13 was routine, and there isn't much to say about it.

## The solve

As soon as the release was seen, the pipeline's `daily.py` ran `mobsolve.py` on the single, the time trial and the mastery and submitted all three. The notes show each mode answered about a second after its start, and every submission was correct: the single at 09:00:05, the time trial at 09:00:07 and the mastery at 09:00:10. The supervisor's summary at 09:00:44 has all three. The time trial and mastery were timed, with server deadlines of 09:00:56 and 09:01:59, and both came back inside them.

On 16 October the improvement loop re-ran the time trial and mastery on fresh variants, and both passed again. The notes do not record which codec the puzzle asset used, so I won't guess at one.

Nothing here needed a fix. The static decode handled every mode on its own.
