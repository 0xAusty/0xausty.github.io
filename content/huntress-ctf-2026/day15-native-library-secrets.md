+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Native Library Secrets"
date = 2026-10-15  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day15-native-library-secrets"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 15 (2026-10-15), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-15-native-library-secrets
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The solve was automatic; the day's real result was the lane's first ranked time-trial run, which placed eighth on the speed board."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "daily.py", "bench.py"]
tags   = ["android", "dex", "jni", "time-trial"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asked for configuration split between the DEX code and a native library the challenge shipped. The notes do not describe what the original Day 15 APKs contained, and the solve did not depend on it: it was automatic.

## The solve

`daily.py` ran `mobsolve.py`'s static decode on all three modes at release. The recorded submissions are correct by 09:00:12, and the supervisor's summary at 09:00:31 agrees. The DEX emulator did not exist yet.

That afternoon `bench.py` re-ran the Day 15 time trials and masteries, mobile's included, on fresh regular variants. The first ranked attempt the team was granted was this time trial, at 12:42:43. An attempt 22 seconds earlier had asked for a ranked run and was not granted.

The result was #8 at 0.553 s against a leader at 0.391 s, with 1.66 s measured client-side. Board time is roughly artifact download plus solve plus submit, and each request cost about 150 ms of server time, so the solver was no longer the slow part.

Regular play scores points and is never ranked. A speed-board attempt has to ask for it with `run_for_time: true`.
