+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Entity Relations"
date = 2026-10-08  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day08-entity-relations"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 8 (2026-10-08), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-08
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "HTML entities were a new encoding for the decoder, but the day's real lesson was that a laptop in suspend made plain cron skip the 08:50 run entirely."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["wusolve.py", "daily.py", "claude-code"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

The warmups ask was unchanged: decode the blob, submit the slug. The encoding was HTML numeric and named entities, a new one for the decoder. The cipher was trivial. What went wrong that morning was the schedule.

## The solve

The 08:50 cron job never ran: the laptop was in S3 suspend, and plain user cron doesn't run jobs missed while suspended. Day 8 was then solved in a Claude Code session instead of by the cron run. The agent added an `html_entities` step to `wusolve.py` (it unescapes when the text contains numeric or named entities), committed at 09:13 on 8 October. The notes don't record when the first answer was accepted, so I won't give a time.

The stale day marker then sent the next morning's run back to Day 8. The fix was a self-healing marker, idempotent catch-up runs and a persistent systemd timer. Days 8 and 9 also came back untimed, after a week of short windows.

Read the live deadline on every start; don't assume the timer.
