+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Bacon Bits"
date = 2026-10-17  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day17-bacon-bits"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 17 (2026-10-17), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-17
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Five-letter a/b groups were hex nibbles, not classic Bacon letters, so the existing Bacon step produced nothing until a nibble-based step was added."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["kpa.py", "python"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 17's prompt described sixteen guests with five little a's and b's apiece: a Bacon-style cipher. It looked covered, because a classic Bacon step had been in the decoder since 14 October. It was not the classic kind.

## The solve

At release the single stayed unsolved, and the time trial and mastery were not attempted. The classic step maps five bits to a letter and did not produce the sentence. Here each group is a hex nibble, with a=0 and b=1 and the first bit always a, so two groups make one byte.

Claude Code added `kpa._bacon_bits` in session, with a nibble step and an 8-bit step. The line-oriented solve took 0.03 s, and the time trial and mastery then solved with no further change. The single was in at 09:01:29 and the mastery at 09:02:34, the quickest fix among the lanes that changed their question that morning.

The gate also matters. Each mode unlocks the next, so one missed single blocks all three.

A cipher's name tells you the family, not the mapping.
