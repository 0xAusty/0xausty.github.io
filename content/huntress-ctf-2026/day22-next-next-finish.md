+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Next, Next, Finish"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-next-next-finish"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-22-installer-script-chain
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "NSIS installer-script polyglots with 1,417 fields in each of single and Time Trial, plus the first mastery of six sets, all banked automatically within about 20 seconds of release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = []
tags   = ["malware-analysis", "nsis", "mastery", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 22 moved to NSIS installer scripts. The prompt asked for real setup actions to be separated from modelled payload behaviour, and for every cross-language handoff to be recovered. The single and the Time Trial each asked 1,417 fields. The new thing was size: the mastery was the first with six sets, 8,502 fields. The solving was routine.

## The solve

The 09:00 cron handled all three modes with the existing script modules. The single was confirmed at 09:00:07, the Time Trial at 09:00:10 and the mastery at 09:00:17, and the supervisor logged its summary at 09:00:32. The notes have the automatic lanes banked about 22 seconds after the release was seen. The convention notes record the day as 21 of 21 modes correct, four of the standard lanes among them automatic.

No solver change is recorded. The extra set count made the mastery larger but not different in kind.

The set count didn't matter to a pipeline that derived every answer from the bundle.
