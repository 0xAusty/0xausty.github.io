+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Eight Is Enough"
date = 2026-10-06  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day06-eight-is-enough"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 6 (2026-10-06), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-06
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The first fully unattended warmups day: an octal blob that the decoder had carried since 5 October, solved in all three modes by the supervisor within seconds of release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py", "daily.py"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

A blob of space-separated octal numbers, and one question: what slug does its last decoded line tell you to submit? It was routine, and nobody touched it.

## The solve

The `octal` step in `wusolve.py` (base-8 numbers below 256, read as bytes) was already in the first committed decoder, so there was nothing to write. The supervisor, `daily.py`, picked up the release at 09:00:09 and had the single, the Time Trial and the 28-blob mastery all marked CORRECT by 09:00:21. Each blob is six chunks, and chunk *i* uses Day *i*'s encoding, so Day 6's octal ends up inside the slug.

I didn't solve anything here. This was the first warmups day the pipeline cleared with no one at the keyboard, so it matters more to the lane's story than the cipher does.

The answer is the slug alone, never the decoded sentence.
