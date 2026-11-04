+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Looks Can Be Deceiving"
date = 2026-10-02  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day02-looks-can-be-deceiving"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 2 (2026-10-02), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-02-looks-can-be-deceiving
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The answer id names a member inside the archive, so the first sixteen bytes to report are the inner file's, not the outer zip's."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["metadata", "forensics", "zip"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 2 asked for one value per mode: the first sixteen bytes of a named member, as lowercase hexadecimal. The members carried extensions that might not match their bytes, which is the prompt's "deliberate disguise". The interesting part was which bytes counted.

## The solve

The answer id names a file inside the archive. The rule in `mfsolve.py` is to read that member, not the outer zip, and hex-encode its first 16 bytes in lowercase with no prefix. The 2 October handoff records the single's lesson: the accepted answer came from the named inner file.

During the time trial, an analyst read the first 16 bytes of the outer zip instead. That was never submitted. The time trial deadlines were only about 5 to 8 seconds after start, and the attempts expired while analysis was still running. The handoff's rule afterwards was not to start a timer until the analysis is ready.

The notes do not say who produced the accepted single. The time trial and mastery were solved in the 4 October Claude Code session, which is why the label reads agent.

The convention "lowercase hex, no 0x" belongs to this field only. Later hex integer fields were graded 0x-prefixed and padded to the type width.
