+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Package Deal"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-package-deal"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-21-package-deal
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "No parser held the Android package name, so spelling heals could not help; a binary-XML manifest parser had to be written in session."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["metaengine.py", "python"]
tags   = ["forensics", "android", "metadata"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 21 asked for the package name of an Android APK, as exact text. The pipeline failed it at 09:00:21, and Claude Code fixed it in session.

## The solve

An APK is a ZIP, and the engine had no APK parser. The generic ZIP parser claimed the bytes, and the closest-name guess offered the archive's member list as the "package". Heal then re-ordered that list four ways (sorted, descending, case-insensitive, reversed). All five submits were rejected.

A spelling heal can only recover a value the parser already holds. Here no parser held the field, and the nearest thing was a different fact.

The fix was a new `parse_apk` in `metaengine.py`. It opens the APK as a ZIP, decodes the binary XML of `AndroidManifest.xml` (the string pool, then the attributes on each start element) and reads the `package` attribute of the manifest element. It also exposes the application label, the version name and code, and the minimum and target SDK. The single was correct before the Time Trial at 09:13, since the Time Trial stays locked until the single is accepted, and Mastery followed at 09:13.

Self-healing recovers spellings, not formats: a new file type still needed a parser.
