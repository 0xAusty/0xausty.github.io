+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Forwarded Misgivings"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-forwarded-misgivings"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "web" (Web Exploitation), web_no 23
#   gm_id web-exploitation-day-23-forwarded-misgivings
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Micronaut app trusted a client-supplied forwarded-IP header for a loopback-only gate; the fix is to accept that header only from the real proxy."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "websolve.py"]
tags   = ["web-exploitation", "header-trust", "python"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

One proof per target behind a reverse proxy, mastery a bundle of five. Routine once you recognise the class: the app makes an access decision from a forwarded client-IP header and treats it as if the proxy had set it.

## The solve

The feature route answers that it is loopback-only and reports the client address it evaluated. `solve_forwarded` in `websolve.py` supplies a forwarded header that names loopback, trying both the `X-Forwarded-For` and `Forwarded` syntaxes, and the JSON reply's `evidence` field is the proof. It is a read-only GET.

The agent folded it in with the other release-day web solvers (commit 57be6d0). The notes call it the fastest of the three Day 27 web challenges. The single was CORRECT at 09:07:24, the time trial at 09:08:36 and mastery at 09:09:02.

The web lane counted this as its day 23, though it was released on calendar Day 27.

The defence is to strip client-supplied forwarding headers at the edge and trust them only from the known proxy.
