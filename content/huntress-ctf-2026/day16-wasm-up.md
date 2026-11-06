+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Wasm Up"
date = 2026-10-16  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day16-wasm-up"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 16 (2026-10-16), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-16-webassembly-optimization-equivalence
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A new binary format on Day 16, WebAssembly, needed only a magic-number check and the right format and architecture labels, and everything was accepted on the first submit."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python"]
tags   = ["reverse-engineering", "wasm", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The Day 16 bundle added a pair of WebAssembly builds, a "direct" and a "compact" one, to the cumulative evidence zip. The questions were the usual per-binary facts: two SHA-256 fields, tagged format and architecture fields, and the HCFG config. The only new thing was the format.

## The solve

At release 150 of 160 fields were banked automatically. The ten WebAssembly fields went unanswered because the two-build branch and `_generic_binary_day` in `binsolve.py` only accepted ELF and PE files. Claude Code fixed it in the session: accept the `\0asm` magic, answer `wasm` for the format and `wasm32` for the architecture, find the HCFG with the existing `_find_hcfg`, and number the SHA-256 fields by zip order, direct build first.

Everything was accepted on the first submit. The same code then solved the time trial and the 800-field mastery unchanged. Later that morning the agent widened the generic handler to any binary format (Mach-O, Java class, DEX, Lua, pyc). Confirmed spellings are sent as answers; the rest go out as guesses with alternates, checked by the heal step.

The mastery stays locked until the time trial is correct. Running the modes in parallel got three other lanes an HTTP 409 that morning, so the lanes went back to single, then time trial, then mastery.

Binary was the day's tail lane, holding the last three of fifteen correct modes.
