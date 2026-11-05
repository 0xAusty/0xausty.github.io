+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "The Full Transform"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-the-full-transform"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-31-xslt-final-gauntlet
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The finale: a 29,250-field XSLT mastery across all 31 languages, solved by the same deterministic pipeline with no new code on a morning when other automation was failing."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["python"]
tags   = ["malware-analysis", "xslt", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 31 was the Script lane's last challenge: XSLT polyglots in a final gauntlet that tied together all thirty-one languages and every host profile. The single had 1,846 fields and the mastery fifteen sets with 29,250. The interesting part is what did not change.

## The solve

The same deterministic pipeline solved it, and the notes record no script solver commit after the Day 23 fold-in. The single was confirmed at 09:00:25, the Time Trial at 09:00:41 and the mastery at 09:03:12.

The mastery was slower than before. Its solve step took about 142 seconds for 29,250 fields, against about 10 seconds for 26,572 on Day 30. The notes do not state why. They do record a stuck warmups worker pegging a core from 09:00 and a crashed coordinating session that morning.

The supervisor still caught the 09:00 drop and banked the deterministic singles, and the day's retro counts the day 15 of 15 recovered after the crash and a dead escalator.

The takeaway is that a lane built to run unattended did, on the one morning it was tested hardest.
