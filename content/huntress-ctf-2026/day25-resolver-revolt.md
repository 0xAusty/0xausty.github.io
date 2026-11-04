+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Resolver Revolt"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-resolver-revolt"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "web" (Web Exploitation), web_no 18
#   gm_id web-exploitation-day-18-resolver-revolt
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "GraphQL field-level authorisation gap: an id-taking resolver returned a protected row's fields with no owner check, reachable once the schema was introspected."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "graphql", "idor"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This target was a POST-only GraphQL endpoint with no REST route. The prompt asked to vary the protocol surface without changing the authorisation discipline, which means the same authorisation gap as the earlier object-access challenges, reached through a different door. A resolver that takes an id returned a protected row's scalar fields without the owner or role check its index implied.

## The solve

A parallel Claude Code subagent solved it. The approach is to introspect the schema for the object resolver that takes an id, then read every scalar field on the protected reference, falling back to each id in the index. That became `solve_graphql` in `websolve.py`. The classifier also had to tell GraphQL apart from the plain object-access shape, since both expose a protected reference, and it did so with the framework fingerprint.

The single was correct by 09:07:26 on 25 October. Mastery shows how bundles bank: the first attempt came back accepted with three proofs still pending, and it only turned correct once the fourth target came in.

Hiding a field from a list view isn't authorisation. Every resolver needs its own check, because introspection hands the caller the whole schema.
