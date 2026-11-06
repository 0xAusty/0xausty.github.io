+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Make It Make Sense"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-make-it-make-sense"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-29-makefile-variant-diff
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Makefile polyglots at 1,747 fields: a routine automatic solve, remembered for a first-pass report that wrongly counted still-running lanes as misses."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["python"]
tags   = ["malware-analysis", "makefile", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 29 added Makefile polyglots. The prompt asked for variants and their earlier-language build chains to be diffed, keeping only conclusions that held across every variant. The solve was routine, but the automation around it had a bug.

## The solve

The autopilot banked the single at 09:00:10, the Time Trial at 09:00:14 and the mastery (thirteen sets, 23,829 fields) at 09:00:28, all at the release. No solver changes were needed.

The supervisor's first-pass report fired at 09:00:04 and listed script among the misses. It had counted every "running" lane as missed, and the script lane's three modes banked between 6 and 24 seconds later. That morning it was only a noisy notification.

The risk came that evening, when the report was wired to kick the escalator. The same bug could then have launched recovery agents on lanes seconds from CORRECT. It was fixed the next morning with a 90 second wait.

A false alarm in the monitor can do more damage than a slow solver.
