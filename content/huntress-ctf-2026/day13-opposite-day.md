+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Opposite Day"
date = 2026-10-13  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day13-opposite-day"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 13 (2026-10-13), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-13
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The Atbash chunk looks like letters when left undecoded, so a slug-shaped reading proved nothing; the mastery's release run garbled many blobs and did not submit."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py", "daily.py"]
tags   = ["encoding", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 13 asked the usual warmups question over blobs of thirteen chunks, and the clue pointed to Atbash. The single and time trial were routine, but the mastery went wrong.

## The solve

Atbash was in the first decoder, so the single and time trial were CORRECT at 09:00:06 and 09:00:08. The mastery's release run produced shape-valid slugs that were not dictionary words for several blobs, and no reading at all for 11 of the 63. Many of the rest were garbled, with slug words still reversed or Atbash-encoded. The pipeline did not submit it.

The notes say only that the mastery was then solved outside the repo, with no solver change committed. They don't say who solved it. The only time in my notes is a re-run from a 16 October sweep, and the scoreboard puts the first solve at 09:17:01 that morning. The autopilot label covers the single and time trial only.

The general fix came the next morning with Day 14: score slug words against the dictionary during the search, and refuse the cheapest-shape fallback.

Letter-substitution chunks still look like letters when left undecoded, so a slug-shaped reading proves nothing.
