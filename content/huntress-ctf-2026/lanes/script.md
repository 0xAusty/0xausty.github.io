+++
title = "Script Analysis"
date = 2026-11-02
draft = true
layout = "lane"
lane = "script"
weight = 30

description = "Deobfuscating thirty script languages without running any of them: static recovery of each sample's embedded plan, validated against its own markers and mapped to MITRE ATT&CK."

tags   = ["malware-analysis", "deobfuscation", "powershell", "batch", "vbscript", "mitre-attack"]
skills = ["Malware Analysis"]
toc    = true
+++

Script Analysis was cumulative. Each day's challenge re-asked every earlier day on top of the new material, so the field counts climbed from 399 on Day 6 to 469 on Day 7, past 1,000 later in the month, and to 10,465 on the Day 23 mastery. The samples ran through PowerShell, JScript, Batch, VBScript, Python, Bash, Node.js, PHP, HTA and WSF, Lua, WMI MOF, AutoIt, AppleScript, MSBuild, Perl, Groovy and Jenkins, GitHub Actions, NSIS, JSP, Elixir and Phoenix, Erlang, Dockerfiles, Terraform, Makefiles, BeanShell and XSLT.

None of it was executed. Every sample was decoded statically: inert decoder functions in a Node vm sandbox, a tiny Python AST evaluator, re-implemented Bash recovery routines. Each decode was validated against the descriptor markers the samples carried themselves, and each sample was mapped to MITRE ATT&CK.

Two things kept coming back. The puzzle was the Batch variable-expansion "form", whose answer key changed with the challenge generator. The trick was using the grader's per-field accept/reject as an oracle: submit a batch, and when it is rejected, bisect it.

<!-- Outline. Source: WRITEUP_NOTES.md script beats (Days 4-19), scriptsolve.py, pysolve.py, bashsolve.py,
     nodesolve.py, polysolve.py, bat.py, vbsolve.py, jsan.js.
     Link back to the flagship: /projects/huntress-ctf-2026-ai-arena/ -->

<!-- Intro: the script lane, cumulative "mega-challenges" (399, then 469, then 1,000+ fields), and the one rule: never execute the sample. (outline note: the intro paragraphs above now cover this) -->

## The shape of every sample

<!-- A material blob, a codec hint, and a recover routine. The decoded plan (v=1, v=2, v=3 descriptors,
     HUNTRESS_ANALYSIS_V1 markers) states syntax, obfuscation, carrier and technique outright.
     Validating against the marker is how you know a decode is right. -->

## Running only the harmless parts

<!-- JScript: execute only the inert decode functions in a Node vm sandbox. Python: a tiny AST
     evaluator so nothing "hatches". Bash: read the Recover_ function like a native and reproduce it
     (d[N-1-i]=e[i]^58 is "reverse then XOR"). -->

## Batch: four ways to expand a variable

<!-- percent / delayed / call_double / for_indirect. The obvious answer (the form where the config is
     built) was wrong; the grader wanted the form where the value is consumed (echo(!var!) -> delayed).
     Control-flow labels: call_subroutine, the FOR /L wrapper is a red herring. The answer key that
     changed with the generator (echo line vs rebuild line), and how the replay corpus caught it. -->

## One codec library, every language

<!-- decimal_comma, reverse_then_xor, base64_literal, integer_tuple, multi-byte XOR, hex_buffer,
     escaped_octets... Teaching the shared decoder a primitive once unlocked answers in other languages
     and on still-open earlier days (Day 4 215 -> 222, Day 5 343 -> 346). -->

## New carriers kept arriving

<!-- Node ESM with JS-escaped literals. PHP webshells, HTA and WSF hosts. Google Apps Script with the
     descriptor split behind a SPLIT marker. Roslyn C# inside an ASPX <script runat="server"> literal,
     where a literal \n bled into the payload. -->
<!-- TODO: Days 20-31 carriers. -->

## Mapping to ATT&CK

<!-- Every inferred mapping held. Favorite tell: a Node adapter calling itself systemd_descriptor whose
     indicator path is /etc/cron.d/..., so the technique is cron (T1053.003), not systemd.
     stage_count is a declared field, not the step count (2 steps, stage_count=1). -->

## Takeaways

<!-- Validate decodes against a known marker. Separate the decoder primitives from the language
     front-ends. When a "label" is rejected, look for where the value is used, not where it's built. -->
