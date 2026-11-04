+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Crystal Clear"
date = 2026-10-13  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day13-crystal-clear"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 13 (2026-10-13), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-13-crystal-dns-configuration
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Crystal binary on a language the pipeline had never seen: the first binary day banked in all three modes at release with nobody in the loop."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["binsolve.py", "binmastery.py", "python"]
tags   = ["reverse-engineering", "elf", "base64", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 13 asked 130 fields: Days 1 to 12 plus ten for a Crystal ELF whose config is a base64 string literal. The language was new to the pipeline and the challenge was routine for it.

## The solve

Nothing was written for it. The generic handler resolved all 130 fields for the single and for the time trial, and `binmastery.py` resolved all 390 for the mastery. All three modes were CORRECT in the 09:00 sweep on 13 October, and the day summary was written at 09:00:44. The shared rate limiter from Day 11 was in place, and this time nothing was lost to a 429.

It was the first binary day banked in every mode at the release with nobody in the loop. The catalog's extra time-trial and mastery attempts are re-runs from the improvement loop on 16 October, not first solves.

The notes keep only family counts for this day's questions, so I can't say more about the fields beyond the usual set.

New language, no new code: that was the point of the Day 10 handler.
