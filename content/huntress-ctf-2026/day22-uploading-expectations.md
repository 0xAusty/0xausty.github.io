+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Uploading Expectations"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-uploading-expectations"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "web" (Web Exploitation), web_no 10
#   gm_id web-exploitation-day-10-uploading-expectations
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An upload filter that accepts anything, chained to a renderer that evaluates template expressions in served HTML, turns a file upload into data disclosure."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "file-upload", "ssti"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was an upload form with weak validation and a render route that serves stored files by extension. Single and Time Trial asked for one proof field, and Mastery bundled it with earlier web types. It is a two-link chain, which makes it more interesting than a plain upload bug.

## The solve

The first weakness is **unrestricted file upload**: the "bouncer" accepts anything. The second is **server-side template evaluation**: the render route serves a file by its stored extension, and for an HTML preview it evaluates template fields in the content. So a note uploaded as HTML can reference the objective's field, and fetching its rendered copy returns the value the field expands to.

The agent wrote `solve_upload` in `websolve.py`, folded in with the CSRF solver. It uploads an HTML note that references the field, fetches the rendered copy and reads the result. The Time Trial was confirmed at 09:07:57 on release day.

The fixes are to allow-list file types and check content, to store uploads where they are never rendered, and never to run user-supplied files through a template engine. The gotcha was that neither flaw alone gets the proof.
