+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Template Temper"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-template-temper"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "web" (Web Exploitation), web_no 11
#   gm_id web-exploitation-day-11-template-temper
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Server-side template injection solved live by a subagent and never folded into the solver, so the notes record the technique and the times, not the steps."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = []
tags   = ["web-exploitation", "ssti"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a site whose template engine evaluates expressions in user-controlled input. Single and Time Trial asked for one proof field, and Mastery was a three-target bundle. The notes for this one are thin, so this note stays short.

## The solve

The bug class is **server-side template injection**. The usual approach is to confirm it first with an expression that can only be evaluated on the server, such as simple arithmetic, and only then reach for the engine's context to read the proof. The notes describe that technique, not the exact steps taken here.

What they do record is who and how. `websolve.py` has a generic `solve_ssti`, but this challenge was not added to its list of known challenges. A subagent in the session solved it live against the game master, so there is no committed solver for it. Single, Time Trial and Mastery were confirmed at 09:10:29, 09:10:41 and 09:10:57 on release day.

The fix is never to build a template from user input; pass user data in only as a variable. The gotcha is a process one: a one-off live solve leaves no reusable code behind.
