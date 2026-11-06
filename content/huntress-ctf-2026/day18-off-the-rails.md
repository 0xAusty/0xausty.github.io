+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Off the Rails"
date = 2026-10-18  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day18-off-the-rails"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 18 (2026-10-18), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-18
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A three-rail rail fence was solved unattended; the single taught the key that the mastery's slug chunk reused, a dependency Day 19 exposed."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["kpa.py", "wusolve.py", "python"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 18 hinted at three rails and one very zigzag commute, which reads as a rail fence cipher with three rails. The notes do not name the encoding, so that reading comes from the prompt and from a later record of a three-rail chunk. Nothing went wrong.

## The solve

All three modes were CORRECT at release, and the 88-blob mastery solved in 1.02s. It ran on the known-plaintext work from 14 October. `kpa.solve` derives a rail-fence key from the known sentence and keeps it only if the decode reproduces that text. `wusolve.learn()` stores the key and offers it as a step in the time trial and mastery, which run in the same lane process. `kpa.hint_steps` can also turn the prompt's number words into candidates.

The slug chunk has no known plaintext, so its key has to come from the single's learned cache or from the prompt, and the notes do not record which one fired here. Day 19's clean-cache replay later showed that the next day's mastery depended on that cache.

The single teaches the key that the mastery's last chunk reuses.
