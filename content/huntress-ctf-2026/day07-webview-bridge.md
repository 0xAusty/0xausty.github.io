+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "WebView Bridge"
date = 2026-10-07  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day07-webview-bridge"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 7 (2026-10-07), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-07-webview-bridge
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mobile Day 7 solved itself at release, and a week later its puzzle showed why a decode search must rank answers by depth as well as check uniqueness."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py"]
tags   = ["android", "encoding", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 7 had a single answer field: a backend answer code for a case, reached by crossing a challenge-owned WebView bridge through an untrusted origin. The solve was routine, and the part worth writing up came a week later.

## The solve

Nobody touched it at release. The puzzle sits in `assets/huntress_puzzle.json` inside a small APK, and the generic decode search in `mobsolve.py` took it through its chain of decode steps. Against a release logged at 09:00:08, the single was CORRECT at 09:00:11, the time trial at 09:00:13 and the mastery at 09:00:21. The time trial and mastery were timed, and both came back inside their deadlines.

On 14 October the replay gate flagged a regression. A new digit-rotation step (rot5) turned the real code into a second, deeper, well-formed answer-code string on Days 7 and 14. The old rule collected codes at every depth and required exactly one, so it would have refused both days. The fix, committed that day, lets the shallowest depth that yields a code decide, and the code has to be unique at that depth. None of this reached the board, because the gate caught it from the corpus.

A rotated code still looks like a valid answer, so the search has to rank by depth.
