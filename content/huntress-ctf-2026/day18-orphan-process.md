+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Orphan Process"
date = 2026-10-18  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day18-orphan-process"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 18 (2026-10-18), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-18-process-story
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Google Apps Script carrier split its payload across a joined string array; joining the pieces was the whole fix, after heal recovered the enums."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["polysolve.py", "heal.py"]
tags   = ["malware-analysis", "google-apps-script", "obfuscation", "deobfuscation"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Google Apps Script polyglots and a Google Docs sidebar host, 1,194 fields, and a prompt about rebuilding the static process tree and catching the child that claims a parent it never had. The carrier was the interesting part.

## The solve

At release 40 fields were unmapped. The supervisor banked the rest, and its heal fixed 8 of the 13 rejected fields. Those were all role and technique enums, found by trying the accepted alternates. Five free-text fields (adapter, host profile, URL) stayed unfixed, because heal can only cycle through enum values.

Claude Code fixed the rest in session. The `.gs` carriers mark the descriptor with a `// HUNTRESS_ANALYSIS_V1:SPLIT` line and spread the payload across a joined array of string literals. `polysolve._split_payload` joins the array after the marker and decodes as before, which gave 1,194 of 1,194 without guessing. The Time Trial and Mastery then passed on their first submits. The records put the single at 09:03:30 and the Mastery at 09:03:46.

Fixes went cheapest first, so the metadata single was done before this one.

A SPLIT marker means the payload is an array to join, and joining it was the whole fix.
