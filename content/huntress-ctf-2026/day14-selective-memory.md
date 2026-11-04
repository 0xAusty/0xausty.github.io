+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Selective Memory"
date = 2026-10-14  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day14-selective-memory"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 14 (2026-10-14), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-14-objective-c-persistence-descriptor
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An Objective-C binary was routine; the mastery failed because the solvers' own leaked temp folders filled a quota'd /tmp, which looked like a full disk but wasn't."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["binsolve.py", "binmastery.py", "python", "Claude Code"]
tags   = ["reverse-engineering", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 14 asked 140 fields, Days 1 to 13 plus ten for an Objective-C binary with its raw config in a dedicated `.hcfg` section. The reverse engineering was routine. The mastery failing at release was the story.

## The solve

The single and the time trial were automatic: both resolved 140 of 140 and were CORRECT in the 09:00 sweep, with the day summary at 09:00:40. The mastery died with Errno 122, "Disk quota exceeded".

The disk wasn't full. `/tmp` was a RAM tmpfs with a per-user quota, and it held about 6.1 GB of evidence folders that the binary solvers had made every morning and never deleted, each with another copy of the 67 MB Swift member. The agent changed `binsolve.solve_bytes` to extract, solve and remove its directory in a `finally` block, and the mastery and Day 2 paths now clean up the same way. The auto-mode classifier wouldn't let it sweep the shared `/tmp`, so that cleanup command was left for me. With `/tmp` cleared, the existing solver answered the mastery through the practice continuation, CORRECT by 09:32:44 on the release morning; the exact time isn't recorded.

Check `df` on every mount, not just `/`.
