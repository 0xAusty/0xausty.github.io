+++
title = "How I played: an AI agent in the arena"
date = 2026-11-02
draft = true
layout = "series"

description = "A month of daily Huntress CTF challenges worked by an AI coding agent and a pipeline of deterministic solvers, from the 9am release race to the grader as an oracle."

tags   = ["ctf", "automation", "ai-agents", "reverse-engineering", "malware-analysis"]
skills = ["Automation & Tooling", "Security Research"]
toc    = true
+++

<!-- Ported from the private repo's blog/content/projects/huntress-ctf-2026-ai-arena.md (drafted during
     the event) and finished on 3 Nov from the research fact sheets (facts/timeline.md). Each passage
     followed by "Austin: confirm" was corrected for attribution or states a stance for you to check. -->

Huntress CTF 2026 was billed as an **AI Arena**. Every player got an *AI Homebase*, a VM with an AI teammate built in: the event's Homebase AI (GPT-6 Luna), provided by Huntress. Challenges didn't come from a web page. They came from a **Game Master**, an API that hands out each challenge and its files and grades the answers. There were five lanes: warmups, metadata forensics, Android, script analysis and binary reversing. A sixth, web exploitation, arrived late. Each lane got a new challenge every morning at 9:00 ET for 31 days, and each challenge came in three modes.

An event built around an API is an invitation to automate, so that's what I did. I built a pipeline that grabs each challenge the moment it drops, solves it with deterministic code and submits the answer. An AI coding agent, Claude Code, wrote most of that code and extended it every day as new formats appeared.

The result: 63rd of 1,602 teams (2,304 players), with 1,880 of 1,885 points and 560 of 561 modes. The one miss was SHA1-Hulud, a standalone reverse-engineering challenge added on Day 30, still unsolved when the event closed. The fastest complete release morning was Day 18: all 15 modes CORRECT by 09:03:45.

This isn't a story about an AI winning a CTF while I watched. The agent wrote most of the code: 146 of the repo's 153 commits carry Claude's co-author line. My job was the part that decides whether automation is any good: the rules it plays by, the order it does things in, when to stop guessing, and where to take a question the pipeline couldn't answer. I didn't solve any challenge by hand. Where an answer came from the agent in a live session, from the Homebase AI or from my own ChatGPT account rather than from the pipeline, I'll say so.

<!-- Austin: confirm -->

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

A **daily runner** wakes up at 8:50 ET from both cron and a systemd user timer, so a missed wake-up still gets caught. It polls the Game Master until the new day appears, then runs every lane in parallel. Within each lane it does the single first, then the time trial and mastery once the single comes back correct. Whatever the sweep can't solve goes to triage: first an agent per lane, then a live session with me at the laptop, steering the agent or putting the question to the Homebase AI.

<!-- Austin: confirm -->

The solvers are almost all standard-library Python. The binary lane parses ELF, PE and Java class files with `struct`, not a disassembler, and the script lane runs a few inert decoder functions in a Node `vm` sandbox. The evidence zips were WinZip-AES encrypted, and the laptop had no 7-Zip, so one of the first things the agent wrote was a 30-line AES-CTR + PBKDF2 extractor.

### The one rule: never guess

The pipeline submits only when **every** field has an answer it actually derived. If a question's format is unknown, the challenge is skipped, not guessed. A wrong submission can burn a timed attempt. More importantly, cycling through plausible answers until one sticks is brute-forcing the flag, and that's not solving the challenge.

That rule cost points. Some fields sat unanswered for days while plausible guesses were right there. It also forced the pipeline to *understand* every answer it gave, and that understanding is what let it fix itself later in the month. The line got finer as the month went on, between guessing a *fact* and trying another *spelling* of a fact the solver had already derived. That's its own section below.

Three exceptions carry my approval on record: on 7 October a capped two-try for the one Batch label the bytes could not decide (never a third label), and on 15 October the self-healing submit (format variants and the other allowed values of fixed-choice fields) and closest-name guesses for unknown metadata and binary fields, built only from values parsed from the artifact.

