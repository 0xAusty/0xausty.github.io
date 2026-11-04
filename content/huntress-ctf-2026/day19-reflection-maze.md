+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Reflection Maze"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-reflection-maze"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-19-reflection-maze
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine mobile release that the pipeline banked at 09:00 with its static decoder, but whose reflection theme came back and broke the emulator on Day 25."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "dex", "reflection"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 19 asked for one `answer` per mode: the exact backend answer code for a named case and app package, in the fixed answer-code shape. The prompt was about reconstructing reflective dispatch across generated, equivalent call graphs. As a solve it was routine, and the pipeline handled it without me.

## The solve

`daily.py` found the release, ran each APK through `mobsolve.py`'s static decode and submitted the single, the time trial and the five-APK mastery. All three came back correct, and the supervisor's summary line is stamped 09:00:26. The notes do not record which codec the puzzle used, so I won't guess at it.

The reflection theme mattered later. On Day 25 one mastery set was a Day 19-style app whose router method reaches its target methods through `Class.forName`, `getDeclaredMethod` and `Method.invoke`. The emulator could not follow that chain until Claude Code added reflection support, which is told on the [Day 25 note](/huntress-ctf-2026/day25-integrity-signals/).

A clean unattended day, and a puzzle shape worth remembering for what it cost the emulator six days on.
