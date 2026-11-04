+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Fraternal Twins"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-fraternal-twins"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-29-variant-diffing
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A variant-diffing day that looked like binary analysis but came down to picking the right member by the question's own basename hint, format-aware across ELF and PE."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["reverse-engineering", "diffing", "elf", "pe"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 29 asked for fields about two builds of one source, an -O3 and an -O0 build, under role-prefixed names: format, machine and config for each. The interesting part was small. The solve was member selection, not analysis.

## The solve

The pipeline banked 400 of 406 fields at release. The six misses were the formats of both roles and the config of the -O3 build. Claude Code fixed it in session: `_fill_variant_roles` in `binsolve.py` now picks each role's member from the question's own "basename ends" hint, falling back to the O3/O0 convention, and answers from that member. The fill is format-aware, reading ELF `e_machine` or the PE COFF machine field, and matches by stem so a PE variant still resolves.

The mastery pass was 78 fields short at 09:16:25: the same six role fields in all 13 sets. The supervisor gave up after three passes without progress, and the log first shows the mastery correct at 09:17:59. The single was correct by 09:14:57 and the time trial by 09:16:25.

The notes don't say whether the day's own role members shipped as PE.

Let the question name the member instead of assuming a fixed filename.
