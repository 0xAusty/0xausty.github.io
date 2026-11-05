+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "SQLite Assumptions"
date = 2026-10-12  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day12-sqlite-assumptions"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 12 (2026-10-12), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-12-sqlite-assumptions
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mobile Day 12 was solved unattended at release, and its timed modes could not be re-run later because the legacy route refused retries."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py"]
tags   = ["android", "sqlite", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 12 asked for a backend answer code, reached by reconstructing authorisation from a synthetic SQLite cache and proving server-side impact. It was routine, and the pipeline solved it with nobody watching.

## The solve

`daily.py` solved each mode about a second after starting it and submitted all three CORRECT: the single at 09:00:03, the time trial at 09:00:06 and the mastery at 09:00:08. The mobile time trial and mastery had deadlines of 09:00:35 and 09:00:37 and came back CORRECT inside them. The summary is stamped 09:00:55, 55 seconds after the release was seen, but it waited on slower lanes in a log full of 429 resends.

The timed modes could not be re-run later for benchmarking. The 16 October sweep got HTTP 409 `retry_variants_unavailable`, the legacy-route behaviour the handoff notes describe for most of Days 1 to 12.

If you want a timing for a legacy-route day, take it on the day; the server won't give you a second go.
