+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Root of Trust"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-root-of-trust"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-22-root-of-trust
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The last of five mobile days banked at release by the static decoder before any emulator existed; from Day 23 almost every mobile release missed a mode."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "root-detection"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 22 asked for the exact backend answer code per mode, with a prompt about modelling and bypassing several synthetic root signals without patching success globally. The mastery grew to six APKs, and the pipeline treated it as routine.

## The solve

`daily.py` solved and submitted the single, the time trial and the mastery through `mobsolve.py`'s static decode, and the supervisor's summary at 09:00:32 shows all three modes correct. The puzzle sat in `assets/huntress_puzzle.json`; the notes do not record the codec.

The day closed a five-day run, Days 18 to 22, in which the supervisor banked all three mobile modes at release with the static decoder, before any emulator existed. From Day 23 on, every mobile release except Day 27 missed at least one mode at 09:00, starting with a Day 23 time trial that returned nothing.

The emulator work that followed was a response to the end of that streak.
