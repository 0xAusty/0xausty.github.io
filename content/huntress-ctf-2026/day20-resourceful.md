+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Resourceful"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-resourceful"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-20-resources-and-overlays
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 20 had one missed field with three plausible sizes in one RS20 resource overlay, and the miss led to a fallback that offers every overlay integer as a candidate."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py"]
tags   = ["reverse-engineering", "xor", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 20 added one new field kind, the size of the HCFG resource inside an `RS20` overlay. Everything else was routine: 239 of 240 fields were banked at release.

## The solve

The overlay is a resource layout, not Day 19's packed one: a magic, a version, a size word at +8, a trailer-name length, a 32-byte SHA-256, then the HCFG resource (a 12-byte header plus an XOR'd payload) and a plaintext trailer. That gives three plausible sizes: the whole overlay, the HCFG payload alone, and the header word at +8, which covers the HCFG header plus its payload. The field wanted the last one.

Claude Code solved it in session and added `binsolve._rs20_hcfg_resource_size`. The single was correct at 09:06:51, the time trial at 09:07:01 and the mastery at 09:07:14.

The miss was a parser gap that the heal step couldn't reach. Two days later the agent added `_overlay_int_candidates`, which offers every aligned little-endian integer in a recognised overlay header as a suspect, since the binary lane had missed almost every recent day on a structural twist.

When one overlay carries several sizes, read the field name against the header layout before guessing.
