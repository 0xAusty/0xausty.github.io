+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Socket to Me"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-socket-to-me"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "web" (Web Exploitation), web_no 22
#   gm_id web-exploitation-day-22-socket-to-me
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Authorisation was enforced on the HTTP routes but not on the WebSocket upgrade, and with no pip available the agent wrote a stdlib-only WebSocket client to exploit it."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "websolve.py", "wsc.py"]
tags   = ["web-exploitation", "websocket", "python"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

The target was a live Koa app. It wanted one proof per target, and mastery was a bundle of five. The bug was a plain missing authorisation check; the tooling it forced is what made it worth a note.

## The solve

The HTTP routes checked the caller's role. The WebSocket upgrade didn't: subscribing to a stream ran no authorisation at all. A disclosed clues endpoint gave away a privileged stream reference. Of the query parameters on the feature route, only one carried the subscription and the rest were inert. Open the socket with that reference and the first text frame holds the proof in an `evidence` field.

The `requests` library can't speak WebSockets, and the host had no pip. Claude Code added two pieces under the parallel-subagent flow: `wsc.py`, a stdlib-only raw client over TLS with its own handshake and frame codec, and `solve_socket` in `websolve.py`, which uses it. The single was CORRECT at 09:11:10, the time trial at 09:14:19 and mastery at 09:17:45.

The gotcha is that the proof here is a JSON `evidence` field, so a scan for the usual token shape misses it. On the server side, the fix is to authorise at subscribe time as well as on the HTTP routes.
