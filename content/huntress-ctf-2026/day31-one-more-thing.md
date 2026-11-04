+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "One More Thing"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-one-more-thing"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-31
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A three-layer decode chain where one missing first step in the fast search left a worker stuck and froze a supervisor that only reloads when idle."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["wusolve.py", "timed.py", "python"]
tags   = ["encoding", "base64", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

The last warmup was the only three-layer chain in the lane: Base64, then gzip, then Base32 in decode order, one chunk per day's encoding, with Day 31's landing in the answer slug. The decode itself was easy. The interesting part was what one missing entry did to the run.

## The solve

The supervisor solved the single and the Time Trial, but slowly, with answers ready 35.55 s and 26.87 s after each mode started. "base64+decompress" wasn't a first step in `wusolve.py`, so the fast per-chunk search never applied the Base32 step to the decompressed text and the blob fell through to the slow deep search.

The 153-blob Mastery made that expensive. A worker running the deep search pegged a core, and because the supervisor only reloads solvers and opens new work when no worker is running, every lane stalled. The log goes silent from 09:03 until the kill.

Claude Code, in a fresh recovery session, added "base64+decompress" and "decompress" to the first steps. That brought a blob to about 0.35 s, and it solved the Mastery inline. The Mastery was confirmed correct by 09:14:39.

One combined unwrap has to be a first step whenever another encoding sits beneath it, and one wedged worker shouldn't be able to freeze a supervisor.
