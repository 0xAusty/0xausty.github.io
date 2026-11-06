+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Family Resemblance"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-family-resemblance"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-28-family-clustering
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A 392-field clustering day: the first fold handled only ELF, but the time trial and mastery bundles shipped PE variants and needed a format-aware second pass."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["reverse-engineering", "elf", "pe", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The generator went back through the previous 27 days of evidence and asked new structural facts about the earlier members: family counts, an ordered-set SHA-256 and the formats and config of three new role members. It was routine record-reading with one trap: the questions defined their own counts and orderings.

## The solve

The pipeline banked 362 of 392 fields at release, with 30 unresolved: symbol counts, a section count, a vtable symbol, the d28 role formats and config. Claude Code handed the miss to a cold general-purpose subagent, which took about 24 minutes over two rounds to fold the missing pieces into `binsolve.py`.

The first fold was ELF-only, but the time trial and mastery bundles shipped PE variants of earlier members. The time trial stuck at 391 of 392 on a section count, and the mastery lacked the vtable symbol in five sets. The final fold made the pass format-aware, with ELF section headers against the COFF section count and a COFF symbol-table parser for the vtable symbol. It also fixed a bug where one field could take a sibling's hash. The supervisor hot-reloaded each edit, and the single was correct at 09:23:06, the time trial at 09:43:21 and the mastery at 09:53:20.

Check which container format the timed bundles ship before trusting a fold built on the single.
