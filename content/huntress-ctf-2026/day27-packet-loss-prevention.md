+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Packet Loss Prevention"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-packet-loss-prevention"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-27-packet-loss-prevention
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine capture-file day: the pcap parser added on 14 October counted packets from record headers and the pipeline answered on the first submit."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaextra.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["forensics", "pcap"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The single asked for `packet_count` from `capture-001.pcap`, as an integer; the timed modes widened it to 32 and then 352 cumulative fields. It was a routine automatic day, and the notes record nothing else about it.

## The solve

`metaextra.parse_pcap`, the parser for PCAP and pcapng files, had gone in on 14 October. It walks the capture's record headers without decoding any packets and exposes `packet_count` directly. The pipeline answered on the first submit and banked the three modes at 09:00:06, 09:00:09 and 09:00:13.

The day's critical path was in the web lane, where three new challenge shapes needed attention.

The lesson is a dull one: a parser written for a field two weeks before anyone asked for that field is what makes a lane look effortless on the day.
