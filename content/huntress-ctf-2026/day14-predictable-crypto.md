+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Predictable Crypto"
date = 2026-10-14  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day14-predictable-crypto"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 14 (2026-10-14), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-14-predictable-crypto
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Routine at release, but the replay gate caught a second, deeper answer on Days 7 and 14 once a new rot5 step landed in the warmups code."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "wusolve.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt talked about seeded nonces and weak derivation. The pipeline never had to reason about either, because the puzzle sat in the APK's asset file in a shape the generic decode search already handled. Live, the day was routine. The replay gate found something later.

## The solve

`mobsolve.py` decoded the single, the time trial and the mastery at release, and the three were correct at 09:00:05, 09:00:07 and 09:00:12 (the supervisor's summary came at 09:00:40). The timed modes had deadlines of 09:00:36 and 09:00:38 and came back correct inside them.

On 14 October the replay gate showed a problem. Once the warmups solver gained a rot5 step, the same real code decoded to a second, deeper answer-shaped string on Days 7 and 14. The old rule demanded uniqueness at every depth, so it now refused. The fix lets the shallowest depth decide, provided it is unique there, so a deeper decoy cannot win.

The gate replays mobile whenever the warmups code changes, because `mobsolve.py` reuses its decode steps. That is why this was caught before it could cost a live answer.

Shared helpers couple lanes, so the replay corpus has to cross lane boundaries too.
