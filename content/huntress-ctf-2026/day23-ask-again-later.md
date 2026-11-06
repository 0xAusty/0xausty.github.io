+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Ask Again Later"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-ask-again-later"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "web" (Web Exploitation), web_no 12
#   gm_id web-exploitation-day-12-ask-again-later
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Second-order injection: the payload is stored, a background process acts on it later, and the proof appears on a follow-up read rather than in the first response."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = []
tags   = ["web-exploitation", "second-order-injection"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was an app that stores input and evaluates it later through a delayed path. Single and Time Trial asked for one proof field, and Mastery was a three-target bundle. The notes keep the prompt and the times, not the mechanism, so I will not claim more than that.

## The solve

The class is **second-order injection**. The request that plants the data looks inert and nothing comes back. The effect only shows when a later process reads the data, so the proof is retrieved on a follow-up read rather than in the first response. The prompt said as much, with its hint that the delayed echo tells all.

A subagent in the session solved it live against the game master. It was not added to `websolve.py`, so no committed solver exists. Single, Time Trial and Mastery were confirmed at 09:14:38, 09:14:56 and 09:15:06 on release day. The exact payload and back-end are not recorded, and I have not reconstructed them.

The defence is to treat stored data as untrusted every time it is read, not only on the way in. The gotcha: a blank response to the first request is not a failed one.
