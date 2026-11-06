+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Trust Issues"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-trust-issues-metadata"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-29-trust-issues
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Routine X.509 fingerprint day; the notable part was a first-pass report that wrongly listed every lane as missed because it counted still-running singles."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["metaengine.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["forensics", "x509"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The single asked for the SHA-256 fingerprint of `certificate-001.pem`, matched as a case-insensitive pattern; the timed modes grew that to 34 and then 442 cumulative fields. The metadata lane itself was routine; the day earns a note for a bug in the reporting around it.

## The solve

The X.509 parser in `metaengine._cert_fields`, built on the `cryptography` package, exposes `sha256_fingerprint`: the SHA-256 over the certificate's DER encoding. The pipeline answered on the first submit and banked the three modes at 09:00:07, 09:00:11 and 09:00:16.

The bug was in the first-pass misses report. It fired at 09:00:04 and listed every lane as missed, metadata included, because it counted singles that were still running; metadata banked 12 seconds later. Once the escalator was wired to that report, it could have spawned deterministic-solver agents for lanes that were solving normally. The fix, a 90-second wait before the report fires, landed on Day 30.

A report that cries wolf becomes dangerous once something acts on it.
