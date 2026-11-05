+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Sharp Practice"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-sharp-practice"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-19-managed-assembly-bridge
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Roslyn C# script inside an ASPX page: the payload ran into C#'s own escape sequences, so it had to end at the first escape or quote."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["polysolve.py", "heal.py"]
tags   = ["malware-analysis", "csharp", "aspx", "obfuscation"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

A Roslyn C# script hosted inside an inline ASPX page, 1,249 fields. The prompt asked for the layered configuration of a `.csx` bridge and each static handoff. The new carrier was the catch.

## The solve

In this carrier the `.csx` sits inside a C# string literal inside an ASPX `<script runat="server">` block. The `HUNTRESS_ANALYSIS_V1:HEX-` payload therefore ran straight into a literal backslash-n escape and picked up stray hex letters from it, so the decode failed and 9 fields were left unanswered. The supervisor's heal had recovered the role and technique from the enum alternates, but it can't recover free-text fields.

Claude Code fixed it in session: `polysolve.fields` now ends the payload at the first escape sequence or quote. That gave 1,249 of 1,249, and the Time Trial and Mastery passed on their first submits. The records put the single at 09:04:16 and the other two at 09:05:13 and 09:05:18.

When a carrier embeds the payload in a string literal, the host language's escape sequences are part of what you parse.
