+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Back Up a Minute"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-back-up-a-minute"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "web" (Web Exploitation), web_no 1
#   gm_id web-exploitation-day-01-backup-exposure
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine exposed-backup challenge: robots.txt pointed at a forgotten directory, and the proof sat in a backup file under it, found by a solver that discovers routes live."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was one of three web challenges that appeared with no release timer, which started the sixth lane from zero on the board. It asked for a single proof from a live target, and it was routine: the vulnerability is **information disclosure through a leftover backup file**.

## The solve

The reasoning is the usual reconnaissance order. `robots.txt` lists paths the owner would rather crawlers skipped, and one of them was a directory the deploy had forgotten to clean up. Listing it showed a `.bak` file, and the proof was inside.

The notes record it as worked through live in an AI coding session on 19 October, then folded into `solve_backup` in `websolve.py` as a coding-agent fix, with the time trial confirmed at 09:42:39 that morning. The app name, routes and parameter names were randomised on every attempt, so the solver discovers them from the target instead of hardcoding anything.

The fix is housekeeping: keep backups and editor leftovers out of the web root, and don't treat `robots.txt` as access control, because it is a map for anyone who reads it.
