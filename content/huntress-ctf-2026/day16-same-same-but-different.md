+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Same Same, But Different"
date = 2026-10-16  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day16-same-same-but-different"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 16 (2026-10-16), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-16-obfuscation-equivalence
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The self-healing submit's first real catch: it found two changed answer values alone, then the parallel Time Trial and Mastery run hit a server lock."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["heal.py", "timed.py"]
tags   = ["malware-analysis", "ruby", "obfuscation", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Ruby polyglots and a Ruby host this time, 1,095 fields, and a prompt about which obfuscated variants are semantically equivalent. What mattered was the answer key for the expansion question, which had changed again.

## The solve

At release the supervisor's full submit was rejected. `heal.py` banked the confident fields, bisected by field family down to the two rejected `batch-*-expansion` fields, then tried the other enum values and found the right one for both. That took 23 submits and about 18 seconds, with no human involved. The single was in at 09:00:25 and the Time Trial passed on its first submit at 09:00:32.

The Mastery was a mistake of ours. The pipeline had been changed on 15 October to start it in parallel with the Time Trial, and the server answered HTTP 409: a Mastery stays locked until its Time Trial is correct. It passed at 09:01:12. Afterwards the new answer rule went into every mode from Day 16, and `daily.lane_pipeline` now runs single, Time Trial, Mastery in sequence. The notes don't record what triggered the 09:01 re-run.

The lock was already visible in the earlier history, and the optimisation ran straight past it.
