+++
title = "Script Analysis"
date = 2026-11-02
draft = true
layout = "lane"
lane = "script"
weight = 30

description = "Deobfuscating thirty-one script languages with nothing run outside an empty sandbox: recovery of each sample's embedded plan, validated against its own markers and mapped to MITRE ATT&CK."

tags   = ["malware-analysis", "deobfuscation", "powershell", "batch", "vbscript", "mitre-attack"]
skills = ["Malware Analysis"]
toc    = true
+++

Script Analysis was cumulative. Each day re-asked every earlier day on top of new material, so field counts climbed from 399 on Day 6 to 469 on Day 7, past 1,000 on Day 15, to 10,465 on the Day 23 mastery and 29,250 on the Day 31 mastery. The samples ran through PowerShell, JScript, Batch, VBScript, Python, Bash, Node.js, PHP, HTA and WSF, Lua and SCT, WMI MOF, TypeScript, AutoIt, AppleScript, MSBuild, Perl, Ruby, AutoHotkey, Google Apps Script, C#, Groovy and Jenkins, GitHub Actions, NSIS, GDScript, JSP, Elixir and Phoenix, Erlang, Dockerfiles, Terraform, Makefiles, BeanShell and XSLT.

None of it was executed outside an empty sandbox. Every sample was decoded statically or through its own inert decoder: JScript's `recover_*` functions in a Node vm, a tiny Python AST evaluator, re-implemented Bash recovery routines. Each decode was validated against the sample's own descriptor markers, and each sample was mapped to MITRE ATT&CK.

Two things kept coming back: the Batch variable-expansion "form", whose answer key changed with the challenge generator, and the grader as an oracle. A wrong field rejects the whole submit but an all-correct partial is banked, so the way through was to submit by family and bisect what failed.

## The shape of every sample

