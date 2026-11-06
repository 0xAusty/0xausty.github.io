+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Portable Deception"
date = 2026-10-06  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day06-portable-deception"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 6 (2026-10-06), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-06-portable-deception
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A PDF version question where only the header counts, and where two of the project's notes credited the 09:00 sweep with a solve the log says it never made."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["metadata", "forensics", "pdf"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 6 asked for the PDF header version of a named document. The bundle mixed real PDFs, renamed impostors and several declared versions. The answer is the version in the `%PDF-x.y` header only, and the literal word none when the member is not a PDF.

## The solve

The handler is the `pdf-header-version` suffix in `mfsolve.py`. The versions rotated between 1.4 and 1.7 across variants, so nothing could be hard-coded. The later metadata engine also exposes the catalog's own /Version entry separately, which this question did not want.

Two of the project's notes, both written in agent sessions, say the 09:00 sweep solved Day 6. The supervisor's log says otherwise: it fetched the single, produced no answer and reported it unsolved, with the time trial and mastery not attempted. The new handler reached the repo in a commit co-authored by Claude on 7 October. The handoff committed with it reports all three modes correct. The scoreboard puts them at 09:03:23, 09:05:08 and 09:05:16 on 6 October, the release morning.

Trust the log over the summary notes.
