+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Reflect Upon This"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-reflect-upon-this"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "web" (Web Exploitation), web_no 6
#   gm_id web-exploitation-day-06-reflect-upon-this
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A callback route that released the proof only when a disclosed nonce and a Referer pointing at the reflection route arrived together, solvable with plain HTTP and no browser."

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

This target was a Fastify app called "Search Mirror", with a route that reflects input and a separate, isolated callback route. The weak point was a **trust decision made on a client-supplied header**: the callback released the proof when two things were presented together.

## The solve

The two gates were a disclosed callback nonce and a `Referer` whose path was the reflection route. Both are ordinary HTTP values, so the solver sets them directly and no browser is needed. That was the reasoning: the callback was meant to be reached by a page, but it only checked what that page would have sent, and a client can send the same thing.

The notes record the Day 21 web challenges as solved by three parallel subagents and folded into `websolve.py` as `solve_reflect`. On release morning the time trial was confirmed at 09:19:13.

The defence is not to rely on `Referer` for authorisation, since the client controls it, and to bind a callback to a server-side session or token.
