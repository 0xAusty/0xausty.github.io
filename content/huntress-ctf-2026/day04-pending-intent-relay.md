+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Pending Intent Relay"
date = 2026-10-04  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day04-pending-intent-relay"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 4 (2026-10-04), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-04-pending-intent-relay
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 4 layered a single-byte XOR over base64 in the same puzzle file, with the key sitting next to the data; routine, and released on a day of 503 errors."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "mobsolve.py"]
tags   = ["android", "xor", "base64", "time-trial"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asks you to recover and redirect a mutable PendingIntent while preserving every earlier component check. The APK only needed its asset puzzle decoded. Day 4's codec is base64 followed by an XOR, with the integer key stored in the puzzle JSON itself. Routine.

## The solve

`mobsolve.py` base64-decodes `data`, XORs every byte with the puzzle's `key`, and accepts the result only as a whole answer code. The order matters: the XOR comes after the base64 unwrap.

The time trial and mastery were solved on 4 October, in the same session that cleared the other mobile, warm-up and metadata time trials and mastery runs. The solvers were committed the next morning in a commit Claude Code co-authored. I have no per-mode times, and the notes do not say who solved the single.

Day 4 was released on a day when the Game Master also returned a 503 release-unavailable error for hours, so the release itself was the awkward part.

The key was in the file, so the XOR was no barrier.
