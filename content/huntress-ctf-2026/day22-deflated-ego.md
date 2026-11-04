+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Deflated Ego"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-deflated-ego"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-22
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine day for the warmups lane: the previous day's decompress step apparently covered the new deflate wrapper, though a parallel-worker flaw surfaced later."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py","timed.py","python"]
tags   = ["encoding","time-trial","mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Another familiar wrapper, and this one needed "a little inflation", which points to a deflate-family stream. For the warmups lane it was a quiet day.

## The solve

The pipeline solved all three modes unattended at release, and the notes record the automatic lanes as banked by 09:00:22. They do not name the encoding. I am inferring that Day 21's decompress step, which chooses gzip, bz2, xz or zlib by magic bytes, and its combined Base64 step already covered it.

A flaw in the mastery solver only showed up later. The mastery solver fans blobs out to parallel worker processes, and each worker confirmed keyed ciphers on its own. A per-day rail fence proven on one blob never reached the blobs whose chunk straddles the seam where the sentence ends and the slug begins. On 28 October a commit made the parent process re-learn every solved blob's keys and retry the unsolved ones once, which brought Days 22 and 23 mastery back to full.

Keys proven in one worker are lost unless the parent collects them.
