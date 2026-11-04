+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Fail Open Friday"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-fail-open-friday"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "web" (Web Exploitation), web_no 24
#   gm_id web-exploitation-day-24-fail-open-friday
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An access check that called a remote policy decoder allowed the request when decoding threw; deny-on-error had become allow-on-error."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "websolve.py"]
tags   = ["web-exploitation", "fail-open", "python"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

A live ASP.NET Core Razor Pages target, one proof per target and a bundle of five for mastery. The prompt asked what happens when the access decision cannot be decoded, and that is the whole bug.

## The solve

The access check consults a remote policy decoder. A policy-format route documents the parameter name and the shape of a valid value: a prefix followed by an encoded JSON payload. `solve_failopen` in `websolve.py` reads those from the format route, sends the correct prefix with a payload that cannot be decoded, and the decoder throws. The broken check then fails open, and the feature route returns a proof in its `evidence` field.

The single first showed unsolved on the 09:00 pass, as new web shapes did before a solver existed. It was CORRECT by 09:15:29 after an agent recovery on the release morning. The time trial was recorded at 09:17:40 and mastery at 09:18:24.

The error path is the vulnerability. Authorisation code should deny when it fails, and a test should feed it malformed input.
