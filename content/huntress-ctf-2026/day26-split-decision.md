+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Split Decision"
date = 2026-10-26  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day26-split-decision"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 26 (2026-10-26), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-26-split-decision
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The answer only existed after an App Bundle's base and feature splits were merged into one APK, so solving each split separately found nothing."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mobsolve.py", "mobemu.py", "python"]
tags   = ["android", "dex", "emulation", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The question named a case reference and an app package and asked for the backend's answer code. The evidence was spread across a base split and a feature split of an App Bundle, so a per-APK solve could never see all of it.

## The solve

At the 09:00 release the pipeline treated `base.apk` and `feature.apk` as two separate apps and got nothing from either. Claude Code taught `mobsolve.py` to treat a bundle of APKs as one app. For the static codec it fills the base's empty part slots from JSON assets in the feature split. For the computed codec it rebuilds a single APK from the base plus the feature split's assets and runs that through the existing solver.

The emulated code also reads a byte asset from a feature split, so `mobemu.py` gained a hook for it. Java bytes are signed, so the hook hands back values in -128..127. The single was correct by 09:06:57.

The timed run failed on every attempt from 09:07 to 09:20, six times with an integer-has-no-length error from the emulated code. An emulator fix and a reload at 09:21:45 returned one merged answer, and the time trial and mastery were correct by 09:21:50.

An App Bundle is one app, and the solver now loads its splits that way.
