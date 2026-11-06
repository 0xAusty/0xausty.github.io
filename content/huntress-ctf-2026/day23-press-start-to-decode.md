+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Press Start to Decode"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-press-start-to-decode"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-23-game-resource-loader
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A new question shape, opaque hex-id file names and a layered codec, broke the automatic script lane; the Time Trial and mastery needed a recovery session and a family-split diagnosis."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "homebase", "chatgpt", "agent"]

tools  = ["polysolve.py", "scriptsolve.py", "daily.py"]
tags   = ["malware-analysis", "obfuscation", "deobfuscation", "mastery", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 23 added GDScript (Godot) resource loaders. The single (1,461 fields) was automatic by 09:00:06. The Time Trial and mastery switched to a new question set: fields named by language and hex id over opaque hex-named files, plus combined fields joining two labels. At release 969 of the Time Trial's 1,495 fields had no mapping, and the supervisor's retry loop sent 544 submits without fixing one.

## The solve

A Claude Code session that took over from a crashed one rewrote `polysolve.py` for the layered codec. Its steps are base64, base32, hex, reverse and a fragment step that only sprinkles dot noise, so the dots are stripped. All 75 polyglot files decoded and the Time Trial reached 1,164 of 1,495. The other 331 base-language fields needed `scriptsolve.py` to find files by hex id and derive role, technique and indicators from the decoded descriptor, not name tables.

The rest happened in a separate recovery session, completed at 10:33. Submitting by language family narrowed 68 unaccepted fields to the PowerShell and Python groups, settled two grading conventions and got the Time Trial accepted. The mastery of 10,465 fields then went in as one complete submission. That session used the event's Homebase AI (GPT-6 Luna) and my own ChatGPT account; the notes do not say which produced what. A replay of 234,407 earlier comparisons showed no regressions.

Each mode was locked behind the one before, so every field had to be right.
