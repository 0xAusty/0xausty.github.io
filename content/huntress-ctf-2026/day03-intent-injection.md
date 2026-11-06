+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Intent Injection"
date = 2026-10-03  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day03-intent-injection"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 3 (2026-10-03), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-03-intent-injection
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A one-step base64 decode of an asset puzzle on Day 3; routine, with its time trial and mastery cleared in the 4 October agent session."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "mobsolve.py"]
tags   = ["android", "base64", "time-trial"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asks for attacker-controlled extras traced through an internal navigation boundary. The APK itself only needed its asset puzzle decoded, and Day 3's codec is base64. It was routine, and the notes record no incident.

## The solve

`mobsolve.py` base64-decodes the puzzle's `data` field and only accepts the result if it's a whole answer code. If the one-step decode doesn't give exactly that, it falls through to a generic decode search, which insists on the same whole-string match.

One session on 4 October solved the time trial and mastery. The notes say it went from 25 to 48 of 62 and cleared all the mobile, warm-up and metadata time trials and mastery runs. The solvers were committed on 5 October in a commit Claude Code co-authored. The scoreboard puts the single at 18:01:34 on 4 October, the time trial at 18:02:36 and the mastery at 18:03:26. The notes don't say who solved the single, so I make no claim for it.

The whole-string check is what stops a decoder from submitting a partial result.
