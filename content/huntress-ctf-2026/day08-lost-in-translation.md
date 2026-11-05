+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Lost in Translation"
date = 2026-10-08  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day08-lost-in-translation"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 8 (2026-10-08), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-08-cross-language-iocs
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The first polyglot carriers tagged themselves with an encoded descriptor, so polysolve.py read each file's role and technique from the file instead of guessing it."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["polysolve.py", "python"]
tags   = ["malware-analysis", "encoding", "base64", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 8 changed the shape of the lane. Instead of a new language with its own codec, the files were PHP polyglots and WSF, HTA and PHP-webshell hosts, and the questions covered role, technique, campaign, stage count and similar fields (615 in the single). The interesting part was that each carrier states its own answer.

## The solve

Every polyglot and host file carries a `HUNTRESS_ANALYSIS_V1` comment in one of four encodings: hex, fragmented hex, base64, and hex text that decodes to base64 text. The new `polysolve.py` undoes the encoding, reads the descriptor and answers by field name, taking the technique straight from it.

The 08:50 cron never fired, because the laptop was asleep, so Claude Code worked the day manually in the session. The single reached 606 of 615 by 09:18 ET, with only the batch-expansion fields left, and was completed in session. The notes don't record the mechanism for those last fields. The mastery was 3,075 fields over five AES-protected sets and was deterministic except for 20 loop-expansion fields, which the capped two-try cleared.

The platform also dropped the timers from this day, so the timed modes ran untimed by default.

The descriptor pattern carried the lane through the rest of the month.
