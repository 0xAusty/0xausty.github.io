+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Go Fish"
date = 2026-10-04  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day04-go-fish"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 4 (2026-10-04), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-04-go-runtime-fingerprints
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Go binary added eight config fields to the cumulative bundle; the chatty runtime changed nothing, since the same config record was found and checked by CRC32."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "homebase"]

tools  = ["binsolve.py", "python"]
tags   = ["reverse-engineering", "go", "elf"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 4 grew the cumulative bundle to 32 fields: the 24 from Days 1 to 3 again, plus eight for a Go binary. Go's chatty runtime made no difference: it was the same config record as before, and the day was routine.

## The solve

The `binsolve.py` branch for Days 4 and 5 takes the format from the magic bytes, reports the architecture, and scans for the config magic, keeping the record whose CRC32 matches. That brought the single to 31 of 32 on 6 October.

The one open field was the Day 1 symbol list, which came from the event's Homebase AI (GPT-6 Luna) on 7 October. The agent then swept the single, time trial and mastery. The single went CORRECT at 11:00:55, the time trial at 11:02:28 and the mastery at 11:08:23.

Mastery sets could swap the ELF for a byte-patched Windows PE copy, so the config is read from raw bytes whatever the container.

The architecture had to be spelled *x86-64*, not *amd64* or *x86_64*.
