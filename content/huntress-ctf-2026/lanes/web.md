+++
title = "Web Exploitation"
date = 2026-11-02
draft = true
layout = "lane"
lane = "web"
weight = 60

description = "A sixth lane added mid-month and run against live targets: from backup exposure and IDOR to SSRF, SSTI and a final incident reconstruction, each class solved once and then generalized into a solver with a live self-test."

tags   = ["ctf", "web", "sqli", "xss", "ssrf", "ssti"]
skills = ["Web Application Security"]
toc    = true
+++

Web Exploitation was the sixth lane, added mid-month. Its challenges were released to players from Day 19, in batches and with their own numbering from 1 to 31, and they ran against live targets.

The lane covered one vulnerability class after another: backup exposure, IDOR, boolean-blind and second-order SQL injection, LFI and path traversal, forced browsing, reflected and stored XSS, session fixation, CSRF, upload to SSTI, mass assignment, SSRF, GraphQL authorization, command injection, password-reset binding, webhook trust, serialized state, double spend, WebSocket authorization, forwarded-header spoofing, fail-open parsers, audit-log integrity, supply-chain signatures, delegated identity, queue ownership, framework fingerprinting, and a final incident reconstruction.

Each class was solved once against its live target, by me, by an agent, or on two occasions by the event's Homebase AI, and then generalized into `websolve.py`. Targets expire, so they cannot be replayed offline; the solver's regression check is instead a live self-test against fresh, non-scoring variants.
