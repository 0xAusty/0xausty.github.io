+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Hive Mind"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-hive-mind"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-25-hive-mind
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A field name no parser exposed at release was answered by the closest-name guess path, then folded into the registry hive parser the same morning."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaextra.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["forensics", "registry"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The single asked for one registry field, the name of a hive's root key, from a file called `hive-001.hiv`. The timed modes widened that to 30 and then 270 cumulative fields across several hives, one of them planted. The ask was routine. The way it was answered was not.

## The solve

No parser field had that name at 09:00. The pipeline's closest-name guess path, built for exactly this, offered three suspects: the hive's root key name, the file name embedded in the hive header, and a lowercased variant. The first was correct, and the three modes were accepted at 09:00:04, 09:00:09 and 09:00:16 with nobody touching anything.

Later that morning `metaextra.parse_regf` began exposing `hive_root_name`, read straight from the root `nk` cell, so the field now solves offline. That mattered for a dull reason: a live-only guess shows up as a regression in the replay gate until it is folded into the parser, and it did in the Day 25 preflight.

The header's embedded file name was only ever the second-ranked suspect. The root key's own name is the answer.
