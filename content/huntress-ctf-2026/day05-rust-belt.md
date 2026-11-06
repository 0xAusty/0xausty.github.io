+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Rust Belt"
date = 2026-10-05  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day05-rust-belt"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 5 (2026-10-05), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-05-rust-runtime-shapes
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Rust binary shipped a decoy config record with a bad checksum next to the real one, so the CRC32 check was the entire defence."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "homebase"]

tools  = ["binsolve.py", "python"]
tags   = ["reverse-engineering", "rust", "elf", "crc32"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 5 took the cumulative bundle to 40 fields, with eight new ones for a Rust binary. The format was the familiar config record, and the interesting part was a trap: the Rust build carries a second copy with a bad CRC32 beside the real one.

## The solve

At the 5 October release the supervisor logged no solver for the binary lane, so it was skipped. Claude Code's `binsolve.py` handled it on 6 October with the same branch as Go. It searches for every config magic and keeps the record whose CRC32 over the decoded payload matches the header, which rejects the decoy. That reached 39 of 40.

The last field, the Day 1 symbol list, came from the event's Homebase AI (GPT-6 Luna) on 7 October, and the agent then swept the single, time trial and mastery. The single went CORRECT at 11:00:56, the time trial at 11:02:32 and the mastery at 11:06:46.

A plain find on the magic returns the decoy first, so validate the checksum, not the magic.
