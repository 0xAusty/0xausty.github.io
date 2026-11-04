+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Shell Company"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-shell-company"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "web" (Web Exploitation), web_no 16
#   gm_id web-exploitation-day-16-shell-company
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "OS command injection through a shell string: a filter blocked command substitution but not separators or variable expansion, and the proof path was named in the environment."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "command-injection"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was OS command injection. A feature route ran a shell command over user input, effectively listing a path, and returned the output. The input went into a shell string unsanitised. The interesting part was a filter that blocked command substitution but not command separators or bare variable expansion.

## The solve

The 09:00 first pass classified it wrongly and failed, because `solve_cmdi` didn't exist yet. One of three parallel Claude Code subagents built it, and the supervisor hot-reloaded it. The solver keeps the disclosed example path so the normal listing still succeeds, then chains a read of the proof file and a dump of the environment into the same request. The proof file's path is named by an environment variable, so the dump is how it finds the file.

The single was correct by 09:07:24 and the time trial by 09:08:38 on 25 October. The solver is in `websolve.py`.

Blocklists on shell metacharacters rarely hold, because the shell has more ways to chain and expand than a filter lists. The fix is never to build a shell string from input: pass arguments as a list, or avoid the shell entirely.
