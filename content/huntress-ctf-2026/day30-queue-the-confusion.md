+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Queue the Confusion"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-queue-the-confusion"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "web" (Web Exploitation), web_no 29
#   gm_id web-exploitation-day-29-queue-the-confusion
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A job queue bound each job to a client-supplied owner field instead of the authenticated caller, so enqueueing as the restricted owner returned its outcome."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["web-exploitation", "idor"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a Pyramid job queue with an enqueue route, an audit route that reports a job's outcome, and an owner directory listing the caller's role and a restricted owner. Single and time trial asked for one proof field. Mastery was a six-target bundle, the largest in the lane.

## The solve

The flaw was an **owner-binding** one: the queue took the job's owner from a field the client supplied, not from the caller's own role. `solve_queue_binding` in `websolve.py` enqueues a job naming the restricted owner from the directory, then asks the audit route for that job's outcome. The proof is in the evidence field. The field and parameter names came from each route's own error response to a plain GET.

The agent folded the solver in and the supervisor banked it. The single was correct by 09:02:31. The time trial was the long pole of the morning: it was retried repeatedly and the supervisor logged it far more than any other challenge, with the first correct by 09:07:58 alongside mastery.

The fix is to derive ownership from the session and ignore any owner the request names.
