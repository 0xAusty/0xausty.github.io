+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Safe Travels"
date = 2026-10-11  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day11-safe-travels"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 11 (2026-10-11), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-11
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Every blob decoded correctly, but the serial 53-blob solve missed a 7-10 second window; a parallel decode and trimmed hot loops made the mastery score."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["wusolve.py", "timed.py", "daily.py", "claude-code"]
tags   = ["encoding", "base64", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

This time it was URL-safe Base64, with the warmups question unchanged. Every one of the mastery's 53 blobs decoded correctly, and the mastery still missed at release because the solve ran out of time.

## The solve

The supervisor submitted the single and the Time Trial at release, and both came back CORRECT, at 09:00:02 and 09:00:04. The mastery decoded its 53 blobs one after another and finished at t+12.37s, against a deadline of roughly 7-10s. Its submit also hit an HTTP 429 in that morning's burst of parallel lane processes.

A fresh Claude Code session fixed it (commit 09:16:08). `timed.solve_artifact` now decodes a zip of more than four blobs across a fork `ProcessPoolExecutor`. `wusolve.py` got a cached translate table per Caesar shift and an ASCII and printable check in place of the per-character loops, which gave about 3.6x per blob, byte-identical over 180 differential trials. The re-run, which came before that commit, reported the submit CORRECT at t+4.00s.

On a timed mode, throughput is part of correctness. If you want fork, ask for it explicitly: Python 3.14 defaults to forkserver on Linux.
