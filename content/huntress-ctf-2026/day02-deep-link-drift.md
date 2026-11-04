+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Deep Link Drift"
date = 2026-10-02  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day02-deep-link-drift"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 2 (2026-10-02), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-02-deep-link-drift
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The Day 2 decode was a string reversal; the lesson was the clock, because the harness started five time trials before any solver existed and every one expired."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "mobsolve.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asks you to tell verified deep-link routing from a scheme and host that wave everybody through, but the APK only needed its asset puzzle decoded. Day 2's codec is a reversal of the `data` string. The decode is routine. The first day the clock bit is the interesting part.

## The solve

On 2 October the early harness swept all five Day 2 time trials in sequence with timed challenges switched on, before any analysis was ready. The deadlines were only about 5 to 8 seconds, so every one expired, mobile included. The handoff note from that day says to avoid starting a timer while analysis is still underway. The analysts spawned for the mobile APK also produced no usable result.

On 4 October the time trial and mastery were solved in one session. `mobsolve.py` reverses the string and accepts it only as a whole answer code. The notes credit that session with the mobile time trials and mastery runs, and the solvers were committed the next morning in a commit Claude Code co-authored. The single was already correct on 2 October, but the notes do not record who solved it.

Never start the timer before the solver exists.
