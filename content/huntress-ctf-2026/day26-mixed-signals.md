+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Mixed Signals"
date = 2026-10-26  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day26-mixed-signals"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 26 (2026-10-26), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-26-beam-message-flow
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Erlang escript polyglots with 1,615 fields in the single, banked at release without intervention, and later cited in a retro as proof that covered shapes solve in seconds."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = []
tags   = ["malware-analysis", "erlang", "mastery", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 26 added Erlang escript polyglots. The prompt asked for message flow to be traced and for true cross-language indicators to be told apart from deterministic collision decoys. The single asked 1,615 fields, the Time Trial 1,677 and the mastery ten sets, 16,770. It was routine for the script lane.

## The solve

The pipeline banked all three modes at release with no intervention and no recorded solver change. The single was confirmed at 09:00:06, the Time Trial at 09:00:09 and the mastery at 09:00:15, and the log shows all three correct by 09:00:18.

The day mattered more as a data point than as a puzzle. The Day 26 retro cites the metadata and script lanes as proof that when a shape is covered, the answers arrive in seconds. The time lost that day came from new shapes in other lanes and from web challenges, not from here.

The Erlang decoys were only a hazard for a solver that had not seen the shape, and this one had.