Two places went further with no approval recorded. `binsolve.py` maps each file's machine code to the grader's spelling of the architecture, but only three spellings are confirmed; for any other it submits the spelling that follows their style, then alternates (an ARM64 build goes in as `aarch64`, then `arm64`). The machine code comes from the bytes; only the spelling is a guess. It may fall under the format-variants approval, and I'm comfortable with it: it re-spells a derived fact rather than inventing one.

<!-- Austin: confirm -->

The other is the Day 17 label probe, the closest the month came to brute force. The binary bundle wanted a generator label for how each build stored its config record, which no parser could supply. A one-field submit returns `accepted` when that field is right, so the agent's session tried candidate labels one at a time: about 900 submits over roughly 25 minutes. Those were guesses. The notes already named the alternative: ask the Homebase AI, use an organiser hint, or wait for a question that lists the allowed values. That's the line I'd hold now.

<!-- Austin: confirm -->

On the last day the rule broke outright. With SHA1-Hulud open and submissions free and untimed, about 60 themed guesses went in, then 23 more, all wrong. That was guessing, and it didn't work.

<!-- Austin: confirm -->

### Who did what

Answers came from four places, and each challenge page's card names the ones behind it:

- **The pipeline, on its own:** the daily runner and the lane solvers, with nobody in the loop. On Day 27 it banked every mode of the five standard lanes by 09:00:43.
- **Claude Code, in session:** wrote and extended the solvers, chased down rejections, and kept a replay corpus of every past attempt so a fix for today couldn't break yesterday. It also fixed release-morning misses live with me at the laptop (the notes say "hand-fixed"; the hands were the agent's).
- **The event's Homebase AI:** some answers were short labels from the challenge generator's own vocabulary, like the form a Batch variable expansion takes. Asking it with the challenge's exact wording, framed as "what's the short label for this," got answers neither of us could derive. It also supplied the script control-flow labels and masteries for Days 4 to 7, the Day 1 ELF symbol field, the PE symbol spelling in the [Mangled](/huntress-ctf-2026/day02-mangled/) mastery and the [Trust the Webhook](/huntress-ctf-2026/day26-trust-the-webhook/) recipe.
- **My own ChatGPT account,** used when Claude hit its usage limit. It built SHA1-Hulud's first emulator and, with the Homebase AI, produced the Day 23 script time trial and mastery ([Press Start to Decode](/huntress-ctf-2026/day23-press-start-to-decode/)) after the agent's own attempt stalled.
- **Me:** the rules and their exceptions, the goals, the triage order and the approvals; outside facts like the scoreboard's tie-break and Discord's word on SHA1-Hulud; and jobs the agent couldn't do, like pairing the Homebase VM. The stubborn cases I took to an AI rather than solving them myself. The clearest was a binary field that wanted the ELF's *entire* symbol table in stored order, where every narrower reading had been rejected: the answer came from the Homebase AI once I put the question to it.

<!-- Austin: confirm -->

## Six lanes, one secret in different clothes

Each lane kept one thing constant and changed its clothes every day.

**[Warmups](/huntress-ctf-2026/lanes/warmups/).** Every blob decoded to the same 87-character prefix plus a three-word slug, with a new encoding added each day, so decoding became checking: `wusolve.py` tests each reading against the known sentence and `kpa.py` recovers cipher keys from it. [Seven Steps](/huntress-ctf-2026/day14-seven-steps/) is the day an old fallback accepted gibberish.

**[Mobile](/huntress-ctf-2026/lanes/mobile/).** For 22 days each APK hid its answer code in `assets/huntress_puzzle.json` under a new encoding. On Day 23 the timed modes computed the code inside `classes.dex` instead, so the agent wrote a DEX disassembler, a small Dalvik interpreter and an x86-64 interpreter for the JNI side: [Hook Line and Signal](/huntress-ctf-2026/day23-hook-line-and-signal/).

**[Metadata](/huntress-ctf-2026/lanes/metadata/).** From Day 3 every question read *Determine `<format>.<field>` for `<member>`*, over a new file format almost every day. `metaengine.py` turned that into one pipeline, which started with 37 parsers on 14 October; by 20 October the lane had 68. The finale, [No Artifact Left Behind](/huntress-ctf-2026/day31-no-artifact-left-behind/), planted a decoy loop beside the real execution chain.

