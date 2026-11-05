+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Fetch Quest"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-fetch-quest"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "web" (Web Exploitation), web_no 15
#   gm_id web-exploitation-day-15-fetch-quest
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Server-side request forgery: a route that fetches a caller-supplied URL was pointed at an internal-only service that trusted loopback, which is fixed by egress allow-lists and real authentication."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "ssrf"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a textbook server-side request forgery. A feature route fetched an absolute URL on the server's behalf, and a second, internal-only service sat behind it, reachable only from the app's own loopback. The routine part was the bug class. The part to remember is that the internal service trusted anything that appeared to come from loopback.

## The solve

A parallel Claude Code subagent solved it. The idea was to make the fetch route request the internal service on the app's own port, so the source address check passed, and then read the proof from the response. The solver tries the container's own HTTP port first, then a short fallback list. That became `solve_ssrf` in `websolve.py`.

The first classifier labelled it as a generic admin challenge and failed, so a dedicated SSRF branch was added. As with the previous challenge that day, the proof arrived as a JSON evidence field rather than a token.

The time trial was correct at 09:25:16 and mastery at 09:25:48 on 24 October, on a morning when the cron had run late.

The fix is to restrict what the fetcher may reach, and to require authentication on internal services instead of trusting network position.
