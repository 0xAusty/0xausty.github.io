+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Zig Zag"
date = 2026-10-10  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day10-zig-zag"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 10 (2026-10-10), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-10-zig-cross-platform-services
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 10 added a Zig binary with the config in its own .hcfg section; the lasting result was a generic handler that made later compiled-language days solve themselves."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python", "Claude Code"]
tags   = ["reverse-engineering", "zig", "elf", "pe", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The questions grew to 100 fields: Days 1 to 9 again, plus the new Zig binary, which stores its raw config blob in a dedicated section named `.hcfg`. One new field asked, literally, whether a section with that name exists. The Zig day itself was routine. The lasting result was the generic handler the agent wrote straight after it.

## The solve

The binary lane had no solver for Day 10 at the release, so it was skipped. The parallel run that morning gave each open lane to its own subagent. The binary one added a Day 10 branch: format from the magic bytes, machine from the ELF header or the PE COFF header, and the config blob picked by its CRC, which tells the real one from decoys. That branch was committed at 09:08, and the single was correct at 09:07:34, the time trial at 09:07:52 and the mastery at 09:08:09.

Straight afterwards the agent generalised it. `_find_hcfg` in `binsolve.py` looks for the blob raw, as base64 in a string literal, in a named section, or single-byte XORed, and accepts only a CRC-valid one. `_generic_binary_day` then answers from the declared answer format, and the agent checked it offline against Days 4, 5, 8, 9 and 10.

Timed mastery also came back this day after two untimed ones, so the live deadline had to be read every time. Days 11 to 14 then solved with no new code.
