+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Crumb Trail"
date = 2026-10-15  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day15-crumb-trail"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 15 (2026-10-15), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-15-credential-store-clues
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = true                    # true → appears in the hub's "Start here"

description = "A fresh time trial scored the Batch expansion question by a different line than two weeks of history; bisecting the submission found the four bad fields in about 40 seconds."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["scriptsolve.py", "timed.py", "heal.py", "replay.py", "bench.py", "python"]   # shown at the bottom + browsable
tags   = ["malware-analysis", "batch", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = true
+++

Crumb Trail is the day an answer key changed under a question the script lane had asked since Day 3. The single went through at release. The time trial, generated fresh that morning, had four of its 1,026 answers wrong, all from a rule that two weeks of accepted answers had confirmed. The recovery used the grader as an oracle, leaned on a replay corpus that stopped a fix which would have broken 140 old answers, and ended in a self-healing submit committed by 09:52.

## The challenge

Script Analysis was cumulative: each day's bundle asked every earlier family's questions again and added more. Day 15 added Perl polyglots and a Perl host.

The field that mattered dated from [Expansion Pack](/huntress-ctf-2026/day03-expansion-pack/) on Day 3: for each of the nine Batch files, a label for its variable-expansion form. On Day 15 the question read: "Classify only the expansion form used by the descriptor reconstruction statement. Ignore output, echo, host-envelope, and separator-noise lines." The notes disagree on whether that wording was new. The handoff written that morning says it was; the write-up notes from the same commit say it hadn't changed.

The single was a static variant, made ahead of release. The time trial and the mastery were generated when each attempt started.

## Reading the prompt

The prompt tells a credential-theft story about a browser's stores and a store that was never there. It says nothing about Batch, which is where this lane's trouble came from. Read literally, the Batch question's Day-15 wording names the line the time trial scored, the reconstruction statement, and says to ignore echo lines. The solver followed the grader instead: since Day 3 the accepted label had been the form on the echo line.

## What was in the files

The single and the time trial each delivered one AES-encrypted evidence ZIP; the mastery's bundle held one per set. Inside, each Batch file carries its descriptor encoded on a `HUNTRESS-MATERIAL` line. A rebuild line reassembles the recovered configuration from fragment variables, an `echo(` line consumes it, and `neutral_*` variables and separator lines are noise. The decoded descriptor answers most of a file's questions; the expansion label describes the code around it.

`_bat_render_form` in `scriptsolve.py` finds the rebuild line, the last `set` that assembles a value from `%` or `!` references outside the noise, and sorts it by syntax: a FOR loop, a `call set`, `!v!` references or plain `%v%` ones. So the expansion question has two candidate lines. For a `!v!` rebuild consumed by `echo(!v!)` they agree; for a `%v%` rebuild they don't.

## The solve

At 09:00 the supervisor ran the lane unattended. The single went through under the old rule: confirmed fields first, then five expansion fields the bytes can't decide, FOR-loop and bare `call set` rebuilds, through the capped two-try I'd approved on 7 October, each accepted on its first label. The time trial's first submit was rejected, and the mastery wouldn't start. The script lane's lines from the supervisor log, other lanes cut:

```text
 ids 1026 ids deadline None sol {} t+6.29s
 submit (confirmed fields) -> incorrect  t+7.42s
 two-try: a confirmed field was rejected; ambiguous fields not tried
...
[2026-10-15 09:00:31] 2026-10-15 day 15 (18s after release was seen)
  script-analysis-day-15-credential-store-clues: CORRECT
  script-analysis-day-15-credential-store-clues/time_trial: incorrect
  script-analysis-day-15-credential-store-clues/mastery: error: Game Master returned HTTP 409
```

The rest was fixed in session by Claude Code, the coding agent that built most of the pipeline, using the grader itself. One wrong field rejects a whole submit and banks nothing, but an all-correct partial submit is accepted and stays banked, so any subset of answers can be tested. Bisecting the submission found the four bad fields in about 20 submits and 40 seconds; checking the fields one at a time had taken more than eight minutes.

They were Batch expansion labels. The fresh time trial scored the rebuild line's form, where the static single and every attempt since Day 3 had scored the echo line's. The agent switched on `RECON_STATEMENT` in `scriptsolve.py` for timed attempts from Day 15, which makes the expansion field read the rebuild line, and all nine of the time trial's expansion labels were confirmed. The mastery, five sets of the same questions, was CORRECT at 09:18:55. It was the last of the day's 15 modes, and finishing then moved us from 55th to 34th.

{{< callout type="warning" title="Same question, two answer keys" >}}
Two weeks of accepted answers confirmed the echo-line rule only for variants generated before the key changed. The static single, made ahead of release, was one; the time trial and mastery weren't.
{{< /callout >}}

## Making it deterministic

The rule went in first: `solve_offline` in `timed.py` sets `RECON_STATEMENT` from the attempt and its questions. The first version regressed 140 past fields in the replay corpus, so it was narrowed to time trials and masteries from Day 15 with that wording. Committed at 09:27, it replayed 225 attempts with 0 regressions.

Then the method. A wrong field used to stop a mode until it was fixed in a session. I approved letting the pipeline try format variants and the other allowed values of fixed-choice fields itself, and `heal.py` was committed at 09:52. Every runner now submits through it: one full submit; if that's rejected, bank the confident fields, bisect the rest, then try each rejected field's alternates, other allowed values and format variants, one field per submit. The bisection order encodes the morning's lesson:

```python
def kind_of(aid):
    """Field kind: answer id without its setN. prefix, digit runs folded (d13-msi-002-x -> d#-msi-#-x)."""
    return re.sub(r"\d+", "#", re.sub(r"^set\d+\.", "", aid))


def family_key(aid):
    """Bisection order: the kind's words reversed, so every '*-expansion', '*-guid' or
    '*_machine' field (any role, set or day) sits in one contiguous block -- a rule that broke
    for a kind of field then fails as one block and bisects in a few submits."""
    return tuple(reversed(re.split(r"[-_.]", kind_of(aid)))), aid
```

Simulated on this time trial's real failure, it fixed it in 26 submits, about 10 seconds. Each fix is logged to `heal-log.jsonl` to be folded back into the solver, replayed and committed.

The rule lasted a day. The handoff had said to try the rebuild-line rule if a Day-16 single missed on expansion, and the [Day 16](/huntress-ctf-2026/day16-same-same-but-different/) single did; `heal.py` recovered by itself in 23 submits and 18 seconds. Fresh variants of Days 7 to 9 scored the rebuild line too. The key followed the challenge generator, not the day. `recon_rule` in `timed.py` sets the boundary at `RECON_ERA`, 13:00 UTC on 15 October, which is the 09:00 ET release. Variants generated from then on take the rebuild line; older ones, the static singles of Days 1 to 15 among them, take the echo line. The replay corpus stores when each case was recorded and passes that time in, so old cases keep the old key.

## Timed modes

The time trial had no clock of its own (`deadline None` above): the runners weren't yet setting `run_for_time`, the flag for a ranked, timed attempt, found in the API's OpenAPI description later that day. The clock that mattered was the board's: ties on points go to whoever got there first, which I explained to the agent that day. Before Day 15 we were 55th of 86 teams tied at 720 points, and the leader finished all 15 Day-15 modes in under two minutes. One miss costs more than any amount of shaved latency saves.

The mastery, refused in the 09:00:31 summary, could only follow the time trial, which was CORRECT at 09:17:52. A 12:27 CORRECT recorded for it that afternoon is a later `bench.py` re-run on a fresh variant, unranked and scoring nothing: one submit, 6.4 seconds end to end.

## Dead ends

- **Trusting a confirmed field.** The two-try covers only fields the bytes can't decide; the wrong labels were among fields earlier variants had confirmed, so it never ran.
- **The first version of the rule.** Applied more widely, it regressed 140 past fields in the replay corpus.
- **Reading the 409 as the single-first lock.** The 09:52 commit also ran each lane's time trial and mastery in parallel after the single. The next morning three lanes' masteries got HTTP 409: a mastery waits for its time trial. The Day-15 409 had followed a failed time trial, and in 44 solved pairs no mastery had finished first, but nobody had checked.

## Takeaways

1. **An answer key can move under the same question.** It followed the challenge generator, not the day, so every replay case keeps the time it was recorded.
2. **A grader that banks correct partials is an oracle.** Bisection found four bad fields among 1,026 in about 20 submits.
3. **Gate every fix against history.** The replay corpus stopped a first fix that would have broken 140 past answers.
4. **Turn the session's method into the pipeline's.** `heal.py` was committed by 09:52, and on Day 16 it handled the next change to the key by itself.
