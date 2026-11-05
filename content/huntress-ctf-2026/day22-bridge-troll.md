+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Bridge Troll"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-bridge-troll"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-22-managed-native-bridge
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Renamed two-build members in the evidence bundle sank the Day 22 bank submit, and a cold subagent took 16 minutes to fix it."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "Claude Code"]
tags   = ["reverse-engineering", "dotnet"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 22 asked 264 fields, the 252 from earlier days plus 12 new ones about a managed .NET assembly bridged to native code. The new questions included the CLR metadata version string. What tripped the pipeline was a rename: the bundle's two-build members went from `dNN--variant-NNN-<tag>.ext` to `dNN--sample-<tag>.ext`.

## The solve

The pipeline resolved only 241 of 264 at release. The renamed members missed the tag regex in `binsolve.py`, so the per-tag fields for Days 15, 16 and 21 fell back to closest-name guesses. One wrong field rejects the whole bank submit, and it came back incorrect.

The miss went to a cold general-purpose subagent spawned by Claude Code. It took 16.3 minutes and became the critical path. The fix was a broader tag regex applied only to the fields actually asked, a reader for the CLR version string at the `BSJB` signature plus 16 bytes, and a correction to positional SHA-256 fields. Those fields follow ZIP central-directory order and count the text members too. The single was confirmed at 09:15:02, the time trial at 09:15:23 and the mastery at 09:15:40.

The cost of the cold start produced a standing rule in the notes: web misses go to parallel subagents, while a deterministic miss is solved inline by the coordinating session.

A closest-name guess is still a guess, and one of them can sink a whole submit.
