+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Main Character Energy"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-main-character-energy"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-22-main-character-energy
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A JAR parser written eight days earlier answered the Main-Class question on release, so the pipeline solved it without help."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaextra.py", "python"]
tags   = ["java", "metadata", "forensics"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 22 asked for the main class of a Java archive, as exact text. The prompt warned that manifests disagree with launchers, but the question was about the manifest, and it was routine. All three modes were correct by 09:00:32.

## The solve

The JAR parser (`parse_jar` in `metaextra.py`) had been added on 14 October, in anticipation of this format. It reads `META-INF/MANIFEST.MF`, unfolds the continuation lines and exposes each header in snake case, so `Main-Class` resolves as `main_class`. The manifest value was accepted as declared, and the pipeline did the whole day without a human or an agent.

What slowed the day was elsewhere. A cold binary subagent took 16.3 minutes, which produced a rule: solve deterministic misses inline, and send only web misses to agents.

Covering a format before the event asks for it is the cheapest way to win a release-time race.
