+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Web of Lies"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-web-of-lies"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-24-jsp-webshell-source
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "JSP webshell-source polyglots on the hex-id question shape that needed a recovery session the day before; the pipeline solved it in seconds, but only after the laptop woke at 09:14."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["daily.py"]
tags   = ["malware-analysis", "jsp", "mastery", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 24 added JSP webshell-source polyglots and a JSP host. The single asked 1,516 fields and the Time Trial 1,560, in the hex-id shape that had needed a long recovery the day before. The prompt asked for requests and stages to be ordered and for inert fixture behaviour to be separated from real execution primitives. The solve took seconds. It just started late.

## The solve

The Day 23 refactor was already on disk (uncommitted until 10:08 that morning), so nothing new was needed. The laptop was off at 09:00 and the cron did not run on time. When the machine woke, the systemd timer caught up and saw the release at 09:14:31.

The single was confirmed at 09:14:34, the Time Trial at 09:14:37 and the mastery (eight sets, 12,480 fields) at 09:14:42. That is 3, 6 and 11 seconds after the release was seen. The supervisor summary followed at 09:14:58, and in that run it banked 6 of 21 modes in 38 seconds, the three script modes among them.

The lateness came from the machine being off, and the score clock does not wait for a laptop to wake.
