+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Out of Bounds"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-out-of-bounds"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-25-synthetic-vulnerability-root-cause
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 25's synthetic vulnerability root-cause set, with a corrected twin, was solved unattended in about a minute from release."

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

Day 25 asked 300 fields: Days 1 to 24 plus 12 about the root cause of a synthetic vulnerability, with a vulnerable and a corrected build supplied as a pair. The notes don't record what the new questions looked like, and the day was routine.

## The solve

The pipeline did all of it. The single and the time trial each resolved 300 of 300, and the mastery resolved 2,700 of 2,700 over nine sets, with a 39.7 second fetch and a 2.1 second solve. By the bench timings the three modes were CORRECT 12.6, 21.9 and 66.8 seconds after release, so the last one was in at 09:01:07.

The laptop had been off, so the agent ran preflight itself before the drop instead of leaving it to the timer. That is the only manual step the notes record.

Day 28 later re-asked the vulnerable role's config.

The solver already knew the family, which left little else to say about the day.
