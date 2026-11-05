+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Posted Too Much"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-posted-too-much"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "web" (Web Exploitation), web_no 13
#   gm_id web-exploitation-day-13-posted-too-much
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mass assignment: the API bound every posted field onto the account object, so a privilege the form never offered could be set by the client; the fix is an allow-list."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = []
tags   = ["web-exploitation"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a mass-assignment challenge. The visible form asked only for a name, but the backing API deserialised the whole request body onto its model. A client that adds a privileged field the form never showed gets promoted, and the account then yields the proof. Each mode asked for one proof from a live target, and mastery was a three-target bundle.

## The solve

The reasoning is the usual one for this class: if the form shows one field and the server binds everything, the interesting field is the one the form leaves out. A Claude Code subagent solved it live on the release morning, working through single, time trial and mastery in turn. Single, time trial and mastery were confirmed at 09:10:04, 09:10:18 and 09:10:35 on 23 October.

The notes record the prompt and the times but little else, so I can't say which extra field the subagent used or how long it spent finding it. It was also not folded into `websolve.py`, so the bug class has no dedicated branch there.

The 09:00 first pass showed the single as unsolved. That was expected for a web shape the pipeline hadn't met, not a failure.

The defence is to bind only an explicit allow-list of fields, and never let a request set roles or flags.
