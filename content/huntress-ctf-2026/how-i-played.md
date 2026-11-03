+++
title = "How I played: an AI agent in the arena"
date = 2026-11-02
draft = true
layout = "series"

description = "A month of daily Huntress CTF challenges worked by an AI coding agent and a pipeline of deterministic solvers, from the 9am release race to using the grader as an oracle."

tags   = ["ctf", "automation", "ai-agents", "reverse-engineering", "malware-analysis"]
skills = ["Automation & Tooling", "Security Research"]
toc    = true
+++

<!-- Ported verbatim from the private repo's blog/content/projects/huntress-ctf-2026-ai-arena.md
     (drafted during the event). Source material: WRITEUP_NOTES.md, HANDOFF.md, notes/claude-memory/.
     TODO (publish day): headline result is now known — 63rd of 1,602 teams, 1,880 points, 560/561 modes;
     153 commits; the only miss was SHA1-Hulud. Fill the empty sections from the notes. -->

<!-- Source material: WRITEUP_NOTES.md (dated entries). Deep dives:
     writeups/huntress-ctf-2026-binary-hcfg.md and writeups/huntress-ctf-2026-script-analysis.md -->

Huntress CTF 2026 was billed as an **AI Arena**. Every player got an *AI Homebase*, a VM with an AI teammate built in. Challenges didn't come from a web page. They came from a **Game Master**, an API that hands out each challenge and its files and grades the answers. There were five lanes: warmups, metadata forensics, Android, script analysis and binary reversing. A sixth, web exploitation, arrived late. Each lane got a new challenge every morning at 9:00 ET for 31 days, and each challenge came in three modes.

An event built around an API is an invitation to automate, so that's what I did. I built a pipeline that grabs each challenge the moment it drops, solves it with deterministic code and submits the answer. An AI coding agent, Claude Code, wrote most of that code and extended it every day as new formats appeared.

<!-- TODO (publish day): headline result, i.e. final placement, score, and the best release-to-15/15 time. -->

This isn't a story about an AI winning a CTF while I watched. The agent wrote most of the code: nearly every one of the repo's 100+ commits is co-authored by Claude. My job was the part that decides whether automation is any good: the rules it plays by, the order it does things in, when to stop guessing, and the handful of answers that neither the agent nor the event's own AI could find. Where a human made the difference, I'll say so.

<!-- Austin: check the paragraph above matches how you'd describe your role, and update the commit count. -->

## The setup

### The Game Master

The Game Master is reachable two ways. One is a proxy inside the CTF network, which the Homebase VM is wired into. The other is a public HTTPS endpoint you can use from anywhere after a one-time pairing, which returns a personal bearer token. Pairing meant the whole pipeline could run on my own laptop, and the Homebase VM only had to be on when I wanted its AI.

The API is small: `list` the challenges, `start` an attempt (which returns the question and its answer format), download the `artifact`, `submit`, `retry`, and check `status`. It also serves its own OpenAPI description, which turned out to matter more than I expected; more on that later.

Answers are structured. A challenge asks for a set of named fields, and each field declares a format: exact text, an integer, a JSON array. The declared format, not the field's name, decides how an answer has to be spelled. That distinction comes back again and again.

### Three modes, three clocks

Every challenge came in three modes:

- **Single:** the day's challenge, untimed.
- **Time trial:** a fresh variant of the same challenge against a countdown, only a few seconds long early in the event.
- **Mastery:** a bundle of variants, also timed, which only unlocks once the time trial is correct.

Five lanes times three modes is **15 solves a day**. The rules around those clocks changed more than once during the month, and each change reshaped the pipeline.

### The pipeline

The hot path has no model in it. Each lane has a **deterministic solver**: given the artifact's bytes and the question text, it produces the answers or gives up. A generic timed runner goes from `start` to download, solve and `submit` in about 1.5–3 seconds, which is what a 5–8 second timer demands. The AI's job is to *write* solvers, not to answer questions live.

A **daily runner** wakes up at 8:50 ET from both cron and a systemd user timer, so a missed wake-up still gets caught. It polls the Game Master until the new day appears, then runs every lane in parallel. Within each lane it does the single first, then the time trial and mastery once the single comes back correct. Whatever the sweep can't solve goes to triage: first an agent per lane, then me.

The solvers are almost all standard-library Python. The binary lane parses ELF, PE and Java class files with `struct`, not a disassembler, and the script lane runs a few inert decoder functions in a Node `vm` sandbox. The evidence zips were WinZip-AES encrypted, and the laptop had no 7-Zip, so one of the first things the agent wrote was a 30-line AES-CTR + PBKDF2 extractor.

### The one rule: never guess

The pipeline submits only when **every** field has an answer it actually derived. If a question's format is unknown, the challenge is skipped, not guessed. A wrong submission can burn a timed attempt. More importantly, cycling through plausible answers until one sticks is brute-forcing the flag, and that's not solving the challenge.

That rule cost points. Some fields sat unanswered for days while plausible guesses were right there. It also forced the pipeline to *understand* every answer it gave, and that understanding is what let it fix itself later in the month. The line got finer as the month went on, between guessing a *fact* and trying another *spelling* of a fact the solver had already derived. That's its own section below.

<!-- Austin: be upfront about where the line ended up. Two places to address:
     1. binsolve.py submits spelling alternatives for unconfirmed architecture names (_ARCH_GUESS:
        aarch64 -> arm64, etc.). That's the same derived fact, re-spelled.
     2. The Day 17 one-field label probe (~900 single-field submits to learn the generator's vocabulary)
        is closer to guessing than anything else in the event. Say why you were OK with it,
        or that you'd draw the line differently now. -->

### Who did what

- **Claude Code**, on my laptop: wrote and extended the solvers, chased down rejections, and kept a replay corpus of every past attempt so a fix for today couldn't break yesterday.
- **The Homebase AI**, the event's own teammate: some answers were short labels from the challenge generator's own vocabulary, like the form a Batch variable expansion takes. Asking it with the challenge's exact wording, framed as "what's the short label for this," got answers neither of us could derive.
- **Me:** the rules, the triage order, and the stubborn cases. The clearest one was a binary field that wanted the ELF's *entire* symbol table in stored order, where every narrower reading had been rejected.

## Six lanes, one secret in different clothes

<!-- Warmups, mobile, metadata, script analysis, binary, and the late web lane, one paragraph each,
     linking to the two deep dives. -->

## The grader as an oracle

<!-- Atomic submits with banked partials, so bisection finds the bad fields in about 2·log2(n) submits.
     "Fix by spelling, not by guessing": sorted JSON, braced GUIDs, padded hex, x86-64 vs amd64. -->

## Racing the 9am drop

<!-- Cron and suspend, stale day markers, the self-inflicted 429s, the ranking model
     (release to the last CORRECT), run_for_time and the speed boards. -->

## When the automation bit back

<!-- The /tmp tmpfs quota, the fork-safety bug, the time-trial-before-mastery 409s,
     and the replay gate catching what the live run didn't. -->

## Results and lessons

<!-- Final score and placement, per-day timing from Day 16 onward, and what I'd do differently. -->
