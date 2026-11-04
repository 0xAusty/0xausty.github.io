+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Decoder Ring"
date = 2026-10-17  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day17-decoder-ring"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 17 (2026-10-17), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-17-encoded-configuration-recovery
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 17 left 24 per-day facts unresolved at release, including a storage label with no visible vocabulary that the agent mapped with about 900 one-field probes of the grader."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "bresolve.py", "python"]
tags   = ["reverse-engineering", "xor", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 17 re-asked every earlier day for two new facts, on top of the 12 for the new binary. At release 180 of 204 fields were resolved; the 24 misses were per-day facts such as the HCFG version, XOR key and offset, runtime predicates, Java method lists and a new "HCFG storage" label.

## The solve

Claude Code fixed most of them in the session as `binsolve._extras`, which runs after each day's branch for any day that asks: the C marker and recover code through `bresolve.c_fields`, the typeinfo symbol of the class that owns `score()`, the Go, Rust and coroutine predicates, section names, and the Java main class's methods, access flags and method count.

The storage labels were the hard part, because nothing showed their vocabulary. A one-field submit returns "accepted" only when that field is right, so the session used the grader as an oracle: one guess per submit, about half a second each. About 900 probes over roughly 25 minutes found the accepted labels. They name the construct (a base64 string literal, a raw constant array), not the section it lands in. Rejected guesses included section names and plain "raw".

The time trial needed one more rule. Its Day 1 binary was stripped, and the grader wanted `none` for the recover code, not the constant a byte search still found.

The label hunt made binary the day's critical path, with its last mode correct by 09:33:57. I had approved closest-name guessing two days earlier.
