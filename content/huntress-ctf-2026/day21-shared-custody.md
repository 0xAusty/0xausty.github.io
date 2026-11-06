+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Shared Custody"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-shared-custody"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-21-shared-library-boundaries
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "On Day 21 the loader carried no config; it lived in a sibling plugin member, so the fix was a scan scoped to the day's own members."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py"]
tags   = ["reverse-engineering", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 21 was about shared-library boundaries. The evidence held a loader and a sibling `plugin.cmxs` member, and the HCFG config lived in the plugin, not the loader. Routine otherwise: 248 of 252 fields were banked at release.

## The solve

The four misses were the config's campaign, domain, mutex and URL fields, which the solver looked for in the loader and did not find. Claude Code fixed it in session with `binsolve._fill_config_from_members`, a day-level pass that scans that day's own `d21--` members for the one CRC-valid HCFG.

The scan is scoped to the day's members on purpose. The cumulative bundle also holds every earlier day's configs, and an unscoped search could pick one of those by mistake.

The single was correct at 09:04:34, the time trial at 09:08:11 and the mastery at 09:08:19.

A small follow-up: on Day 22 the members were renamed with a sample tag, and the plugin-tagged Day 21 fields broke for a day.

If the loader has no config, look at what it loads.
