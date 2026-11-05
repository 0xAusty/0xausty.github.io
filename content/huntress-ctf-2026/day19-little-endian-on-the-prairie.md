+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Little Endian on the Prairie"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-little-endian-on-the-prairie"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-19-little-endian-on-the-prairie
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An e_machine field the parser did not expose was answered by the closest-name guess in all three modes, and the live solve hid an offline regression for a day."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaengine.py", "python"]
tags   = ["forensics", "elf", "metadata"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 19 asked for the ELF machine type as a four-digit hex string in the single, with 24 fields in the Time Trial and 120 in Mastery. It looked routine, and it was: the single was correct at 09:00:05, the time trial at 09:00:08 and the mastery at 09:00:13. The trouble surfaced the next morning.

## The solve

At 09:00 the engine had no field named `e_machine`, because the ELF parser exposed the value only as `machine`. The guess path offered the parsed machine value, rendered at the field's u16 width (`0x` plus four hex digits), as its first suspect. It was accepted on the first submit in every mode, with no human in the loop.

The live guess hid a gap. The offline replay uses the deterministic solver, which still returned nothing for this field, so every replay after Day 19 had regressed. A preflight failure at 08:26 the next day exposed it, behind three expected web failures that a truncated output list had been hiding. The fix folded the spec names (`e_*` and `ei_*`) into `parse_elf`, with the u16 suffix on the field name driving the hex width. The preflight also stopped truncating its list.

A solve that only the live guess path can produce will not show up in an offline replay, and a pre-commit gate limited to changed files missed it because that commit touched no metadata solver file.
