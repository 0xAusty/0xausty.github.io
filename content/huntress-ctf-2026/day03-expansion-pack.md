+++
title = "Expansion Pack"
date = 2026-10-03
draft = false
params.kind = "challenge"  # Hugo reserves a top-level "kind" (removed in v0.144); this still reads as .Params.kind
catalog_key = "day03-expansion-pack"
depth = "full"
featured = false
description = "Batch variable expansion, read statically: the grader scored the form where the config is consumed, not where it is built, and two look-alike FOR loops took different labels."
solved_by = ["homebase", "agent"]
tools = ["bat.py", "scriptsolve.py", "timed.py", "python"]
tags = ["malware-analysis", "batch", "deobfuscation", "xor"]
skills = ["Malware Analysis"]
toc = true
+++

Expansion Pack was the script lane's first Batch day, and the puzzle the lane kept coming back to. Decoding nine Batch files without running them was routine. Naming how each one expanded its variables was not: the obvious reading was wrong, the right one came from the event's Homebase AI (GPT-6 Luna), and two files built on the same FOR loop took different labels. That last gap is the part worth showing, because there the solver was made to answer nothing instead of guessing.

## The challenge

Script Analysis was cumulative. The Day 3 bundle re-asked Day 1's three PowerShell samples and Day 2's nine JScript files, then added nine Batch files with eight questions each: the file's role, its ATT&CK technique, indicators from its decoded config, and two labels only the challenge generator could define. One was the variable-expansion form, four short names that match the prompt's four phrases: `percent`, `delayed`, `call_double` and `for_indirect`. The other was the control-flow form of the wrapper around the file's recover routine.

## Reading the prompt

The prompt reads like a description of cmd.exe, but it turned out to describe the generator.

| Phrase | Implication | What the solver did |
|---|---|---|
| "expands percents, delays expansion, CALLs twice, and bends FOR loops into indirection" | Four mechanisms, one label each; the wording mirrors the generator's categories. | The first `bat_expansion` sorted rebuild lines into the four; quoted verbatim to the Homebase AI, the sentence later unlocked the short labels. |
| "Reconstruct every variable … without executing a single line" | Static recovery only. | `bat.py` doesn't replay the expansion; it decodes the material directly and keeps only a decode that starts with the descriptor prefix `v=1\|`. |
| "follow the staged chain to its final handoff" | Roles are classified by the decoded graph's last step. | Took the role from a table keyed by file family; a Homebase note on 8 October said to read the decoded steps instead. |

## What was in the files

`evidence.zip` is WinZip-AES encrypted with the usual password. Each Batch file inside has the same anatomy:

- a `HUNTRESS-MATERIAL` line carrying the encoded config, with a `HUNTRESS-CODEC` hint;
- a rebuild line that reassembles the config from fragment variables, and an `echo(` line that consumes it;
- a wrapper around the recover routine: `goto :HUNTRESS_DISPATCH`, `call :HUNTRESS_RECOVER`, an `if defined` or `if errorlevel` guard, or none;
- noise: a separator line (`||`, `&&`, `&` or `| findstr`) that a `goto :HUNTRESS_SEPARATOR_DONE` jumps over, and `neutral_*` variables.

Decoded, the material is a pipe-delimited `key=value` descriptor beginning `v=1|`, and most indicator questions read straight out of it. The two labels don't: they describe the code around the config.

## The solve

The first Batch solver, written by Claude Code, the coding agent that built most of the pipeline, labelled the obvious line: the rebuild. It was wrong. The Homebase AI found the rule the grader used: the expansion form is the one where the config is **consumed**, the `echo(!var!)`, not where it is built. The seven files without a FOR-loop rebuild all took `delayed`. Of the two with one, the benign `host-context.cmd` was accepted as `for_indirect`; the launcher, `local-dispatch.bat`, stayed open.

By 11:19 on 5 October the single stood at 149 of 159, and the notes list only generator labels as blocking it: the nine control-flow forms and the launcher's expansion. Several answers had already been rejected. The pipeline's rule was never to guess, and the notes called cycling wordings brute force under the competition rules, so the way forward had to be information about the intended format. Expansion Pack "was stuck for hours".

What the notes credit to me is the framing: quoting the Game Master's prompt to the Homebase AI word for word. The prompt mirrors the generator's categories, and the answers turned out to be short generic labels, not descriptions. The Homebase AI got `if_guard` accepted for the files with an `if defined` guard and gave `call_double` for the launcher. The single was CORRECT at 13:19:34 on 5 October, and the notes record it as solved by the Homebase AI. That afternoon the agent wrote the construct-to-label table into the solver.

## Making it deterministic

**Decoding.** `bat.py` never needs the codec hint. It reads the material as base64, reversed base64, hex or decimal, forwards or reversed, and at first tried all 256 XOR keys, 255 subtraction keys and seven right-rotations, keeping the candidate that starts `v=1|`: up to 4,144 transforms per file. On 15 October profiling showed that search taking 6.8s of the Day 15 script mastery's 7.8s solve, so the agent switched to recovering the key from the known prefix: 45 times faster, identical on all 657 corpus samples. The inner step, condensed:

