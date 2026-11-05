+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Campaign Trail"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-campaign-trail"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-30-multi-binary-campaign
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A multi-binary campaign day: Neko bytecode members carried an HGRF record with the same layout as HCFG, so the work was extending config-record handling, not new reverse engineering."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["reverse-engineering", "xor", "crc32"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 30 asked for the formats of a loader, a library and a config-capsule member, plus the campaign config under two spellings: plain keys and a nested `graph.config.*` form. It was the familiar record extraction in an unfamiliar container, Neko VM bytecode.

## The solve

The Neko members carry an **HGRF** record: the same 12-byte XOR-plus-CRC layout as HCFG, but the JSON is a campaign graph with the config nested under a `config` key. The pipeline banked 409 of 420 fields at release. The escalator was kicked at 09:00:31, and its headless Claude hit a session limit at 09:07:26. The single and time trial were already correct by then, at 09:05:51 and 09:06:39, and the coordinating session solved the mastery inline at 09:12:13. HGRF went into the config-record magics, the Neko magic was recognised, and `loader.n`, `library.n` and `config.n` were mapped to the three roles. Nested config is flattened so both spellings answer, and flat keys win over nested ones.

Neko's format token is `neko_bytecode`, and VM bytecode has no machine field. The single was correct at 09:05:51 and the time trial at 09:06:39. The mastery's first passes were 126 and then 70 fields short before the final fold, and it was correct at 09:12:13.

A new container usually hides the same record format.