PowerShell carried a base64 JSON literal, JScript an inert function returning JSON, Batch to Node.js (Days 3 to 7) a material blob and a codec hint, and the polyglots and hosts from Day 8 a `HUNTRESS_ANALYSIS_V1` marker that decodes to the descriptor. The decoded plan, JSON for the first two and a `key=value` descriptor (`v=1|`, later `v=2` and `v=3`) for the rest, states most answers outright: adapter, campaign, stage count, steps and indicators, and from Day 8 role and technique. The questions followed it: role (an enum classified by the decoded graph's terminal intent), technique, exact-text indicators such as a URL or a mutex, and from Day 6 an integer stage count and ordered-token steps. On top sat the generator's own labels, which decided spelling: the grader wanted short generic names such as `if_guard` and `for_once`; descriptive phrasings failed.

## Running only the harmless parts

Claude Code, the coding agent that built most of the pipeline, wrote one front-end per language family; only one of them runs anything. `jsan.js` loads each JScript file into an empty Node `vm` context, calls only its inert `recover_*` function and reads the style labels off the `inspect_*` function's syntax with regexes. `pysolve.py` reads fourteen Python packagings with a tiny AST evaluator that understands only literals and string operations, so nothing "hatches". `bashsolve.py` reproduces each `Recover_` function's representation and transform in Python (`d[N-1-i]=e[i]^58` is reverse-then-XOR) and checks the result against the `v=1|` marker.

## Batch: four ways to expand a variable

[Expansion Pack](/huntress-ctf-2026/day03-expansion-pack/) on Day 3 asked which of four forms each Batch file used to expand a variable: `percent`, `delayed`, `call_double` or `for_indirect`. The obvious reading, the form on the rebuild line where the config is built, was wrong. The event's Homebase AI (GPT-6 Luna) found that the grader scored the line where the value is consumed, the `echo(!var!)`, and gave the last labels once the Game Master's prompt was quoted to it verbatim; the single went CORRECT on 5 October.

Two Day 3 files with the same FOR-loop rebuild scored different labels, so the agent made `bat_expansion` return `None` there and I approved a capped two-try: `for_indirect`, then `call_double` only on the fields still open, never a third. On [Crumb Trail](/huntress-ctf-2026/day15-crumb-trail/), Day 15, the key moved: a fresh time trial scored the rebuild line's own form, and bisecting the submission found the four bad fields among 1,026 in about 40 seconds. The fix is keyed to the variant's generation time, not the day; the replay corpus stopped a first version that would have regressed 140 past fields. On Day 16 the self-healing submit, `heal.py`, caught the next change alone in 23 submits and 18 seconds.

## One codec library, every language

Teaching the shared decoder Day 6's Bash codecs lifted the still-open Day 4 single from 215 to 222 fields and Day 5's from 343 to 346, and a fallback over every known representation and transform that keeps only a valid descriptor ended the per-variant whack-a-mole. On 15 October `bat.py` stopped searching up to 4,144 transforms per file and derived the key from the known `v=1|` prefix: 45 times faster, identical on all 657 corpus samples.

## New carriers kept arriving

Day 8, [Lost in Translation](/huntress-ctf-2026/day08-lost-in-translation/), changed the lane's shape: PHP polyglots and WSF, HTA and webshell hosts carried the `HUNTRESS_ANALYSIS_V1` comment, its descriptor states role and technique, `polysolve.py` answers by field name, and most later languages went through it unchanged.

Day 18's Google Apps Script split its payload across a string array behind a `SPLIT` marker; Day 19's C# sat in an ASPX string literal, where the hex payload ran into a `\n` escape. The fixes were just joining the array and stopping at the first escape. Day 23, [Press Start to Decode](/huntress-ctf-2026/day23-press-start-to-decode/), was the hard one: a layered `LYR` codec and opaque hex-id file names that broke every role-name lookup table. The agent handled the codec and reached 1,164 of the time trial's 1,495 fields; the rest, deriving role, technique and steps from the descriptor instead of file names, was finished in a separate session where I put the problem to the Homebase AI and my own ChatGPT account, and the 10,465-field mastery was accepted in one submit.

## Mapping to ATT&CK

The interpreter technique follows the language (T1059.004 Bash, .005 VBScript, .006 Python, .007 JScript and Node.js), and a staged chain ending in process dispatch keeps it even when its config also carries a cron path or service name. The best tell was a Node.js adapter calling itself `systemd_descriptor` whose indicator was a cron.d path: cron (T1053.003), not systemd. Two conventions the grader settled: `stage_count` is a declared field, not the step count, and a collection sample's secondary indicator is the first entry of its decoded file list, not the decoy archive beside it.

## Days worth knowing

- **Day 3 · [Expansion Pack](/huntress-ctf-2026/day03-expansion-pack/)**: the full write-up of the lane's signature puzzle and the capped two-try it produced.
- **Day 15 · [Crumb Trail](/huntress-ctf-2026/day15-crumb-trail/)**: the full write-up of the morning the answer key changed and `heal.py` came out of it.
- **Day 6 · [Shell We Begin](/huntress-ctf-2026/day06-shell-we-begin/)**: 399 fields across six languages, where per-family submits turned the grader's remaining counter into a debugger.
- **Day 23 · [Press Start to Decode](/huntress-ctf-2026/day23-press-start-to-decode/)**: a layered codec and opaque file names turned an automatic lane into a 93-minute recovery.
- **Day 31 · [The Full Transform](/huntress-ctf-2026/day31-the-full-transform/)**: 29,250 fields across thirty-one languages, solved automatically by code last changed on 24 October.

## Takeaways

- **Validate every decode against something the sample carries.** That is how a static decoder knows it is right.
- **Keep the codec primitives apart from the language front-ends.** A primitive learned for Bash lifted the Day 4 and Day 5 singles.
- **When a label is rejected, look where the value is used, not where it is built.** When the key moves, date the rule by the variant's generation, not the day.
