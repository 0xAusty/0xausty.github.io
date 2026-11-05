+++
title = "A Little Based"
date = 2026-10-01
draft = true
params.kind = "challenge"
catalog_key = "day01-a-little-based"
depth = "note"
featured = false
description = "The first warmup: one Base64 blob whose answer is the slug in the final line, not the decoded sentence, which set the format rule every later warmup followed."
solved_by = []
tools = []
tags = ["encoding", "base64"]
skills = ["Automation & Tooling"]
toc = false
+++

The warmups lane opened with a Base64 blob, a hint in the prompt ("sixty-four") and a strict answer format: the slug alone, never the decoded sentence. It is routine decoding. What made it worth a note is the fixed sentence inside the blob, which every later warmup decodes to as well.

## The solve

The decode is Base64, then take the slug after "Game Master:" in the final line. My first harness, committed on 2 October with Claude Code as co-author, had a strict Base64 solver, but it returned the whole decoded text, and my notes later call that the wrong answer for warmups. Who or what submitted the Day 1 single is not recorded; the scoreboard puts it at 21:15:22 on 1 October.

The time trial and the mastery followed at 21:22:52 and 21:23:23 that evening, before the 4 October Claude Code session that wrote `wusolve.py` and `timed.py`, so the notes do not record what produced those answers either. `wusolve.py` decodes in a bounded search until the "Game Master: slug" instruction appears with dictionary words; `timed.py` fetches, solves and submits in one process. Later, the fixed sentence became known plaintext for deriving cipher keys.

Answer with the slug only, and check the format where it is declared: on start and submit, not on status.
