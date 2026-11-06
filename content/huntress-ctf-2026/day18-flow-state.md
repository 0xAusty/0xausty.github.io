+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Flow State"
date = 2026-10-18  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day18-flow-state"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 18 (2026-10-18), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-18-control-flow-reconstruction
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 18's control-flow reconstruction bundle of 216 fields solved itself first try, on facts the agent had added the day before."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["binsolve.py"]
tags   = ["reverse-engineering", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 18 was control-flow and call-graph reconstruction, and routine for the pipeline: 216 fields (Days 1 to 17 plus 12 new ones), the same 216 for the time trial, and 864 for the mastery.

## The solve

Nothing was fixed in session. The single, the time trial and the mastery were solved automatically at release, using the per-day facts Claude Code had added in session on Day 17. The log records the single at 216 of 216 about 6 seconds after release, and the mastery was fetched, solved and accepted in about 21 seconds. All three modes were correct by 09:00:36.

The notes do not record what the Day 18 questions themselves asked. Day 28 later re-asked the binary through handler symbols named for success, decoy and failure events, which is the only hint of its contents.

The previous day's fixes paid off the next morning: a 216-field bundle solved first try.