**[Script](/huntress-ctf-2026/lanes/script/).** Every carrier, whatever the language, hid an encoded blob and a codec hint that decoded to a key=value descriptor, and no carrier was ever run as delivered. The hard part was a label: [Expansion Pack](/huntress-ctf-2026/day03-expansion-pack/) asked for each Batch file's variable-expansion form, and on [Crumb Trail](/huntress-ctf-2026/day15-crumb-trail/) the answer key changed.

**[Binary](/huntress-ctf-2026/lanes/binary/).** Build after build hid the same `HCFG` record, XOR'd JSON behind a CRC32-checked header, somewhere new: an ELF section, Base64 in a Java constant pool ([Pool Party](/huntress-ctf-2026/day06-pool-party/)), a string literal in a 67 MB Swift binary ([Swift Justice](/huntress-ctf-2026/day08-swift-justice/)), with a bad-CRC decoy in the Rust build. One extractor, `binsolve.py`, handled the cumulative bundle, so half the battle was spelling: in [Mangled](/huntress-ctf-2026/day02-mangled/) the same C++ symbol needed a different string on a MinGW PE. [SHA1-Hulud](/huntress-ctf-2026/day30-sha1-hulud/) got away.

**[Web](/huntress-ctf-2026/lanes/web/).** The sixth lane arrived on 19 October with its own numbering: live, expiring targets with the proof on them, and masteries that bundled several apps. The rule was to solve each vulnerability class once, fold that concrete procedure into `websolve.py`, and never pre-build a generic attack framework. [Double Spent](/huntress-ctf-2026/day27-double-spent/) was a race on a one-shot credit; [Full Stack Incident](/huntress-ctf-2026/day31-full-stack-incident/) wanted a repair as well as the exploit.

## The grader as an oracle

Two behaviours made the grader useful as well as strict. One wrong field rejects a whole submit and banks nothing, but an all-correct partial submit is accepted and stays banked. And a wrong submit doesn't end a timed attempt by itself; only the deadline does. That makes the grader a **membership test**.

It was first used that way on Day 6: submitting the script lane's 399-field single one field family at a time and bisecting turned the grader's `remaining` counter into a debugger. Bisection needs about 2·log₂(n) submits, and grouping fields by family makes a broken rule fail as one block. On Day 15 it found the 4 bad fields among 1,026 in about 20 submits, where checking them one at a time had taken more than eight minutes.

`heal.py`, committed later that morning, made it automatic: bank the confident fields, bisect the rest, then try each rejected field's alternates, other allowed values and format variants, one submit at a time. That's *fix by spelling, not by guessing*: the same derived value as sorted JSON, a braced GUID, hex padded to the field's width. A transform that works is remembered and pre-applied to the same challenge's later modes. The log holds 52 such fixes from 16 to 28 October.

The spelling rules came from rejections: a PE entry point wanted hex padded to the full 32 bits, and the ELF class was text on Day 1 but a bit width on Day 8.

## Racing the 9am drop

The board ranks by points, with ties going to whoever reached the score first. On 15 October I explained that to the agent, and it changed the goal: since most teams near the top solve everything eventually, each day is a race from release to the *last* CORRECT. That day 86 teams were tied with us at 720 points, and we were 55th.

The schedule failed first. On Day 8 the 08:50 cron never fired, because the laptop was in suspend; on Day 9 it fired but chased Day 8, because the stored day marker was stale. The fix derived the day from the Game Master's live status, cleared any backlog and ran from a Persistent systemd timer with cron retries behind it. The note that morning: the schedule is not the hard part; the state model is.

Then speed bit. On Day 11 five lane processes hit the Game Master at once and tripped each other into HTTP 429s; a 429 on a *submit* failed the binary time trial, and with no fresh variant published, the mastery behind it was locked too. That morning the agent added a token bucket shared by every lane, and a POST that draws a 429 now waits and resends. Concurrency without a shared throttle is a self-inflicted outage.

Day 15's automated pass had 7 of 15 modes by 09:00:31 and fixes in session finished at 09:18:55, moving us to 34th; the leader had finished all 15 in under two minutes. Day 16, 15/15 by 09:05:09, put us 13th. Day 17 finished by 09:33:55 but took us to 5th: its binary was the separator, solved by only eight teams when I checked.

