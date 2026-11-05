+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "D-Day"
date = 2026-10-11  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day11-d-day"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 11 (2026-10-11), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-11-d-collection-planner
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A D-language binary solved with no new code, then a self-inflicted 429 burst cost the time trial its only window, and a shared rate limiter fixed it."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["binsolve.py", "binmastery.py", "python", "Claude Code"]
tags   = ["reverse-engineering", "elf", "base64", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

This was a D-language ELF with the config as a base64 string literal, and 110 fields to answer. It was the first language the pipeline had never seen, and it needed no new code. The interesting part was what the automation did to itself.

## The solve

The Day 10 generic handler resolved all 110 fields in the 09:00 sweep, and the single came back CORRECT at 09:00:07. The time trial also resolved 110 of 110, but its submit got an HTTP 429: five lane processes were firing at the release and rate-limiting each other. The timed window is one-shot, so it expired. That day's retry rotation wasn't published either, so retry, practice and start on it all returned a stable 409, and the mastery stayed gated behind the time trial.

The fixes went in that morning. A token bucket in a lock-protected file is now shared by every lane, and a POST that gets a 429 waits for `Retry-After` and resends. A 429 is rejected before processing, so resending is safe; a 5xx stays ambiguous and is never blindly resent. A standalone watcher with no Claude in the loop then polled both modes every 5 minutes and recovered them. The time trial went CORRECT at 18:32:48 on 13 October and the mastery at 23:28:18 that night.

The solver had every answer right, and its own lane processes locked it out.
