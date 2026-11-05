+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Session Impression"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-session-impression"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "web" (Web Exploitation), web_no 8
#   gm_id web-exploitation-day-08-session-impression
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Session fixation on a resume site: the server never rotates the session id on login, so a planted id becomes the reviewer's privileged session."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "session-fixation"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a "Resume Room" site with a landing route that accepts a session id and a second route gated on the session. Single and Time Trial asked for one proof field, and Mastery bundled it with earlier web types.

## The solve

The bug is **session fixation**. The server takes the session id from a request parameter and does not issue a new one when a user authenticates. It had also pre-authenticated a reviewer against the id the challenge disclosed. So the solver only has to get that id set as its own session, then read the gated route with the resulting cookie, which is now privileged.

The agent wrote `solve_session` in `websolve.py` as part of the three-subagent run over web days 6 to 8. It plants the disclosed id through the landing route and requests the gated route with the cookie. The Time Trial was confirmed at 09:18:55 on release day.

The fix is to rotate the session id on every privilege change and to refuse ids the client supplied. The gotcha was how little there was: no cracking and no guessing, just a server trusting an id it should have issued itself.
