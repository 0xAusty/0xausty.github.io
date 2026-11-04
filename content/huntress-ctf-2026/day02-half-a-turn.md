+++
title = "Half a Turn"
date = 2026-10-02
draft = true
params.kind = "challenge"
catalog_key = "day02-half-a-turn"
depth = "note"
featured = false
description = "A trivial ROT13 warmup that taught the first timing lessons: timers shorter than any analyst, and a retry that quietly swapped the artifact."
solved_by = ["agent"]
tools = ["wusolve.py", "python"]
tags = ["encoding", "rot13", "time-trial"]
skills = ["Automation & Tooling"]
toc = false
+++

The cipher here is ROT13, hinted by "thirteen steps forward", and it is trivial. The useful part is what the time trial taught on 2 October, which is why the one-process runner exists.

## The solve

For the single, my notes only say it was already correct by about 17:35 UTC on 2 October. That came from a handoff written by a chat AI session, so who solved it is not recorded. The time trial and mastery were solved in the 4 October Claude Code session. For the mastery, `wusolve.py` decodes each chunk separately and keeps only readings that match the known sentence prefix and contain dictionary slug words, because a ROT13'd slug still looks like a slug.

The lessons came from the first time trial. Timers ran about 5-8 seconds after start, too short for live analysis. A slug decoded from the original 107-byte artifact was submitted after a retry and came back incorrect, because the retry had served a different 109-byte file.

Never submit an answer derived from a stale artifact: re-fetch and hash after every retry.
