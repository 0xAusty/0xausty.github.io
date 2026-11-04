+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Back in Sixteen"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-back-in-sixteen"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-28
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine warmup: the prompt hints at hex plus a reversal, and the solver's per-chunk search chained both steps with no intervention."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["encoding"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 28's warmup was another decode-and-find-the-slug blob, tiny at 220 bytes for the single. It was routine, and the pipeline solved it on its own.

## The solve

The autopilot banked the single by 09:00:08, the Time Trial by 09:00:10 and the Mastery by 09:00:14. No session was involved.

The notes do not name the encoding. The prompt points to hex combined with a reversal, and both `reverse` and `hex` are in the first-step set of `wusolve.py`, so the per-chunk search could have chained them. The prompt's "sixteen-fingered friend" reads as hex and "walking backwards" as a reversal. That is my inference from the prompt and the solver, not something the logs confirm. The Mastery was 138 blobs of 28 chunks each, and it went through the same way as the single.

Nothing here needed a fix, which was the point of the earlier days' coverage work.
