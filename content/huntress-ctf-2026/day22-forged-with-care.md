+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Forged With Care"
date = 2026-10-22  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day22-forged-with-care"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 22 (2026-10-22), lane "web" (Web Exploitation), web_no 9
#   gm_id web-exploitation-day-09-forged-with-care
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A CSRF token that only echoes the session cookie protects nothing, and the grader wanted the state change to arrive looking cross-site."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "csrf"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was an ASP.NET app with a preferences page. The state-changing route accepted GET, and the page offered an external destination. Single and Time Trial asked for one proof field, and Mastery bundled it with earlier web types. The twist is that the anti-CSRF token was decorative.

## The solve

The bug is **cross-site request forgery**. The token just echoes the session cookie, so anyone who can read the page can read the token, and it defends nothing. The server only granted the proof when it saw the change arrive from another site.

The agent folded `solve_csrf` into `websolve.py`, in the same commit as the next challenge. The solver reads the token and the external destination off the preferences page, then repeats the state-changing request with Referer and Origin headers pointing off-site. That flips the server's cross-site check, and the evidence shows in the response. The Time Trial was confirmed at 09:04:17 on release day. Day 22 as a whole ran slowly only because of a cold binary subagent, not the web pair.

The defence is a real anti-forgery token that cannot be derived from the cookie, SameSite cookies, and never changing state on GET. The gotcha was that the grader judged the origin headers, not the token.
