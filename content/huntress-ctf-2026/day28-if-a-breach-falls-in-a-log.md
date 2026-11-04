+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "If a Breach Falls in a Log"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-if-a-breach-falls-in-a-log"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "web" (Web Exploitation), web_no 25
#   gm_id web-exploitation-day-25-if-a-breach-falls-in-a-log
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A privileged export was logged as a benign page view, so the audit trail hid the real action; the solver proved the gap by correlating the export id."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "websolve.py"]
tags   = ["web-exploitation", "logging-gap", "audit-log", "python"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

A different angle for the web lane: the flaw is in what the application recorded, not in what it allowed. One proof per target on a live Slim app, mastery a bundle of five.

## The solve

The target had a privileged feature action and an audit route that reports discrepancies over its log. `solve_logging_gap` in `websolve.py` runs the protected export through the feature route, which returns an export id and the real operation name. It then reads the audit log, where that export appears as a harmless page view. Finally it submits the discrepancy report tying the export id to the real operation, the decisive moment the log missed, and reads the proof from the reply.

The solve depends on correlating the export id across the feature reply and the audit log. An agent recovery wrote it on the release morning. The single was CORRECT by 09:15:39, the time trial was recorded at 09:18:29 and mastery at 09:19:21.

Takeaway: a privileged action that is logged as something benign is a detection gap, and the fix is to log it as itself.
