+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "All the World's a Stager"
date = 2026-10-09  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day09-all-the-world-s-a-stager"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 9 (2026-10-09), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-09-stager-relationships
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A keyed transform with an empty key crashed bashsolve.py on one fixture; guarding it to fall back to identity fixed the Time Trial, while the single had solved at release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["bashsolve.py", "python"]
tags   = ["malware-analysis", "lua", "bash", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 9 added Lua polyglots, SCT and Lua hosts and two more advanced bash fixtures. The prompt asked for the stage whose claimed lineage is impossible, and the fields were the usual families. Routine for the lane, apart from one crash.

## The solve

The existing dispatch solved the single. The supervisor banked the confirmed fields in one submit, then tried each ambiguous loop-expansion field alone, at most two labels each. The single was CORRECT at 09:02:12, about two minutes after the drop, because the 08:50 run had spent itself re-confirming Day 8 on a stale marker. `daily.py` now advances past days that are already solved.

At release the Time Trial was held back as unmapped and the mastery returned HTTP 409. The cause was a fixture whose codec named a keyed transform with an empty key. That raised an `IndexError` in `bashsolve._transform` before the identity path was reached. Claude Code made keyed transforms fall back to identity, and the Time Trial and mastery were CORRECT at 09:08:06 and 09:09:30. The mastery's 30 loop-expansion fields went through the capped two-try.

An empty key must degrade to identity, not crash.
