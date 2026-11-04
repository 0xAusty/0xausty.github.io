+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Spot the Difference"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-spot-the-difference"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-24-patch-diffing
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Patch diffing on two Java jars: the config sat inside deflated class files, so a raw byte scan found nothing and the agent had to decode them."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "Claude Code", "python"]
tags   = ["reverse-engineering", "java", "diffing"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 24 asked 288 fields. The 12 new ones covered patch diffing: a shared config common to both builds, and a separate set of corrected-config fields taken from the fixed jar. The bundle held a vulnerable jar and a `corrected.jar` twin, each carrying a config blob inside a class file.

## The solve

The laptop was off at 09:00. The systemd timer caught up on wake, and the supervisor saw the release at 09:14:31. By then 280 of 288 fields resolved, and the eight misses were exactly the new config fields.

The agent fixed it in session. Jar entries are deflated, so a raw byte scan never sees the config. `_fill_config_from_members` now decodes the jars first. It takes the corrected-config fields from the member whose name ends in `corrected.<ext>`. The two configs are byte-equal, so the plain config is whichever role member turns up first.

The single, time trial and mastery were confirmed by 09:25. The time trial and mastery had shown "not attempted" until the single passed, because one missed single blocks three modes. Day 28 later re-asked the vulnerable-config fields.

Compressed containers hide things from a raw byte scan, and a late start made this miss expensive.
