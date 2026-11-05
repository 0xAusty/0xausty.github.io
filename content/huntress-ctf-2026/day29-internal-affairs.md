+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Internal Affairs"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-internal-affairs"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "web" (Web Exploitation), web_no 27
#   gm_id web-exploitation-day-27-internal-affairs
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An SSRF on a public fetch route reached a loopback-only case service, whose missing per-object owner check leaked another role's record."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["web-exploitation", "ssrf", "idor"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

The target was a Ktor service with a public fetch route. The single and time trial asked for one proof field, mastery for a bundle of five. Both bug classes were routine. The useful part is that the challenge chained them.

## The solve

A topology route disclosed an internal case service reachable only from loopback, and a directory listed each case with its owner. The headless escalator's Claude agent folded the chain into `websolve.py` as `solve_internal_affairs`. It uses the server-side request forgery in the public fetch route to reach the internal service and asks for a case owned by someone other than the current role. The internal service had no per-object owner check, so it returned the record, with the proof in the reply's evidence field. The solver tries a foreign-owned case first, then every listed one.

The escalator log marks all three modes correct. The single was correct at 09:05:17 on the release morning.

Two boundaries failed here. The fetch let a public caller reach an internal service, and the internal service checked no owner on what it served. The fix is an allow-list on outbound fetches plus an owner check on every object, wherever the request came from.
