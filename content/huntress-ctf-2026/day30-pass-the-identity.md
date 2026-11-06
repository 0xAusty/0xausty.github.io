+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Pass the Identity"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-pass-the-identity"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "web" (Web Exploitation), web_no 28
#   gm_id web-exploitation-day-28-pass-the-identity
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A delegated service boundary trusted a header asserting the end user's identity, and its 403 response named that header in Vary."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["web-exploitation"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a small Axum service ("Caller Courier") with one feature route behind a delegated service boundary. The boundary believed a request header that named the end user and never checked that the caller was allowed to say so. The single and time trial asked for one proof field, mastery for a bundle of five.

## The solve

An identity directory showed the caller's role and the owner of the privileged records. A request to the feature route with no identity header got a 403, and its Vary response header named the header the service trusted. The solver, `solve_passidentity` in `websolve.py`, replays the feature request with that header set to the privileged owner, then falls back to any directory identity that isn't its own role. The proof came back in the evidence field.

The agent added the function in session and the supervisor hot-reloaded it. An earlier 09:00 pass, before the function existed, had misclassified the target as SSRF. The single was correct at 09:02:03 on the release morning.

The defence is to have the edge authenticate and set the identity header itself, and to strip it from anything a client sends.
