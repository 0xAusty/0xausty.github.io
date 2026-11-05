+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Double Spent"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-double-spent"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "web" (Web Exploitation), web_no 21
#   gm_id web-exploitation-day-21-double-spent
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A one-shot credit redeemed by a non-atomic check-then-decrement, raced with concurrent requests so the balance goes negative, with recon kept read-only so a serial probe can't brick the target."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
solved_by = ["agent"]

tools  = ["websolve.py", "huntress_harness.py", "python"]
tags   = ["web-exploitation", "race-condition", "toctou", "time-trial", "mastery"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = true
+++

Double Spent was the [Web Exploitation](/huntress-ctf-2026/lanes/web/) lane's twenty-first challenge and the slowest of its morning to fall. Its single asked for one proof from one live target, and the prompt gave the method away: a ledger that cannot count a credit spent twice. The trap was around it. The credit is one-shot, so the first careless request spends it and bricks the instance. That happened on the first run and turned a one-line bug into the long pole of the morning.

## The challenge

The web lane has no downloadable artifact. Each attempt hands back a live site on a short time-to-live, and the proof sits on the target rather than in any bytes. Here the target was a Rails application holding an instance-global credit meant to be redeemed once. The single wanted the proof recovered from that one target as `exact_text`. The time trial was the same field under the clock. The mastery bundled four targets of different types, each classified on its own.

One grader convention shaped the parsing across the whole lane: the proof comes back as a JSON `evidence` field, not under the obvious proof-named key. A scan for that key alone would have walked straight past it.

## Reading the prompt

The prompt is unusually direct and names the class outright.

| Phrase | Implication | What the solver did |
|---|---|---|
| "One credit, two purchases" | A single, one-shot credit that should spend exactly once. | Treated the credit as a one-shot resource: recon read-only, never spend it by hand. |
| A ledger that "can't count what it can't see coming" | The balance check and the decrement are not atomic; a concurrent arrival slips between them. | Looked for a check-then-decrement redeem that commits its write late. |
| Its instruction to spend the same credit twice | Several redeems at once, so more than one clears the balance check before any writes the decrement. | Ran a synchronised burst of redeems while the balance was still one. |

## What was on the target

Two routes mattered. A redeem route performed the privileged action; it accepted only POST, so a GET came back as "method not allowed". An audit route reported the balance over a safe GET and, once the balance had gone negative, carried the proof in its `evidence` field.

The shape is a classic time-of-check/time-of-use (**TOCTOU**) race. The redeem path reads the credit, decides it is positive, and only then writes the decrement. Between the read and the write there is a window, and the application holds a single global credit for every caller to contend over. Nothing in one request on its own is wrong; the defect only appears when two overlap.

## The solve

The first job was telling this target apart from its neighbours. Its nearest look-alike is a server-side request forgery challenge: it exposes the same pair of routes and also answers 403 on the audit route, so a naive classifier reads double-spend as SSRF and tries the wrong attack. The discriminator is read-only: a Rails server, a redeem route that rejects a GET as POST-only, and the words *credit* and *overspent* in the audit body. All of that is learned with safe GETs, which spend nothing.

With the class fixed, the race itself is short. The solver opens a set of connections ahead of time, holds them at a barrier, and releases them together so the redeems land as one burst while the credit is still one. Several clear the check before the first decrement commits, the balance drops below zero, and the audit route then returns the proof in its `evidence` field. The solver reads it there and submits.

What made this safe is that the solver never issues the redeem outside the race. A single serial POST would spend the one-shot credit and leave a dead instance behind, so every touch of the write path happens inside the concurrent burst.

## Making it deterministic

The procedure went into `websolve.py` as `solve_doublespent`, with the classifier ordered to detect double-spend before SSRF. Three things keep it from being a one-morning script.

It recons read-only. The classifier and the clue read use GETs only, so running the solver against a fresh target never spends the credit by accident.

It reads the `evidence` field first, then falls back to a pattern scan. That is the lane-wide convention, shared with the forwarded-header shape released the same day and the webhook shape from the day before.

It heals a target it has already spent. Because a spent single leaves a bricked one-shot credit, a `GameMaster.reset()` call was added to the harness and wired into the run: an untimed single that comes back with the balance already below one is reset to a fresh instance before reconnecting, so a bricked target repairs itself instead of failing the day. The reset is gated to the untimed single, because issuing it against a running timed attempt would end the ranked run; a timed retry already hands back a fresh credit, so the race just runs first.

## Timed modes

Both timed modes used the same race. The time trial asked the one field under the clock and came back CORRECT at 09:24:22, a little over a minute after the single. The mastery was a compounding bundle of four targets, the day's double-spend alongside siblings of earlier types, each classified independently. The first submit was accepted with three of its proofs rejected before the bundle went CORRECT.

The single did not bank until 09:22:56, roughly twenty-three minutes after the drop, while the rest of the day's fifteen deterministic modes had finished by 09:00:43. The mastery went CORRECT at 09:26:14.

## Dead ends

- **The serial probe that bricked the target.** On the first run the agent reconned the redeem route the obvious way, with a request that spent the single credit, and the instance was dead until a Game Master reset brought it back. That cost the bulk of the twenty-odd minutes and drove the self-healing reset above.
- **Misreading it as SSRF.** Before the classifier learned to check for Rails and the POST-only redeem first, the shared feature-and-audit route pair pushed the target down the SSRF branch, which cannot drive a balance negative. Detecting double-spend first, from safe signals, was the fix.

## Takeaways

1. **The bug is non-atomic check-then-act; the fix is atomicity.** Decrement under a row lock or a conditional update that cannot go below zero, or make the redeem idempotent, and the window the race depends on disappears.
2. **A one-shot resource makes recon dangerous.** When an action can be taken once, read-only reconnaissance and touching the write path only inside the exploit is the difference between a solve and a bricked target.
3. **Look-alike classes need a safe discriminator.** Double-spend and SSRF present the same routes; a GET-only fingerprint separated them without spending anything.
4. **Build the recovery in.** The bricking became a gated `reset()` that heals the next spent single on its own, so the same mistake could not cost a second morning.
