+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Chunk Norris"
date = 2026-10-05  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day05-chunk-norris"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 5 (2026-10-05), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-05-chunk-norris
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A PNG whose prompt hinted at a hidden chunk but whose question only asked for the declared IHDR geometry; the first sweep had no handler."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["metadata", "forensics", "png"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 5 asked for the width and height of a named PNG, as WxH. The prompt talked about an unexpected structural passenger among the chunks, but the question only wanted the declared header geometry. The interesting part was operational: there was no PNG handler yet.

## The solve

The handler in `mfsolve.py` reads the width and height from the IHDR chunk that follows the 8-byte PNG signature. The later metadata engine also walks every chunk and records chunk types, text chunks and trailing bytes after IEND, though this question needed none of that.

The challenge was released before 9 am, and the supervisor's pass at 09:05 on 5 October logged "NOT SUBMITTING (unmapped)". The single was left unsolved, and the time trial and mastery were not attempted. The IHDR handler first appears in a commit co-authored by Claude at 11:19 that day, and the handoff committed with it lists metadata as solved for all modes. So the answers came from an in-session fix between those two points, which is why the label reads agent. The notes do not narrate that fix; the scoreboard puts the three modes correct at 09:06:57, 09:06:59 and 09:07:01.

The answer is the header value, not a rendered size.