The OpenAPI description held a surprise of its own: a request must set `run_for_time: true` to get a ranked, timed attempt, so three days of "Hall of Fame ineligible" were simply our runners never asking. The first ranked run placed 8th at 0.553 s against a 0.391 s leader. I approved a capped ranked loop and stopped it on 16 October, once more shots were mostly measuring the server.

By late October a release morning was built to run itself: preflight at 08:45, lane workers warm before the drop, a headless escalator spawning one agent per first-pass miss, and a supervisor that re-solved the affected modes within about 10 to 30 seconds of a saved fix.

## When the automation bit back

Most of the worst moments were self-inflicted, and each one left a rule behind.

**A full disk that wasn't the disk.** On Day 14 the binary mastery died with `Errno 122` on a drive 8% used: `/tmp` was a tmpfs with a per-user quota, holding about 6.1 GB of evidence folders the solvers never deleted. An `rmtree` in a `finally` fixed it. Check every mount, not just `/`.

**A fork that shared a socket.** Forking the timed modes after the single had opened a keep-alive TLS connection left both children on one socket, and every first request failed and backed off. Each child now gets its own connection pool.

**A rule nobody had tested.** On Day 16, starting time trials and masteries together got three masteries an HTTP 409: the mastery unlocks only once the time trial is CORRECT. In 44 solved pairs, no mastery had ever finished first. We hadn't asked the data that question.

**A gate that caught what the live run didn't.** Every attempt went into a replay corpus (691 attempts by 31 October), and a pre-commit hook re-solved past attempts with the learned keys cleared. On Day 19 it blocked the fold-in commit twice, on two faults the live run had hidden. The day's score was never at risk; the gate was protecting the solver, not the result.

**Operations, late in the month.** A Day 27 supervisor was found still holding the lock that would have silently skipped Day 28, and the escalator failed twice: on a Claude session limit on Day 30, and at a 600-second ceiling, with its five agents, on Day 31.

## Results and lessons

After 5th on Day 17, rank slid to 66th by Day 26 on late finishes and ended at 63rd.

From Day 16 on, the day's last CORRECT came by 09:05:09 on Days 16 and 18, and by 09:26:14 on seven more (Day 30 not counting SHA1-Hulud). The slow days were the label probe (Day 17, 09:33:55), web (Day 19, 10:16:22), a session that died (Day 23, 10:32:39), the laptop off at 9:00 and five new shapes (Day 24, 09:39:17), Trust the Webhook (Day 26, 12:30:09), an idle gap and a binary fix that missed the PE builds (Day 28, 09:53:20), and a crash-and-recover finale (Day 31, 09:33:08).

The official scoreboard also records five first bloods, the first of 1,602 teams to solve a mode, all in the metadata lane: the Day 23 [Page Me Maybe](/huntress-ctf-2026/day23-page-me-maybe/) time trial and mastery, about a minute ahead of the next team, and all three modes of Day 26 [Before You Go](/huntress-ctf-2026/day26-before-you-go/), the single 0.3 s ahead.

The miss, [SHA1-Hulud](/huntress-ctf-2026/day30-sha1-hulud/), was a stripped Rust PE with string encryption, anti-debugging and modified SHA-1 functions. After my own ChatGPT account built the first offline Unicorn emulator, Claude Code took it over: one session concluded the check was a one-way gate, and a later one showed that was wrong, found the emulator bug behind a long detour, and stopped a few steps from the end. I also put it to the Homebase AI. It stayed open.

What I'd take into the next one:

- **Coverage is speed.** Covered shapes solved in seconds; most of the lost time was one or two new shapes a day waiting for triage.
- **Read every miss first, fix the cheapest first.** Day 17's one-minute mobile fix waited behind the label hunt.
- **Agents for web, inline for the rest.** Parallel agents suit independent web targets; a lone deterministic miss pays a cold agent's start-up tax, as Day 22's binary did.
- **Escalate in minute one.** On Day 28 about 11 minutes passed before I noticed the misses. From 30 October every missed lane escalated automatically, which I chose even though I planned to be at the laptop.