```python
PREFIX = b"v=1|"  # every decoded Batch descriptor starts with this
ROR = [None] + [bytes(((i >> n) | (i << (8 - n))) & 255 for i in range(256)) for n in range(1, 8)]

def unwrap(raw: bytes):
    """raw: the material after base64, reversed base64, hex or decimal, forwards or reversed."""
    if len(raw) < len(PREFIX):
        return None
    k = raw[0] ^ PREFIX[0]                       # XOR: the first byte gives the key
    if all(raw[i] ^ k == PREFIX[i] for i in range(4)):
        return raw.translate(bytes(i ^ k for i in range(256)))
    k = (raw[0] - PREFIX[0]) & 255               # subtraction: the same trick
    if k and all((raw[i] - k) & 255 == PREFIX[i] for i in range(4)):
        return raw.translate(bytes((i - k) & 255 for i in range(256)))
    for n in range(1, 8):                        # rotate right: seven tables to try
        if raw[:4].translate(ROR[n]) == PREFIX:
            return raw.translate(ROR[n])
    return None
```

**Control flow.** `scriptsolve.bat_control` reads only the body between the `:HUNTRESS_SEPARATOR_DONE` label and the `echo(` line, so the separator noise never reaches it, and names the wrapper:

| Wrapper around the recover routine | Label |
|---|---|
| `if errorlevel` | `errorlevel_guard` |
| `if defined` | `if_guard` |
| `goto :HUNTRESS_DISPATCH` | `goto_dispatch` |
| `call :HUNTRESS_*` | `call_subroutine` |
| none | `direct` |

**Expansion.** `bat_expansion` returns `delayed` for plain `%var%` and `!var!` rebuilds. A FOR-loop rebuild, and later a bare `call set`, gets `None` plus two candidates for the timed runner's two-try.

**Eras.** On 15 October the answer key itself changed: variants generated from 09:00 ET (13:00 UTC), the [Day 15](/huntress-ctf-2026/day15-crumb-trail/) time trial among them, score the rebuild line's own form; older ones, every Day 3 attempt included, the echo line. `timed.recon_rule` carries the cut-over.

## Timed modes

The time trial, the same questions on a fresh bundle, came back CORRECT at 15:54:37 on 7 October, run by the agent in its timed-modes session. The mastery took longer. Timed submits were all-or-nothing, the Batch expansion fields now blocked every script mastery, and I put every script mastery and retry on hold until the Homebase AI came back with a mapping.

The same day the two Day 3 FOR-loop rebuilds were compared side by side:

```batch
for %%G in (0 1 2 3) do call set "recovered_configuration=%%recovered_configuration%%%%fragment%%G%%"
for %%G in (0 1 2 3) do call set "cfg=%%cfg%%%%h%%G%%"
```

The first is `host-context.cmd` (`for_indirect`), the second the launcher (`call_double`): same loop, same `call set` double expansion, same `echo(!x!)` consumer, different variable names, codec and one guarded initialisation line. Nor was it the role; the launcher took `for_indirect` on Day 6. The escalation note concluded that "the label is not a function of the visible artifact", the Homebase AI agreed the four forms alone didn't decide it, and at 17:14 the agent made `bat_expansion` return `None` there, so no timed attempt could hinge on a guess.

I approved a capped two-try, committed at 01:33 on 8 October: submit `for_indirect`, then `call_double` only on the expansion fields the Game Master still reports open; never a third label, never another field.

By 09:02 on 8 October the Homebase AI's own engine had solved the Day 4 to 7 script masteries from fresh bytes the evening before, and its note named the Day 3 difference: the indexed variable's name, `fragment…` for `for_indirect`, `h…` for `call_double`. That rule never went into `bat_expansion`; the two-try stayed, and cleared 12 such fields on the Day 10 mastery.

The Day 3 mastery was still listed open at 09:15 on 10 October. A 13:14 commit that day records the script backlog CORRECT, already solved when checked. The submit was at 20:43:56 on 7 October; who made it is not recorded.

## Dead ends

- **The build line.** The first `bat_expansion` labelled where the config is built; the grader scored where it is used.
- **The launcher's expansion.** `percent`, `delayed` and `for_indirect` were rejected before `call_double`.
- **The stager's control flow.** `||`, `double_pipe`, `string_join` and prose were rejected. Separator lines are noise; the label belongs to the wrapper.
- **Reading harder.** Hours on the bytes without the prompt's framing went nowhere.

## Takeaways

1. **Label where the value is used, not where it is built.** The scored expansion form sat on the `echo(!var!)` line, not the rebuild line.
2. **Quote the source before theorising.** The Game Master's sentence mirrored the generator's categories; leading with it got short labels back.
3. **When the solver can't decide, make it say so.** `None` kept guesses out of timed submits, and the one guess left went through a two-try that was capped and that I approved.
4. **Timestamp your evidence.** The key moved with the generator, not the day, and only each replay case's recorded time told the eras apart.
