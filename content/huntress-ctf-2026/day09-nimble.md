+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Nimble"
date = 2026-10-09  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day09-nimble"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 9 (2026-10-09), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-09-nim-generated-runtime
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Nim hides its config the way Swift does, as a base64 string literal among decoys, and an empty list is a valid answer when a symbol is missing."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "binmastery.py", "python"]
tags   = ["reverse-engineering", "nim", "elf"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 9 asked 90 fields: Days 1 to 8 plus ten for a Nim ELF, including a new integer for the file offset of the config blob. Nim turned out to be Swift in a different hat: same hiding place, same decoys.

## The solve

The binary lane was skipped at the 9 October release (09:02:03). Claude Code solved it in session that morning, and the day was complete by 09:25, with the single, time trial and mastery all correct by then.

The config is base64 in a string literal. Plaintext config strings in the binary are decoys, as is a dynamic-trace block. The `binsolve.py` helper finds the one base64 run that decodes to a record with a valid CRC32 and returns its file offset too, which answers the offset question. The mastery still went through `binmastery.py`.

Some variants have no `recover_code` symbol, and the disassembly field then wants an empty list. The machine is an integer here, while architecture and format are text.
