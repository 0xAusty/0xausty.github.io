+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Universal Appeal"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-universal-appeal"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-20-universal-appeal
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Universal Mach-O binaries need every CPU type listed, and only the grader's rejections revealed the element spelling it wanted."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["metaengine.py", "python"]
tags   = ["mach-o", "metadata", "forensics"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 20 asked for the set of CPU types in a macOS binary, as a JSON array. The carriers were thin images, universal (fat) binaries and static archives. The pipeline did not get the single, so Claude Code fixed it in session.

## The solve

The Mach-O parser had read only a thin image's header since 14 October. It was extended to list every CPU type in a carrier: one for a thin image, one per `fat_arch` entry for a universal binary (the fat header is always big-endian on disk), and one per Mach-O member of an `ar` archive, found by walking the 60-byte member headers. The answer is the distinct values, sorted.

The declared format said only "JSON array", so the element spelling came from rejections. An array of architecture names was rejected, and so was an array of raw integers. What the grader accepted was each CPU type as `0x` plus eight lowercase hex digits. The single was correct at 09:12:21, and the Time Trial and Mastery followed at 09:13:19 and 09:13:22.

Later that day the fix was made general: the guess function now returns the canonical render first and then a fan of alternative representations. Measured with a heal audit that treats every corpus field name as unseen, unattended recovery rose from 77.5% to 93.2%.

When the declared format leaves the element type open, the grader's rejections are the spec.
