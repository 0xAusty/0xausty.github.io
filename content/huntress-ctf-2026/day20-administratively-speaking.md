+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Administratively Speaking"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-administratively-speaking"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "web" (Web Exploitation), web_no 5
#   gm_id web-exploitation-day-05-administratively-speaking
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Broken access control by forced browsing: a disclosed route returned the proof as JSON with no authorisation, protected only by not being linked."

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

The simplest of the web lane's early challenges, and a useful contrast with the others. The target was a Django-style app with a staff-only feature route, and the weakness was **broken access control**: the door had a sign on it and no lock.

## The solve

A clues endpoint disclosed the route, and a plain GET of it returned the proof in a JSON response, because nothing enforced authorisation there. That is forced browsing: the route was protected only by being unadvertised.

The notes record the Day 20 web misses as fixed in the coding-agent session and folded into `websolve.py` as `solve_admin`. The one gotcha repeated across the lane is that on many classes the proof is a JSON `evidence` field rather than a bare token with the usual proof prefix, so a scan for the token shape would miss it. On release morning the time trial was confirmed at 09:18:56 and mastery at 09:19:04.

The defence is to enforce authorisation on every route on the server, since a hidden URL is not a control.
