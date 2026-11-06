+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Before You Go"
date = 2026-10-26  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day26-before-you-go"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 26 (2026-10-26), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-26-before-you-go
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Prefetch files answered on the first submit because the parser and its Xpress-Huffman decoder had been built on 14 and 15 October, before any prefetch challenge existed."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaextra.py", "xpress.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["forensics", "prefetch"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The single asked for `executable_name` from a prefetch file, `trace-001.pf`; the timed modes grew that to 31 and then 310 cumulative fields. Nothing about the day was hard, because the preparation had been done well in advance.

## The solve

The agent built `metaextra.parse_prefetch` on 14 October for uncompressed SCCA versions 17, 23, 26 and 30. On 15 October it gained version 31, following libyal's notes, and the Windows 10 compressed format, decoded by `xpress.py`, which was written from the MS-XCA pseudocode. The parser read the name from the header and the pipeline answered on the first submit, banking the three modes at 09:00:05, 09:00:07 and 09:00:10. All three were first bloods, the first of 1,602 teams: the single landed 0.3s ahead of the next team, the Mastery 1.3s.

Building the decoder hit one snag. One of the spec's worked examples had lost a byte in the fetched copy, and that surfaced only because the Huffman code came out incomplete: the Kraft sum fell short of 1. With the byte restored, the example decoded to the alphabet. At that point the decoder had never seen a real prefetch file, and the notes don't record whether the Day 26 files were compressed.

Eleven days of lead time turned this into a non-event.
