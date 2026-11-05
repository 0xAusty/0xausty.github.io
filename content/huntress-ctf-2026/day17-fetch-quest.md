+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Fetch Quest"
date = 2026-10-17  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day17-fetch-quest"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 17 (2026-10-17), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-17-download-graph
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "AutoHotkey polyglots and a download-graph question that the pre-warmed script lane cleared in all three modes by 09:00:19, its best finish to that point."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = []
tags   = ["malware-analysis", "autohotkey", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

AutoHotkey polyglots this time, with a prompt about reconciling the fetch targets a script declares against the generated network evidence, and finding the indicator seen on only one side. The single asked 1,139 fields in the usual shape, and what stood out was how fast they went in.

## The solve

Nothing needed fixing. The pre-warmed script lane (workers started at 08:59:30 and 08:59:57, warm node servers, and the solve trim from 16 October) submitted the single, the Time Trial and the Mastery correctly on the first try. The records put them at 09:00:05, 09:00:08 and 09:00:19, with the supervisor's summary at 09:00:23. No script fix is listed for the day.

It was the lane's best finish up to then, and it came on a morning when four other lanes changed their questions.

The speed work paid off on a day with no analysis story.
