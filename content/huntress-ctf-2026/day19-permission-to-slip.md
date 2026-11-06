+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Permission to Slip"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-permission-to-slip"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "web" (Web Exploitation), web_no 2
#   gm_id web-exploitation-day-02-idor
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A textbook IDOR: the object API checked no owner, and the app's own activity feed leaked the id of someone else's row, so nothing needed guessing."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "idor"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This one was a clean **insecure direct object reference**, also called broken object-level authorisation. The target was a small object-style API with an activity feed, and the question was the same single proof as its siblings.

## The solve

The activity feed referenced a row owned by someone else, which leaked a valid identifier, so no id guessing was needed. Asking the object API for that row worked, because it enforced no owner check.

An AI coding session solved it live on 19 October, then folded it into `solve_idor` in `websolve.py` as a coding-agent fix. The solver reads the API template and the feed from the pages themselves, because routes were randomised per attempt. The time trial was confirmed at 09:49:49 that morning.

The defence is to check ownership on the server for every object request, and to treat an identifier in a feed as public the moment it is shown.
