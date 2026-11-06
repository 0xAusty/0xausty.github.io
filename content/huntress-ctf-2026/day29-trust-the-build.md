+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Trust the Build"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-trust-the-build"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "web" (Web Exploitation), web_no 26
#   gm_id web-exploitation-day-26-trust-the-build
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A package updater trusted a signature's presence without re-checking the artifact hash it covered; the first fully automated web recovery by a headless Claude escalator."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "websolve.py", "run-escalate.sh"]
tags   = ["web-exploitation", "supply-chain", "signature", "python"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

A live Fiber updater serving a signed package manifest and an update policy. One proof per target, mastery a bundle of five. The supply-chain bug was small: the updater treated a signature as if it were integrity.

## The solve

The manifest covers the artifact bytes with a SHA-256, and the signature is over that hash. The updater activates a signed manifest but never re-verifies the bytes against the hash. `solve_trustbuild` in `websolve.py` takes the routine manifest, swaps its artifact hook for the restricted privileged hook the update policy names, keeps the original signature and submits it. The unverified update activates and the reply carries the proof.

This was the first web recovery run end to end by the escalator, `run-escalate.sh`, which spawns a headless Claude agent after a first-pass miss instead of a subagent spawned from the coordinating session. The single was CORRECT at 09:04:39. The time trial was recorded at 09:05:50 and mastery at 09:06:25. By 09:08 the escalator's log reported all modes correct on this and another web challenge.

Verify the hash after activation as well as the signature.
