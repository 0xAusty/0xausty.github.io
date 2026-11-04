+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Mangled"
date = 2026-10-02  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day02-mangled"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 2 (2026-10-02), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-02-cpp-and-pe-orientation
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = true                    # true → appears in the hub's "Start here"

description = "One C++ class in two containers: the ELF set took bare Itanium symbol names, but the mastery's MinGW PE set wanted COFF section-qualified ones."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["homebase", "agent"]

tools  = ["bresolve.py", "aeszip.py", "python"]
tags   = ["reverse-engineering", "pe", "elf", "crc32", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = true
+++

Day 2 of the binary lane asked for 17 facts about two binaries: a C ELF in the style of Day 1, and a C++ build with vtables, RTTI and the config record the lane kept hiding from then on. Most of it was parsing. The part worth writing up is two mastery fields, where one set's C++ binary was a MinGW-built Windows PE. The grader rejected the mangled names that binary plainly contained, and the fields sat open until 7 October. The answer turned on the container, not the class.

## The challenge

Five fields are about the C binary: its SHA-256, its marker string, whether a `.symtab` survives, the integer `recover_code` returns, and the machine. Eight come from the C++ binary's bytes: its SHA-256, its container, the XOR key and CRC32 of its config record, and four config values. The last four are about the classes: vtable and typeinfo presence, the mangled `score()` method and the vtable symbol. The time trial asked the same on a fresh variant, the mastery once per set across two sets.

Only `cpp_format` declared its vocabulary: ELF or PE "from the final bytes", in any letter case, or ELF32, ELF64, PE32 or PE32+. The symbol questions say only "exact", which is where the trouble was. On the single, the handoff records the spellings `c_machine` and `cpp_format` took, and that "several plausible alternatives were rejected".

## Reading the prompt

The prompt, quoted in the card above, reads like a checklist:

| Phrase | Implication | What the solver did |
|---|---|---|
| "C++ on Windows" | The C++ build can be a PE, so the container must come from the bytes. | Reads the magic, `\x7fELF` or `MZ`. The single's C++ binary was not a Windows build; the mastery's PE set was. |
| "The symbols are mangled" | Itanium C++ ABI names (`_Z…`), wanted mangled. | Takes the one `_Z` name containing `5score`, or no answer. |
| "the classes hide behind vtables, and RTTI is your Rosetta Stone" | `_ZTV` (vtable) and `_ZTI` (typeinfo) symbols name the classes. | Presence flags from those prefixes; the vtable name from the class in the score symbol. |
| "Demangle it all with `c++filt`" | Good for reading; the answers stay mangled. | Never demangles. |
| "don't forget the PE imports" | No field asked about imports. | Nothing. |

## What was in the files

Each `evidence.zip` is WinZip-AES with the lane's usual password. In the mastery each set held `day01-c.elf` and either `day02-cpp.elf` or `day02-cpp.exe`.

The C binary is the [Day 1](/huntress-ctf-2026/day01-elf-aware/) kind: a plain ELF with a custom `.huntress` section and a `recover_code` function that returns a constant. The C++ binary carries HCFG, the record later days hid in a different place per language (see [Pool Party](/huntress-ctf-2026/day06-pool-party/)):

```text
offset  size  field
0       4     magic "HCFG"
4       1     version
5       1     XOR key
6       2     payload length (little-endian)
8       4     CRC32 of the decrypted payload
12      n     JSON, every byte XOR'd with the key
```

The check of the PE found two classes. The base has only a typeinfo and a type-name string; the derived class's RTTI names it as its single parent. The derived class owns `score()` and the vtable, whose slots follow the standard Itanium layout:

```text
_ZTV<n><Class>
  [0] offset-to-top (0)
  [1] _ZTI<n><Class>              typeinfo
  [2] <Class>::~<Class>()         complete-object destructor (D1)
  [3] <Class>::~<Class>()         deleting destructor (D0)
  [4] <Class>::score(...) const   the method the question names
  [5] <Class>::family() const
```

The mastery's PE was a byte-patched copy of one MinGW build, and the patch touched the config, not the classes.

## The solve

**The single, 2 October.** The pipeline had no binary solver yet. The single was worked in an AI chat session on the Homebase VM. That session's handoff records all five Day 2 singles CORRECT by about 13:35 ET, but not which analysis produced which binary answer.

**The time trial, 4 October.** After the first attempt expired, Claude Code wrote `bresolve.py` in a session on 4 October, and the time trial went CORRECT there; the time wasn't recorded. The handoff committed at 11:19 ET on 5 October lists the mastery as an open blocker.

**The mastery, 5 to 7 October.** `bresolve.solve_day2` ran once per set and banked 32 of the 34 fields. The two left were the PE set's `mangled_score_symbol` and `vtable_symbol`, where the bare Itanium names and `none` were all rejected.

After a byte-level check (see Dead ends), the escalation note concluded that this "needs the organizer's intended PE answer (grader quirk, or a non-artifact convention), not more RE." It said to ask the event's Homebase AI (GPT-6 Luna), naming the PE set, and not to cycle spellings, which the run's rules counted as brute-forcing the flag.

I put the question to the Homebase AI, and that is where the answer came from. On the PE, the grader wanted COFF section-qualified names:

```text
ELF set   _ZNK<n><Class>5scoreE<params>          _ZTV<n><Class>
PE set    .text$_ZNK<n><Class>5scoreE<params>    .rdata$_ZTV<n><Class>
```

The note calls them MinGW COMDAT section-qualified names: the name of the COMDAT section that holds each definition, `.text$` or `.rdata$` followed by the mangled symbol. They were accepted in practice mode on 7 October. The agent added the rule to `bresolve.cpp_fields`, and its commit at 11:43 ET reports the mastery complete and the binary lane finished for Days 1 to 7.

{{< callout type="warning" title="Same symbol, different string" >}}
Same class, same vtable slots, same `score()` method, and a different expected string on each container. Read the container before you spell the symbol.
{{< /callout >}}

## Making it deterministic

`bresolve.py` was 86 lines when committed, and it refuses rather than guesses:

- **Identify by content.** The C binary is the ELF with no HCFG record; the C++ binary is the file that has one. File names and set numbers play no part.
- **Validate the config.** The payload counts only if its CRC32 matches the header.
- **Cross-check the constant.** `recover_code` is read from the `mov eax, imm32` at the symbol and must agree with a scan of `.text` for that instruction followed by `ret`.
- **One match or none.** Exactly one `_Z` name containing `5score`, and a `_ZTV` name with the same length-prefixed class. The machine comes from `e_machine` through a one-entry table, so an unfamiliar architecture gets no answer.
- **Container last.** When the magic is `MZ`, the two symbols get their `.text$` and `.rdata$` prefixes.

The binary came back on [Day 17](/huntress-ctf-2026/day17-decoder-ring/) and [Day 28](/huntress-ctf-2026/day28-family-resemblance/). On Day 28 the PE variants' vtable fix read the COFF symbol table in raw order, where the first match is the section-qualified name. So, in that bundle at least, the spelling was in the file. Neither Day 2 tool was built to see it: `bresolve.py` matches `_Z…` runs in a PE's raw bytes, which drops any prefix, and the byte-level check read the COFF symbol table for a different class, not a different spelling.

## Timed modes

On 2 October the first harness's sweep started the Day 2 time trials one after another. Their deadlines were about 5 to 8 seconds after start, and all five expired before any analysis was ready. The handoff's lesson: avoid starting a timer while analysis is still underway.

The mastery was timed too, and all-or-nothing. Partial submits persisted within a live attempt, so the 32 solved fields stayed banked while the last two were open.

## Dead ends

- **The bare names on the PE.** Accepted on the ELF set and in the time trial, rejected on the PE set. So was `none`.
- **A renamed class or a repointed vtable.** The byte-level check found two RTTI type strings, every mangled token belonged to those two classes, and the vtable's slots resolved to the derived class's own entries: "there is no alternate artifact-derived value to submit". True of what it searched for.
- **Cycling spellings, ruled out.** The note's two ideas, the base class or a Windows- or COFF-specific decoration, were for the Homebase AI to weigh, not for the grader.
- **Analysts against the clock.** On 2 October the chat session's binary analysis produced nothing usable in time; the local record said "no confident solver".
- **"Set 1 is always a PE."** The 5 October handoff said so; by 7 October the PE had turned up in set 1 and in set 2. The solver never relied on it.

## Takeaways

1. **The container is part of the answer.** The same symbol was spelled differently on the PE set.
2. **Prove the negative, then escalate a narrow question.** Ruling out a different class left one question about the organisers' convention, for the Homebase AI rather than the grader.
3. **Search for the right kind of difference.** The check looked for a different class; the answer was a different spelling, which a raw-order read of the COFF symbol table found on Day 28.
4. **Don't open a timer you can't finish.** The 2 October time trial expired within seconds of starting.
