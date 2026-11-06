+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "AutoIt Takes Two"
date = 2026-10-12  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day12-autoit-takes-two"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 12 (2026-10-12), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-12-autoit-workflow-pair
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The single solved itself, but the Time Trial and mastery hit rate limits at 09:00 and were recovered that afternoon and the next evening, by whom the notes don't say."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["polysolve.py", "python"]
tags   = ["malware-analysis", "autoit", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 12 added AutoIt polyglots: two inert AutoIt workflows presented as a matched pair, with a prompt asking which pairing is genuine. The single asked 855 fields. It was routine for the lane, and no script code change is recorded.

## The solve

The supervisor solved the single at release. It banked the confirmed fields, then resolved the ambiguous loop-expansion fields with the capped two-try. The single was CORRECT at 09:00:08, though the summary didn't log it until 09:00:55 because the 429 retries held it up.

The Time Trial ended at 9:00 with a rate-limit error on its POST, and the mastery's GET hit HTTP 429 as well. The Day 11 shared limiter was in place by then, but the burst still got through. The adaptive, deadline-aware limiter only arrived on 14 October.

The notes say the script lane was recovered the same day. The scoreboard has the Time Trial at 14:17:26 that afternoon, but the mastery not until 18:24:25 on 13 October. Who ran the Time Trial and mastery recovery isn't recorded, so `solved_by` lists only the pipeline's automatic single.

A shared limiter wasn't enough on its own to keep the timed modes clear of the 9:00 burst.
