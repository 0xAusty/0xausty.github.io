+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Name Collapse"
date = 2026-10-17  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day17-name-collapse"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 17 (2026-10-17), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-17-name-collapse
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A new indexed codec defeated the release run; Claude Code fixed it with two readings and a unique-match check, but triage order made it wait until 09:12."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mobsolve.py", "daily.py"]
tags   = ["android", "obfuscation", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt described restoring behaviour after identifier shrinking and decoy insertion. The Android pipeline had been clean for days, and this was the first morning it returned nothing for the single.

## The solve

At release `mobsolve.py` found no answer, so nothing was submitted. Because the single gates the time trial and mastery, both showed as not attempted too. The supervisor had already exited at 09:00:24.

The puzzle used a new codec the notes call `indexed`: a 20-character data string and an `order` list. Claude Code fixed it in session. Character `i` of the string belongs at position `order[i]`, but `order` could mean target position or source index. So `decode_puzzle` builds both readings (scatter and gather) and keeps the one that is a valid answer code, only if exactly one is. That avoids guessing the convention.

The single was fixed at about 09:12, with the time trial correct at 09:12:32 and the mastery at 09:12:39. The fix was committed at 09:38.

It was a one-minute fix that waited about twelve minutes behind the metadata and binary work. The rule that came out of it: read every miss first and fix the cheapest first.
