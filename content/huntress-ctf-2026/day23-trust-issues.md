+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Trust Issues"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-trust-issues"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-23-anti-analysis-recognition
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 23's anti-analysis recognition set on a .NET assembly needed no intervention: the solver banked all three modes within about a minute."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["binsolve.py"]
tags   = ["reverse-engineering", "dotnet"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 23 asked 276 fields: everything from Days 1 to 22 plus 12 about anti-analysis recognition in a .NET managed assembly that carries environment and clock checks. The notes say nothing about what the new questions looked like. This one was routine.

## The solve

The pipeline solved it unattended. The single and the time trial each resolved 276 of 276, and the mastery resolved 1,932 of 1,932 over seven sets. The log has the mastery fetch at 9.0 seconds and the solve at 29.1 seconds, and it was the day's critical path at about a minute from release. The single was confirmed at 09:00:09, the time trial at 09:00:18 and the mastery at 09:00:59.

Day 28 later re-asked two of the Day 23 fields. One was the CLI runtime version. The other was whether the assembly contains a decoy branch, which `binsolve.py` answers by looking for the word *decoy* in the member as Latin-1 or UTF-16LE text.

Nothing here needed a fix. The notes have no more to say about this day than that.
