+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Managed Expectations"
date = 2026-10-12  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day12-managed-expectations"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 12 (2026-10-12), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-12-managed-expectations
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The module version ID of a .NET assembly, rendered as a canonical lowercase GUID; the notes do not record who first solved it, only that a generic reader followed."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = []

tools  = ["dotnetmeta.py", "metaengine.py", "python"]
tags   = ["forensics", "metadata", "dotnet"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Each mode asked for the MVID of a small .NET assembly. The assemblies shared names, versions and source ancestry but kept distinct module identities.

## The solve

The notes do not record who solved it. The release sweep left it unsolved, and the agent's handoff says only that it was solved outside the repo, with no solver change committed. Every mode was correct on the release morning: the single at 09:01:32 and the time trial and mastery at 09:04:29 and 09:04:39; a commit at 09:32 on 14 October reports Days 12 to 14 at 15 of 15 each.

Two days later the repo gained `dotnetmeta.py`, a reader for the .NET metadata format: PE data directory 14, the CLI header, the metadata root, the table stream, then the Module table's Mvid taken from the GUID heap. It answered the MVID question in later cumulative time trials.

The MVID is a binary GUID with no stored text, so the accepted spelling is the canonical lowercase 8-4-4-4-12 form, confirmed on Day 15. The binary itself prints it with .NET's `ToString("D")`, which is why the golden was first stored as unverified.
