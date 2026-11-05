+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Percent Chance"
date = 2026-10-07  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day07-percent-chance"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 7 (2026-10-07), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-07
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Percent-encoded blobs for a seventh day of the warmups lane, handled by an existing URL-decoding step and submitted by the supervisor at release in all three modes."

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

Same warmups shape as the days before it: decode the blob completely and submit the slug from its final non-empty line. The encoding this time was URL percent-encoding, given away by the prompt's line about an address bar having a moment, and the decode was routine.

## The solve

The `url` step in `wusolve.py` (urllib's unquote, applied when the text contains a percent sign) was already in the first committed decoder. The supervisor saw the release at 09:00:08 and had the single, the Time Trial and the 33-blob mastery all CORRECT by 09:00:22. Each blob is seven numbered chunks, and chunk *i* uses Day *i*'s encoding, so Day 7's percent-encoding lands in the slug.

I didn't solve it; the pipeline did, with no new code. Nothing in the notes records a snag.

The answer is the slug alone, three lowercase words and two digits, not the decoded sentence.
