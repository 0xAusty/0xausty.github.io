+++
title = "Web Exploitation"
date = 2026-11-02
draft = true
layout = "lane"
lane = "web"
weight = 60

description = "A sixth lane added mid-month, run against live targets: backup exposure, IDOR, SSRF, SSTI and a final incident reconstruction, most folded into a self-testing solver."

tags   = ["ctf", "web", "sqli", "xss", "ssrf", "ssti"]
skills = ["Web Application Security"]
toc    = true
+++

Web Exploitation was the sixth lane, bolted on mid-month. Its challenges appeared from Day 19 under their own counter, 1 to 31 — the first three backfilled with no release clock, then two or three every morning after — and every one ran against a live target rather than a file to download.

Across thirteen days it ran through most of the OWASP catalogue. The early targets were textbook disclosure and injection: an exposed backup, an IDOR, boolean-blind SQL injection, path traversal, forced browsing, a reflected callback, a bot-driven stored XSS, session fixation, CSRF and a file upload chained into template evaluation. The middle days moved to broken access control and API flaws: server-side template injection, a second-order injection, mass assignment, object- and function-level authorisation gaps, SSRF, GraphQL field authorisation, command injection and a password-reset token bound to no account. The last week was about misplaced trust — an unsigned serialised session, a webhook that verified nothing, a credit raced into a double spend, a WebSocket that skipped authorisation on upgrade, spoofed forwarded headers, a fail-open access check, an audit log with a gap in it, a signed build left unverified, a queue that trusted a client-supplied owner, the same bugs on an unfamiliar framework, and a final incident to reconstruct and repair.

Each class was solved once against a live target; most were then folded into `websolve.py`. The work was the coding agent's — Claude Code, in a live session, a release-morning subagent, or later a headless escalator — with one exception: the Trust the Webhook reading came from the event's Homebase AI (GPT-6 Luna) after an hour of automated probing stalled. My part was the rules and the triage order, not the solving. Targets expire, so nothing replays offline; the regression check is a live self-test that re-solves a fresh, non-scoring variant of each known class.

## What the lane kept asking for

Every single asked the same thing: one `exact_text` field, the proof recovered from one live target. The time trial repeated that field against a fresh target under the clock, and the mastery bundled several targets — two to six — each a different app and often an earlier day's class. So a mastery was not one puzzle but a handful, each classified on its own.

Because the lane had no artifact, there was nothing to parse offline. Each attempt handed back a short-lived site with its app name, routes and parameter names randomised, so a solver discovered what it needed from the pages rather than hardcode it. The convention that caught the pipeline out was where the answer lived: on most classes the proof came back inside a JSON `evidence` field, not the `proof_` token the first targets used, and a scan for the token alone walked straight past it.

The three modes were gated: a time trial would not open until its single was CORRECT, and a mastery not until its time trial was. A brand-new shape that missed on the single therefore cost all three modes at once.

## How the solver took shape

The lane arrived on 19 October, its first three challenges backfilled with no release clock. They were worked that evening and folded the same day into `websolve.py` (commit `2e8c821`), which classifies a live target and dispatches it to a proven procedure under the same `run()` contract the other five lanes use. The blind-SQLi extractor was the one piece with real engineering: a per-character search parallelised across threads to finish inside the target's short TTL.

The rule was to solve each shape once, fold in one concrete proof-recovery solver, and never pre-build a generic web-attack framework — the speculative offensive pieces added no value without a live target and kept tripping the safety classifier. From 20 October the challenges came two or three a morning, and release-day misses went to parallel subagents, one per open challenge.

Two changes shaped the rest of the month. The rewritten supervisor, live on 25 October, added a hot reload: saving a solver file made it re-attempt the unresolved modes within half a minute, so an agent could submit the single, fold its procedure in, save, and let the supervisor bank the time trial and mastery. On 27 October, when web was the whole critical path for about twenty-five minutes, three supports went in: an auto-recon dump on every miss, a gated `reset()` to heal a bricked one-shot target, and a reusable web-solver playbook. The lane grew its own primitives too — `wsc.py`, a stdlib WebSocket client written because the laptop had no library and no pip, and `jwtkit.py`, the one class verifiable offline without a live target. By 29 October a headless escalator was taking web misses on its own; the last morning finished in a crash-and-recover scramble, three fresh subagents reconnected to the open attempts. By then `websolve.py` held close to thirty solver classes.

## Days worth knowing

- **Day 26 · [Trust the Webhook](/huntress-ctf-2026/day26-trust-the-webhook/)** — the lane's best reversal: an hour lost not to the exploit but to a scanner that recognised a proof token and ignored the `evidence` field holding the answer, broken by the Homebase AI.
- **Day 27 · [Double Spent](/huntress-ctf-2026/day27-double-spent/)** — a time-of-check/time-of-use race on a one-shot credit, where a careless serial probe spent it and bricked the target, which drove a self-healing reset.
- **Day 31 · [Full Stack Incident](/huntress-ctf-2026/day31-full-stack-incident/)** — the closing capstone, the only challenge that wanted a fix as well as an exploit: reconstruct the incident from a log, reproduce it, then ship a detector and repair.
- **Day 27 · [Socket to Me](/huntress-ctf-2026/day27-socket-to-me/)** — a WebSocket whose upgrade did no authorisation, reached with a from-scratch stdlib WS client because the laptop had no pip to install one.
- **Day 25 · [Shell Company](/huntress-ctf-2026/day25-shell-company/)** — OS command injection with a precise filter bypass: command substitution blocked, but `;` chaining and bare variable expansion allowed, and the proof path named by an environment variable.
- **Day 21 · [Stored for Later](/huntress-ctf-2026/day21-stored-for-later/)** — a stored XSS that did nothing until an authenticated moderator bot rendered the note, then exfiltrated moderator-only data back to a channel the attacker could read.
- **Day 25 · [Resolver Revolt](/huntress-ctf-2026/day25-resolver-revolt/)** — GraphQL object-level access control: the same authorisation gap the REST targets had, reached over a different protocol surface by introspecting the schema.

## What the lane taught

- **Solve first, generalise second.** Every shape was worked once against its live target, and nearly all were folded into one concrete solver; the speculative attack library was never built, and never missed.
- **The tool's assumptions are part of the attack surface.** The `evidence`-versus-`proof_` blind spot cost an hour on a request that was already correct; widening the reader, not the exploit, was the fix.
- **A one-shot resource makes reconnaissance dangerous.** Where an action can be taken only once, recon stays read-only and the write path is touched only inside the exploit.
- **Most of these were authorisation bugs, not injections.** The lane trusted a client-supplied owner field, a forwarded header, an unsigned serialised blob, a reset token bound to no account and a signature's mere presence far more often than it failed to sanitise input.
- **Offence and defence are one skill.** The capstone rewarded reproducing an incident and then closing it, which is closer to real incident work than a flag on its own.
