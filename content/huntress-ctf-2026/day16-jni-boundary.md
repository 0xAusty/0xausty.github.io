+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "JNI Boundary"
date = 2026-10-16  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day16-jni-boundary"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 16 (2026-10-16), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-16-jni-boundary
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Single and time trial were automatic, but starting the mastery in parallel with the time trial ran into a server unlock rule, so the pipeline went sequential."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["mobsolve.py", "daily.py"]
tags   = ["android", "jni", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt was about a Java-to-native type or length assumption changing backend authorisation. The solver treated it like every other Android day. What went wrong that morning was in the pipeline.

## The solve

The single and time trial were answered at release, at 09:00:09 and 09:00:11. The mastery failed with HTTP 409. The previous day's optimisation started the time trial and mastery in parallel, but the server only unlocks the mastery once the time trial is correct. The notes show 44 solved pairs, and in none of them had a mastery been solved before its time trial, so the rule was sitting in our own data the whole time.

Claude Code re-ran the mastery in session and it landed at 09:00:58, 47 seconds after the time trial. Three lanes lost their mastery the same way. The fix made `daily.py` run single, time trial and mastery strictly in sequence, with a test.

The ranked time trial later sat at #1 with 0.409 s until someone posted 0.407 s. I read 0.409 s off the board, which helped calibrate the board's stamp against our own clock. A chase to win it back never fired, because artifact probes stayed slower than its trigger.

Check a gating rule in the history before parallelising across it.
