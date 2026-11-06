+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Stay in Your Directory"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-stay-in-your-directory"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "web" (Web Exploitation), web_no 4
#   gm_id web-exploitation-day-04-lfi
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Local file inclusion through a viewer page that joined a request parameter onto a pages directory with no traversal filter, in a mastery bundle that mixed two task types."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "lfi"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a **local file inclusion** challenge. A PHP viewer page included a file from a pages directory based on a request parameter, and the whole challenge was the missing check on `../` sequences. The mastery mode was a two-target bundle, a backup task plus this one.

## The solve

The home page offered a sample link that exposed the endpoint and parameter name. A viewer that simply joins the parameter onto a directory can be walked out of that directory to a file elsewhere in the container, and the proof lived in a fixed objective file.

The Day 20 web misses were fixed in the coding-agent session and folded into `websolve.py` as `solve_lfi`. Because mastery mixes types, `classify()` dispatches each target on its own, and the endpoint and parameter are discovered from the page rather than hardcoded. On release morning the time trial was confirmed at 09:18:37 and mastery at 09:21:26.

The defence is to resolve the final path and check it stays inside the intended directory, or to map names to files from an allow-list.
