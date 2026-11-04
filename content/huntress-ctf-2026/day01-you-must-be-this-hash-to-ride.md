+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "You Must Be This Hash to Ride"
date = 2026-10-01  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day01-you-must-be-this-hash-to-ride"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 1 (2026-10-01), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-01-hash-to-ride
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The opener of the metadata lane: filename, size and three digests, all taken from the bytes of the member the question names."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["metadata", "forensics"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 1 asked five identity questions about a named member of a small evidence zip: its exact filename, its size in bytes, and its MD5, SHA-1 and SHA-256 digests. The time trial repeated them for a different file, and the mastery doubled them across two sets. It was routine, and it set the lane's habit.

## The solve

The work is choosing the right member and hashing its exact bytes. The solver reads the member the question names, then reports its basename, byte length and the three digests. These plain questions are handled by suffix handlers in `mfsolve.py`, which stayed in the pipeline as the fallback behind the later metadata engine.

The notes do not record how the original single was produced. The time trial and mastery were solved in the 4 October Claude Code session, when the notes say the score went "from 25 to 48 of 62 in one session".

The filename answer is the basename of the member that matches the question's stem. Later cumulative masteries let a global name search bleed one set's filename onto every set. The fix scoped the lookup to each set's own archive, and the first version of it broke this day, whose note has no id suffix.

Every answer comes from the bytes, never from the label.
