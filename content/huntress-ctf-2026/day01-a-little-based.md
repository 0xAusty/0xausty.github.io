+++
title = "A Little Based"
date = 2026-10-01
draft = true
params.kind = "challenge"  # Hugo reserves a top-level "kind" (removed in v0.144); this still reads as .Params.kind
catalog_key = "day01-a-little-based"
depth = "note"
featured = false
description = "The first warmup: one Base64 blob, and a strict decoder that accepts a decode only when the alphabet, the length and the output all check out."
solved_by = ["autopilot"]
tools = ["python"]
tags = ["encoding", "base64"]
skills = ["Automation & Tooling"]
toc = false
+++

The warmups lane opened with one blob and a prompt that doubles as the hint: "Everyone has to start somewhere. I hear sixty-four is a good base." The question asked for the blob to be decoded completely and for the exact answer slug that its final non-empty decoded line instructs you to submit. The declared format was strict: three lowercase words separated by hyphens, then a hyphen and a two-digit number, the slug alone.

The file was `blob.txt`, 148 bytes of Base64. Decoded, it is a single sentence of the shape "Nice work decoding this warmup! To solve, submit this exact answer to the Game Master: &lt;slug&gt;". That fixed sentence turned out to matter more than the slug, because it is what later warmup decodes were validated against.

My first harness, committed on 2 October, had a deliberately strict Base64 solver: it decodes only when the text uses a valid Base64 alphabet, the length is a multiple of four and the result is printable. Anything else is left alone rather than guessed at. That was enough here. All three modes came back CORRECT: the single, the time trial with its fresh 144-byte blob, and the three-question mastery zip. Times for Day 1 were not captured; the supervisor that logs them only started on Day 5.

Later warmups taught the solver to peel layers and to check each one against the known sentence, but the rule was set on Day 1: a decode is accepted when it can be verified, not when it looks right.
