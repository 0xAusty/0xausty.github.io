+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "The API Has Opinions"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-the-api-has-opinions"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "web" (Web Exploitation), web_no 14
#   gm_id web-exploitation-day-14-the-api-has-opinions
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Broken object and function-level authorisation: access was checked per field and action, and one action on the protected object was never locked down, found by sweeping the action matrix."

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

This was an object API whose authorisation was enforced per field and per action, with an inventory route that listed the routes, fields, actions and object ids. It is a broken object-level authorisation bug, and the weakness was one action nobody had locked down.

## The solve

A Claude Code subagent read the inventory first. Then it tried every action and field pairing on the protected object, starting with the actions that aren't a plain read, until one pairing returned the proof. Authorisation was applied per pairing, so an unusual action leaked what the obvious ones refused. That logic became `solve_bola` in `websolve.py`.

The pipeline's first classifier sent this day's two new web shapes down the generic admin path, and that failed. Dedicated branches went in ahead of the admin fallthrough. The proof also came back in a JSON evidence field, not as a token, so a scan for a token's shape would have missed it.

The 09:00 run started late because the laptop was asleep. The time trial was confirmed at 09:24:15 and mastery at 09:25:32 on 24 October.

The fix is to deny by default for every field and action pairing, not only the ones someone thought to test.
