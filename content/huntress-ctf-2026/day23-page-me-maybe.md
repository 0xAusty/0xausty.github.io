+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Page Me Maybe"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-page-me-maybe"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-23-page-me-maybe
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A SQLite header parser built in advance answered the page-size question within seconds, with one automatic heal in the cumulative Time Trial."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaengine.py", "python"]
tags   = ["sqlite", "metadata", "forensics"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 23 asked for the page size of a SQLite database, as an integer. It was routine. The bench file recorded release-to-correct times of 4.4 s for the single, 9.3 s for the Time Trial and 12.6 s for Mastery.

## The solve

The SQLite header parser had been built on 14 October. It reads the big-endian u16 page size at offset 16 of the database header, where a stored 1 means 65536. The engine stripped the trailing type word `bytes` from `page_size_bytes` to reach the `page_size` key. Nothing else was needed.

The Time Trial was cumulative, so it also carried older fields. The ZIP member-names field from Day 8 was rejected in central-directory order and was healed automatically to an alphabetically sorted array.

The day's long tail was in other lanes. A script Time Trial and Mastery were only recovered at 10:33, while the metadata lane had banked its modes in 13 seconds.

This field later made up about 200 of the "latent" cases in a generality audit. The agent investigated and judged them not a real miss risk, because the parser already emits the value and the event's field naming is stable.

A cumulative challenge re-tests the old fields too, and the heal path for them worked here.
