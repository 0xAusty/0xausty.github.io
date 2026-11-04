+++
title = "Hex Appeal"
date = 2026-10-03
draft = true
params.kind = "challenge"
catalog_key = "day03-hex-appeal"
depth = "note"
featured = false
description = "The lane's first wrong answer: the hex decode was right, but a generic decoder submitted the whole sentence instead of the slug inside it."
solved_by = ["agent"]
tools = ["wusolve.py", "python"]
tags = ["encoding", "time-trial"]
skills = ["Automation & Tooling"]
toc = false
+++

Day 3 is hex, hinted by "sixteen fingers". The decode was never the problem. The Day 3 single was rejected once because the answer was too long.

## The solve

One of the harness's generic decoders submitted the entire decoded string, and the Game Master rejected it. My notes do not record which decoder fired. The fix was a slug extractor: `wusolve.py` looks for three lowercase words and two digits after "Game Master:" and answers with only that. It is also what let the timed modes run without anyone watching.

A Claude Code memory from 4 October records the wrong submit and the need for the extractor. The time trial and mastery were solved in that same session. Who submitted the accepted single is not recorded, and the catalogue has no solve time for any Day 3 mode.

A second trap sat nearby: the declared answer format only appears in the start and submit responses, while status shows it empty.

Answer only what the format declares, which here was the slug and not the sentence around it.
