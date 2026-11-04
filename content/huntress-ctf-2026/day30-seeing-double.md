+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Seeing Double"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-seeing-double"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-30-seeing-double
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Grouping zip members by identical SHA-256 content, answered as sorted basenames; the agent computed it straight from the archive and it was never folded into a parser."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["forensics", "diffing", "time-trial", "mastery"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The single asked for `identical_sha256_groups` from `cluster-001.zip`, as case-insensitive JSON: which members of the archive are byte-identical copies. The timed modes grew that to 35 and then 490 cumulative fields.

## The solve

Claude Code computed it directly from the zip. It grouped the members by the SHA-256 of their content and answered each group as member basenames, with the `artifacts/` prefix stripped, each group sorted and the groups sorted. It was never folded into a parser.

The agent's coordinating session solved metadata inline within about five minutes of release. The single was correct by 09:03:11 and the time trial by 09:04:05. The exact mastery time is not recorded; the supervisor's own mastery attempt was still unsolved at 09:04:49, so the inline submission landed shortly after. One earlier submission, at 09:02:42, was rejected, and its form is not recorded.

That morning's earlier fixes held: the first-pass report fired once, at 09:00:31, and listed only real misses.

The gotcha: basenames, not stored paths, and sort twice, within each group and then across groups.
