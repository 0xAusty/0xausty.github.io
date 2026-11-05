+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Spill the Beans"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-spill-the-beans"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-30-beanshell-jsp-graph
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "BeanShell polyglots inside an inert JSP host at 1,802 fields: the second-to-last Script day, solved automatically by the existing pipeline in all three modes."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["python"]
tags   = ["malware-analysis", "jsp", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 30 added BeanShell polyglots inside an inert JSP host, and the JSP host family grew from one file to two. The prompt called it the last piece of a thirty-language puzzle and asked for the edge that holds the execution, host and evidence graph together. For the pipeline it was routine.

## The solve

All three modes were banked at the release: the single at 09:00:09, the Time Trial at 09:00:12 and the mastery (fourteen sets, 26,572 fields) at 09:00:25. The notes record it as fully automatic, with no new solver code.

The supervisor's first-pass report went out at 09:00:31 and did not list script as a miss, so the false alarm from the day before had not come back.

A new language and a bigger host family changed what the solver had to read, and the same method still covered both.
