+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "ELF Aware"
date = 2026-10-01  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day01-elf-aware"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 1 (2026-10-01), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-01-c-elf-orientation
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine header-reading primer on one plain C ELF, whose symbol table came back as the binary lane's longest blocker in the cumulative bundles from Day 3."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = []

tools  = []
tags   = ["reverse-engineering", "elf"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The first binary challenge was a primer: nine header-level facts about one plain C ELF, such as class, byte order, machine, object type, a custom section's string, whether a symbol table survives and the entry point. It was routine. The time trial and mastery asked the same nine facts again, four and eight times over.

## The solve

The notes don't record who solved Day 1 or how. The scoreboard dates all three modes to the morning of 2 October, between 09:06:02 and 09:28:33, and the only line in the notes is a later hand-off note that lists the Day 1 mastery fields among those with no code in the repo. I'm not going to guess at a method.

The notes do show how the same facts were automated later. The `binsolve.py` branch for this ELF emits the class, byte order, object type and machine as fixed text, reads the entry point from `e_entry` and whether a `.symtab` exists, and lists the section names in header order. A shared helper reads the `recover_code` constant and accepts it only when the symbol and a byte-pattern search of `.text` agree.

The same ELF rides along in every later cumulative bundle, so these fields kept coming back.

Here the facts were spelled as text. Later days asked for the same ones with integer kinds.
