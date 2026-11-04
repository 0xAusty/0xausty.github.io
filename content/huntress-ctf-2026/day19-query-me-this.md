+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Query Me This"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-query-me-this"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "web" (Web Exploitation), web_no 3
#   gm_id web-exploitation-day-03-sqli
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Boolean-blind SQL injection against a search box, where the real constraint was the target's short lifetime, so the extractor ran its per-character search in parallel."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "sqli", "sqlite"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was the one early web challenge with real engineering in the solver. The target was a search box over a SQLite-backed table, and the proof was the summary of a hidden article. The vulnerability class is **SQL injection**, and the output was blind: the page only behaved differently for true and false conditions.

## The solve

That left boolean-blind extraction: ask a yes/no question about one character of the hidden value, and binary-search each position from the page's truthy or falsy response. Done one request at a time that is slow, and the live target expired after a short time with nothing to replay offline.

So `solve_sqli` in `websolve.py` keeps the search lean and spreads it across worker threads, and the lane runner reconnects once if a pass comes back incomplete. The notes record it as solved live in an AI coding session on 19 October and then folded into the solver by the coding agent, with the time trial confirmed at 16:58:58.

The defence is parameterised queries. The gotcha was the clock, not the injection.
