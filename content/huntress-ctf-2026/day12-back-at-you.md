+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Back at You"
date = 2026-10-12  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day12-back-at-you"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 12 (2026-10-12), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-12
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine layered-encoding blob: the first decoder already handled the reversed-text step, and all three modes were solved by the pipeline at release."

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

Day 12 had the standard warmups shape: decode a blob of numbered lines and submit the slug its last line asks for. The clue hinted at reversed text, and that was the only twist.

## The solve

The first committed decoder already had the reverse step, so the pipeline solved all three modes at the 09:00 release run without help. The mastery had 58 blobs of twelve chunks each. By the lane's rule chunk 12 uses Day 12's encoding, so that encoding lands in the slug. The mastery's answers were ready about 5 seconds into its run.

The 09:00 burst did hit HTTP 429 rate limits that morning, but on the script and binary lanes. A later sweep could not re-run the time trial or mastery, because the server answered 409 and offered no fresh variants.

The reverse step from the first decoder was all this day needed.
