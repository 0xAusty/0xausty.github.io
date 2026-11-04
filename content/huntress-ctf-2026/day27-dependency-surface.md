+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Dependency Surface"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-dependency-surface"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-27-dependency-surface
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine day: the Day 23 to 26 solver fold-ins, including split-bundle merging, handled a mixed-template 11-set mastery with nobody involved."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "mobemu.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asked which generated dependency flaw was reachable from an exported mobile surface, and the question wanted the backend's answer code. It was routine. Nothing broke and nothing needed fixing.

## The solve

The pipeline solved all three modes unattended with the code folded in over Days 23 to 26: the emulator, the split-bundle merge and the fallback to emulation for any computed codec. The single, time trial and mastery were correct by 09:00:15, at release.

The 11-set mastery mixed earlier templates, which you can tell from the file sizes. One set was the size of Day 10's app, one matched Day 20's, and one was a split bundle like Day 26's. The notes do not say which decode path each mode or set took, so I won't guess.

Its only value is as evidence that the previous days' fixes generalised to a new day's apps without anyone touching them.
