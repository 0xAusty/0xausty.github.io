+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Picture This"
date = 2026-10-04  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day04-picture-this"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 4 (2026-10-04), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-04-picture-this
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Reading JPEG frame size from the first start-of-frame segment, and answering width first even though the segment stores height first."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["metadata", "forensics", "jpeg"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 4 asked for the true dimensions of a named JPEG as WIDTHxHEIGHT. The photographs had been resized, renamed and shuffled, so the file name was no help. It was a small, clean technique and nothing went wrong.

## The solve

The solver in `mfsolve.py` walks the JPEG marker segments until it reaches the first start-of-frame marker, skipping the marker codes in that range that are not frame headers (DHT, JPG and DAC). It reads height and width from that segment and answers width by height. The time trial and mastery used the same handler on other files.

The notes do not name who solved the single, which the scoreboard puts at 11:09:24 on the release morning, with the time trial and mastery at 18:07:18 and 18:07:48 that evening. They do say the 4 October Claude Code session solved all the metadata time trials and masteries that day, and that all modes were correct by the 14 October backfill.

The gotcha is the order: the start-of-frame segment stores height before width, but the accepted spelling is width first. The agent's memory file confirms this as a solved example.

Swap the two numbers on the way out.
