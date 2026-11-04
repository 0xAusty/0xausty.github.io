+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Full Stack Incident"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-full-stack-incident"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "web" (Web Exploitation), web_no 31
#   gm_id web-exploitation-day-31-full-stack-incident
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = true                    # true → appears in the hub's "Start here"

description = "The web lane's capstone: reconstruct an unsigned-fetch-to-worker SSRF incident from the request log, reproduce it, then ship a detector and repair that block it while preserving signed status checks."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "ssrf", "time-trial", "mastery"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = true
+++

Full Stack Incident was the last challenge the [Web Exploitation](/huntress-ctf-2026/lanes/web/) lane released, and the only one that asked for a fix as well as an exploit. Its single wanted one proof from one live target, but getting there meant reconstructing an incident that had already happened, reproducing it end to end, then submitting a defence that blocked the attack without breaking the feature it abused. It is the lane's most useful story, because it shows both halves of the work: the break and the repair.

## The challenge

The web lane has no downloadable artifact. Each attempt hands back a live site on a short time-to-live, and the proof sits on the target rather than in any bytes. Here the target was an Actix Web service the organisers called "Whole Story". The single asked for one field as `exact_text`; the time trial was the same field under the clock; the mastery bundled the capstone with siblings of earlier web types, each classified on its own.

What set this one apart was the shape of the task. Every other web day ended at the exploit; this one did not. It asked me not only to break the service but to reconstruct the incident from the request log, reproduce it, and submit a detector and repair. The grader scored the fix, not just the break.

One lane-wide convention also applied: the accepted value came back as a JSON `evidence` field, not as a token in the obvious `proof_` shape, so a blind scan for the token alone would have walked past the answer.

## Reading the prompt

The prompt was a brief, not a riddle. It named the incident class and told me where the evidence was.

| Phrase | Implication | What the solver did |
|---|---|---|
| "Reconstruct the unsigned fetch-to-worker incident from the request log" | The attack is already on record; the log names the forged event. | Read the request log and took the one fetch record marked unsigned (`signed: false`). |
| "Follow the exposed service routes to reproduce it" | The routes needed to replay the chain are discoverable, not hidden. | Enumerated the disclosed routes — a dispatch route, an audit route, a worker route, an evidence route and a response route — and replayed the chain through them. |
| "inspect the resulting evidence" | The outcome is an evidence record, not a value echoed in a response. | Read the evidence route for the executed event and its response schema. |
| "submit a detector and repair that block the attack while preserving signed status checks" | The fix is graded, and it has to be selective. | Built a detector for the unsigned executed event and a repair that required a signed event, blocked the internal fetch, and allowlisted only the legitimate command. |

## What was on the target

The service modelled a small event-driven back end. A dispatch route turned a "fetch event" into queued work; an audit route verified a queued event and handed it to a worker; the worker route executed a command tied to that event; and a request log, an evidence route and a response route recorded and graded what happened.

The defect was in how the service decided a fetch event was trustworthy. It treated an event as **signed** — authentic, safe to dispatch — purely because its target matched the token already sitting in the queue. That is not a signature check; it is a token-equality check. The request log proved the consequence: it held exactly one fetch record whose `signed` flag was `false`, and whose target was that same queued token. An unsigned event was being accepted as signed. That mismatch is the whole vulnerability: forge a fetch that points at the queued token, and the worker will dispatch and run it as though it had been authorised.

The class is server-side request forgery chained to worker command execution, gated by a trust flag that was never really verified. Everything the solver needed was disclosed by the service's own clues and log — which mattered, because the routes and tokens were randomised on every attempt, so nothing could be hardcoded.

## The solve

The reproduction followed the incident one step at a time, all in one session. The solver read the request log and pulled the target of the single unsigned fetch record, created a fetch event for that token on the dispatch route, and verified it at the audit route, which disclosed the commands the worker would accept and the resource it could read. It ran the command that read the objective resource through the worker route — the SSRF-to-execution step the incident turned on — then read the evidence route, which returned the executed event and the schema the fix had to match.

With the break reproduced, the second half was the repair. The detector described the offending event: the kind of unsigned event that had executed, its signed flag false. The repair set the three controls the schema asked for — require a signed event, block the internal fetch path, and restrict the worker to an allowlist that kept only the legitimate status command. Submitting it to the response route returned the grader's verdict in the `evidence` field: the incident was detected and remediated, and the signed path's regression checks still passed. That evidence value was the proof.

The point lived in that allowlist. Turning the worker off would have blocked the attack and also broken the legitimate signed status check the application depends on, so the graded fix had to be narrow: reject the unsigned path, keep the signed one. That is the difference between a patch that ships and one that gets rolled back on Monday.

## Making it deterministic

The procedure went into `websolve.py` as `solve_fullstack`, folded in with the rest of the day's recoveries and committed at 09:45 on 31 October. The day's pre-commit replay gate passed on that commit — 691 deterministic-lane attempts replayed in 577 seconds with nothing regressed.

Three things keep it from being a one-morning script. The classifier recognises the shape from two signals the service discloses — a request-log route together with a worker query field — so the capstone is never mistaken for a plain SSRF target with similar routes. The solver discovers every route, field and token from the live service rather than assuming any, because all of it is randomised per attempt. And it reads the proof from the JSON `evidence` field first, the convention across the late web days, before falling back to a token scan.

Because web targets expire, none of this replays from a static corpus the way the byte-artifact lanes do. The lane's regression guarantee is instead a live self-test that re-runs solved web challenges against fresh, non-scoring variants, so a later change that broke this solver would show up there rather than on a release morning.

## Timed modes

The timed modes reused the same chain. The time trial's single field came back CORRECT at 09:12:28, the one exact time recorded for the challenge. The untimed single and the mastery are logged CORRECT by 11:58:29 — upper bounds from the supervisor's end-of-morning summary, after the automated first pass at 09:00:41 had missed. The agent's own notes put the finish in the crash-recovery window around 09:34.

## Dead ends

- **The first pass classified it as plain SSRF and missed.** At 09:00 the supervisor's single-class solver tagged the target `ssrf`, then `unknown`, and banked nothing. Right instinct, wrong scope: the fetch-to-worker step is server-side request forgery, but the challenge also needed the log reconstruction and the graded remediation, which a single-class solver cannot produce. A dedicated solver for the whole chain turned the miss into a solve.

## Takeaways

1. **A trust flag is only as good as its check.** The service believed an event was signed because its token matched the queue. Verifying authenticity has to mean verifying a signature, not re-checking a value the caller already controls.
2. **The graded fix was the selective one.** Blocking the worker outright would have stopped the attack and broken the signed status check the app needed. The repair that passed required a signed event and allowlisted the one legitimate command.
3. **Reconstruct from the evidence you already have.** The request log named the forged event outright; the fastest route to reproduction was reading the record, not guessing the attack.
4. **Offence and defence are one skill.** The capstone rewarded reproducing the incident and then closing it — real incident work, far more than a flag on its own.
