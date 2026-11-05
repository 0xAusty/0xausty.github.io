+++
title = "The Shortcut Home"
date = 2026-10-14
draft = true
params.kind = "challenge"
catalog_key = "day14-the-shortcut-home"
depth = "note"
featured = false
description = "A static MS-SHLLINK parser answered every mode, and the same morning the per-day metadata handlers became one generic engine."
solved_by = ["agent"]
tools = ["lnksolve.py", "metaengine.py", "python"]
tags = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]
toc = false
+++

Each mode asked for one exact-text field: where a Windows shortcut actually points, as opposed to where the file sits. The prompt hinted at an impossible destination. Once the format was in hand the parsing was routine. The bigger change that day was to the rest of the lane.

## The solve

The 09:00 run had no answer, and the time trial and mastery weren't attempted. Claude Code then wrote `lnksolve.py`, a static MS-SHLLINK parser that walks the header, the target ID list, the link info, the string data and the extra data blocks without resolving anything against a live filesystem. The target path is the link info's local base path plus its common path suffix, falling back to the path rebuilt from the shell-item ID list and then to the environment-variable block. The parser also exposes the working directory, arguments, icon location, volume label and drive serial.

The commit landed at 09:32:44, and every mode was correct by then: the single at 09:23:10, the time trial at 09:23:20 and the mastery at 09:23:26. The same morning the agent folded the per-day handlers into one metadata engine.

Absent strings answer *none*, and numbers are rendered only when the declared format says integer.
