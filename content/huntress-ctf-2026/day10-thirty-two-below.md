+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Thirty-Two Below"
date = 2026-10-10  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day10-thirty-two-below"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 10 (2026-10-10), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-10
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Base32 was already supported, but a correct decode was rejected because the slug word was missing from the system dictionary, so the gate fell back to the cheapest unique reading."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["wusolve.py", "timed.py", "daily.py", "claude-code"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

A Base32 blob ("smaller alphabet" in the prompt), with the usual warmups question. The decoder already handled Base32, so the bug was in the dictionary check.

## The solve

The supervisor solved the single and the Time Trial at release; they were CORRECT at 09:00:04 and 09:00:06. The 48-blob mastery was left unsolved: the dictionary gate in `wusolve.py` rejected a correct decode because the real slug word wasn't in the system word list, which left one blob of 48 unanswered, so nothing was submitted. Timers had also come back after two untimed days, and a serial solve overran the window of about 13s.

Claude Code fixed it: when the dictionary gate yields nothing, fall back to the strictly cheapest reading (one standard encoding per chunk) and accept it only if that minimum is unique, refusing ties. A process-parallel solve and a single submit fit the window. The mastery was CORRECT at 09:12:28, before the 09:15:41 commit, but the notes don't say whether the submit came before or after the fix.

That same fallback later accepted gibberish on Day 14.
