+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Mobile Arena Gauntlet"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-mobile-arena-gauntlet"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-31-mobile-arena-gauntlet
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Fourteen of fifteen mastery apps solved unattended; the one failure loaded a second DEX at runtime, which the emulator then learned to do."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["mobsolve.py", "mobemu.py", "python"]
tags   = ["android", "dex", "emulation", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The last mobile day was a mass-generated campaign composing every earlier mobile primitive. The single and time trial were routine and solved by the pipeline at release, by 09:00:24. The 15 mastery apps mixed earlier templates.

## The solve

Fourteen of the mastery sets solved unattended. Set 10 was a Day 20-style app that loads `payload.dex` from its assets at runtime, which the emulator had never needed, and it failed with a comparison between a null and an integer. The release run reported one unmapped set.

Claude Code extended `mobemu.py` inline. It added runtime second-DEX loading, with the asset stream read into a byte array and handed to a class loader whose methods are registered so reflection can reach them, plus array-copy, buffer and string methods. It also made the if-test compares treat a null reference as 0. Dalvik compares a null against zero, and a Python model of registers has to do the same.

The mastery's exact time is not recorded. The catalog carries the supervisor's 11:58:29 summary, but the 09:45 fold-in commit already reports every Day 31 lane banked. The escalator only fires on unsolved singles, so a mastery-only miss never triggered it.
