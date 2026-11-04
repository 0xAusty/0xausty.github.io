+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Where It All Began"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-where-it-all-began"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-28-where-it-all-began
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A disk-image partition-order question needed a new parser, written in session, and saving it let the supervisor's hot-reload bank the timed modes within seconds."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "autopilot"]

tools  = ["metaengine.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The single asked for `partition_start_lba_sequence` from `disk-001.img`, as JSON: the starting sector of every partition, in order. The timed modes grew that to 33 and then 396 cumulative fields. No parser handled disk images yet, so this was the day the pipeline missed first and had to be fixed.

## The solve

Claude Code wrote a new disk-image parser, `metaengine.parse_disk`. If an `EFI PART` header follows the protective MBR (sector size 512 or 4096) it reads GPT. Otherwise it reads the legacy MBR's primary entries in on-disk order and splices in each extended container's EBR chain, where a logical partition's start is the EBR's LBA plus its relative offset. The answer is that list of starting LBAs as stored, not sorted.

The agent submitted the single from the session, which was correct by 09:11:31. Saving the parser triggered the supervisor's hot-reload, which then banked the time trial and mastery by about 09:15. Five of that day's lanes needed new shapes.

Recovery started late. About 11 minutes were lost to an idle gap because the recovery launch waited until I noticed the misses.

The gotcha: keep the table's order, including logical partitions reached through the EBR chain.
