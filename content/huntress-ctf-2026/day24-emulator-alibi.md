+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Emulator Alibi"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-emulator-alibi"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-24-emulator-alibi
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The laptop was off at 09:00, and the single only passed on a lone-literal fallback; the time trial and mastery needed the Day 23 emulator wired into mobsolve.py."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["mobsolve.py", "mobemu.py", "python"]
tags   = ["android", "emulation", "fallback"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 24 asked for the exact backend answer code per mode, with a prompt about defeating app-owned environment checks on the same pinned emulator used by the solve oracle. What made it worth a note was the morning: the laptop was off at 09:00.

## The solve

A systemd persistent timer caught up at 09:14:20, and the run saw the release at 09:14:31. The single came back correct at 09:14:32, but only through the last-resort fallback, which accepts a code only when exactly one answer-shaped literal appears in the package. The time trial and mastery APKs use an "analysis" codec, where the app's DEX computes the code behind environment checks and decoy literals sit around it. The time trial returned nothing, and since each mode is locked behind the one before it, the mastery was never attempted.

The Day 23 emulator already solved these APKs. Claude Code wired `mobemu.solve_apk` into `mobsolve.solve_apk` ahead of the literal fallback, and the time trial and mastery were submitted in session at 09:29:53 and 09:29:57.

The single's pass said nothing about whether the solver could read these apps; the fallback had covered for it.
