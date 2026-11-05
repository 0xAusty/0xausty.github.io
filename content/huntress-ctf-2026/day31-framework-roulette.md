+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Framework Roulette"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-framework-roulette"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "web" (Web Exploitation), web_no 30
#   gm_id web-exploitation-day-30-framework-roulette
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An unfamiliar ASP.NET Blazor Server target fell to two stacked header-trust gates, showing the lane's forwarded-header skill transfers to an unseen framework."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["web-exploitation"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

The organisers pitched this as a new stack with none of the usual names: an ASP.NET Core Blazor Server app, a framework I had no solver for. The single asked for one proof field. The 09:00 first pass classified it as unknown.

## The solve

The feature route sat behind two gates, both driven by headers the app trusts. The app took the client address from the leftmost entry of a forwarded-for header, so a forged value passed the first, loopback-style gateway check. Only then did a staff-policy gate appear, and its response named the privileged role header in Vary. Setting that header passed it, and the proof was in the evidence field. The order matters: the second header can only be discovered with the first already set.

That day went badly. The headless escalator died at a 600-second background-wait ceiling and the coordinating session crashed. Three fresh subagents were spawned by hand, one of them on this target, and the fix became `solve_roulette` in `websolve.py`. The catalog records the single correct at 09:18:18, the time trial at 09:19:51 and mastery at 09:21:50.

The defence is to trust forwarding headers only from a known proxy, and never to let a header grant a role.
