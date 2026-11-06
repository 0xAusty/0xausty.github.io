+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Stored for Later"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-stored-for-later"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "web" (Web Exploitation), web_no 7
#   gm_id web-exploitation-day-07-stored-xss
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Stored XSS that only fires when an authenticated moderator bot views the note, so the solver plants the note, waits and polls for the exfiltrated data."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "xss"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a guestbook that renders the message field raw, with a moderator-only data route and a reviewer bot that visits the notes. Single and Time Trial asked for one proof field, and Mastery bundled it with earlier web types. The wait was more interesting than the injection.

## The solve

The bug is **stored XSS**: the note body is not escaped, so script in it runs for whoever views the page. The reviewer bot is logged in and the script runs same-origin, so it can read the moderator-only route that an outsider cannot. It then posts what it read back as a public note where the solver can see it.

The agent (Claude Code) added `solve_stored_xss` to `websolve.py` in the parallel web-days run. The payload does nothing until the bot arrives, under 15 seconds by the notes, so the solver waits and polls the notes above its own. A later fix added a second branch for a variant that delivers the data through a per-note receipt route instead of a re-posted note. The Time Trial was confirmed at 09:21:04 on release day, the latest of that day's three web times, because the bot wait sits on the critical path.

The fix is output encoding on the message field, and keeping privileged routes out of reach of script in a page a reviewer opens. The gotcha was patience: the note looks inert until the bot opens it.
