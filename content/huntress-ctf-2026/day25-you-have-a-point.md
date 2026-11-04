+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "You Have a Point"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-you-have-a-point"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-25
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A code-point blob decoded by a strictly guarded step, plus a late fix for transposition chunks that fell below the known-plaintext confirmation threshold."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "autopilot"]

tools  = ["wusolve.py", "kpa.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["encoding"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 25's warmup asked for the slug hidden at the end of a blob of space-joined `U+XXXX` code points. The decode was easy. The interesting part was what the clock and the later replay did to the fix.

## The solve

The first pass at 09:00 missed. The agent (Claude Code) added a `codepoints` step to `wusolve.py` with a strict guard: every token must be `U+` followed by one to six hex digits, and surrogates or values above U+10FFFF are rejected, so the step cannot fire on ordinary text. The single was submitted with `fix.py --only` and was CORRECT by 09:07:38.

The Time Trial and Mastery were not run by hand. The supervisor hashes the solver files about every ten seconds and, on a change, re-attempts unresolved work. Three saves between 09:08:02 and 09:08:41 re-ran them without success; the save at 09:09:31 banked both, at 09:09:34 and 09:09:36. The notes do not record what changed between those saves.

That evening the preflight replay flagged the Mastery: with the learned cache cleared it solved 96 of 123 blobs. Chunks shrink as the Mastery grows, and a transposition chunk can fall under the six-character threshold that known-plaintext keying needs. The agent added a fallback that reorders the raw chunk against the fixed prefix, and the replay went to 123 of 123.

A strict guard keeps a new decoder from firing on text it was never meant for.
