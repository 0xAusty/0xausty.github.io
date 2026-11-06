+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Table Manners"
date = 2026-10-03  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day03-table-manners"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 3 (2026-10-03), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-03-managed-configuration
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The first cumulative bundle: an under-specified symbols field resisted every obvious list until the neighbouring questions were read as a spec for its scope."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["homebase", "agent"]

tools  = ["binsolve.py", "python"]
tags   = ["reverse-engineering", "elf", "dotnet"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

This was the first cumulative bundle: 24 fields over Days 1 to 3, spanning the Day 1 C ELF, the Day 2 C++ ELF and a .NET DLL. Most of it was ordinary format-and-config reading, except for one field.

## The solve

About 20 of the 24 fields were banked before 6 October. Claude Code then wrote `binsolve.py`, which added the .NET answers (the CLR version from the metadata root, the config record from the DLL's raw bytes) and the Day 1 disassembly, reaching 23 of 24.

The last field asked for the Day 1 ELF's symbols with no guidance on which ones or in what order. Every obvious list was rejected: the full table with the empty names, the planted names alphabetically, the planted names in table order. On 7 October the event's Homebase AI (GPT-6 Luna) supplied the reading: section names and symbols are both ELF inventory, and a separate question already covers `recover_code`, so "symbols" meant the whole `.symtab` in stored order, empty names dropped. The agent encoded that and swept every binary single, time trial and mastery for Days 3 to 7.

The .NET format wanted a compound token, not bare *pe*, and the machine wanted lowercase text.
