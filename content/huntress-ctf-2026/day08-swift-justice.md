+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Swift Justice"
date = 2026-10-08  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day08-swift-justice"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 8 (2026-10-08), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-08-swift-network-configuration
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The config in a 67 MB Swift ELF was base64 in a string literal beside a decoy; a CRC-checked search found it, and a parallel runner beat the timed mastery."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "binmastery.py", "python"]
tags   = ["reverse-engineering", "swift", "elf", "base64", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = true
+++

Day 8 put a 67 MB statically linked Swift binary into the binary lane's cumulative bundle and asked, among other things, where it phones home. The earlier days kept the lane's config record, HCFG, as raw bytes or as base64 in a jar's constant pool. This one keeps it as base64 in a Swift string literal, with a decoy beside it for anyone grepping strings. It's worth writing up for a small calling-convention exercise, a lesson in letting the declared format pick the encoding, and the one mastery still on a clock that day.

## The challenge

The bundle carried Days 1 to 7 again plus the Swift ELF, and the single asked 80 fields across all eight, a fuller set than any earlier single: older members picked up new questions, from the Day 1 ELF's entry point to the compression methods of the two jars.

For the Swift member the questions wanted its SHA-256, format, `elf_class`, `machine` and `architecture`, the config's campaign, domain, mutex and URL, and the record's CRC32. Two declared formats mattered. `elf_class` and `machine` were integers for Day 8, while the same questions about the Day 1 ELF stayed text. And `compression_methods` wanted the distinct method codes, in first-appearance order, as a JSON array of integers.

The time trial asked the same fields over a fresh bundle. The mastery repeated them over five sets and was still timed, although that day the Game Master had started returning `deadline: null` for the other four lanes' time trials and masteries.

None of it ran on the schedule. The laptop was suspended at 08:50, plain cron has no catch-up, and Day 8 was worked in a session with Claude Code instead; the analysis and the code below are the agent's. The next morning's cron, pointed at Day 8 by a stale marker, found all three binary modes already CORRECT ([Day 9](/huntress-ctf-2026/day09-nimble/) has the fix).

## Reading the prompt

Three phrases in the prompt carry the solve.

| Phrase | Implication | What the solver did |
|---|---|---|
| "hide their networking in plain sight" | The config is readable text, not raw HCFG bytes, and a strings pass also finds things that look like config and aren't. | `binsolve.py` decodes long base64 runs and keeps only one that is an HCFG record with a valid CRC32. |
| "Follow the symbols" | The functions are named: `encodedConfig()` returns the literal, `decodeConfig()` checks it. | In session the agent disassembled `encodedConfig` and read the string it returns. The solver never looks at a symbol. |
| "see where this one phones home" | The URL and domain to report are the ones inside the decoded record. | `_cfg` copies campaign, domain, mutex and URL from the record's JSON, and the CRC32 from its header. |

## What was in the files

`evidence.zip` is the lane's usual WinZip-AES archive, opened in code with the usual password. Inside are the Day 1 to 7 members and the Swift ELF: statically linked, built for Linux, 67 MB on its own.

The config runs through two functions. `encodedConfig()` is 31 bytes of machine code returning a Swift `String`, which comes back in two registers: the count, `0x1fc` (508), and a pointer into read-only data. Those 508 characters are base64. `decodeConfig()` decodes them and checks the magic with `mov edi, 0x47464348`, which is `HCFG` as a little-endian 32-bit integer. Decoded, it is the same record as on the earlier days: a 12-byte header (magic, version, XOR key, payload length, CRC32 of the plaintext), then JSON XOR'd with the key byte.

{{< callout type="warning" title="The decoy is built for strings" >}}
Right next to the real literal sits a "dynamic trace" scaffold: a `HUNTRESS_HOST_MODEL` marker and a placeholder URL that is never requested. It is bait for a strings-grep, and its URL is not the answer.
{{< /callout >}}

## The solve

The Day 1 to 7 members went through the branches `binsolve.py` already had, extended with the new fields. The Swift member needed two new pieces.

The first is the header fields. The d08 branch reads the ELF class byte at offset 4 and writes the bit width it stands for, not the byte; reads the `e_machine` half-word at offset 18 and writes it in decimal; and writes `architecture` as text, in the spelling the lane had settled on. So one header gave three encodings, each picked by the declared format rather than the field's name.

The second is the config. Following the symbols showed what to look for, but the solver doesn't disassemble anything. `_hcfg_b64`, as committed for Day 8, decodes every base64 run of 300 characters or more and keeps the first that starts with `HCFG` and survives `hcfg_from`:

```python
def _hcfg_b64(b):
    """Swift carrier (d08): the HCFG blob is base64 text held in a Swift string
    literal (`encodedConfig`); `decodeConfig` base64-decodes it then checks 'HCFG'."""
    for m in re.finditer(rb'[A-Za-z0-9+/]{300,}={0,2}', b):
        try:
            dec = base64.b64decode(m.group(0))
        except Exception:
            continue
        if dec[:4] == b'HCFG':
            h = hcfg_from(dec)
            if h:
                return h
    return None
```

`hcfg_from` XORs the payload with the header's key byte and checks it against the header's CRC32 before parsing the JSON, so nothing but a valid record can supply an answer. With that, the single and the time trial each answered every field.

## Making it deterministic

Everything went into `binsolve.py`, and it had to keep working: the later cumulative bundles shipped Day 8 again.

- **Older days, new fields.** The entry point comes from `e_entry`, the `.symtab` flag from the section headers, and the C++ flags from whether any `_ZTI` or `_ZTV` symbol exists. The .NET record already carried a URL and a CRC32; Day 8 was the first day the questions asked for them. The Go and Rust version and key come from their HCFG headers, and each jar's compression methods from its entries in order, deduplicated into a compact JSON array.
- **The offset.** Day 9's Nim binary hid its record the same way and asked for the run's file offset, so the search became `_hcfg_b64_off`, which returns it too. When [Day 17](/huntress-ctf-2026/day17-decoder-ring/) re-asked Day 8 for that offset and a storage label, the offset came from the same function; the label took a one-field-at-a-time probe of the grader.
- **Faster.** A profile on 16 October put the regex pass over the 67 MB member at 0.35s. Base64 turns `HCF` into `SENG`, so the scan now decodes only runs that start at a `SENG` hit: the same first match, in milliseconds.
- **Cleaner.** The binary solvers, the mastery runner written that day included, extracted each bundle into a temp folder and never removed it, leaving another copy of the Swift member behind on every run. By [Day 14](/huntress-ctf-2026/day14-selective-memory/) about 6.1 GB of them had filled the laptop's quota'd `/tmp`, and that morning's binary mastery died with `Errno 122`. The solvers now clean up in a `finally`, and since 16 October the binary solve decrypts in memory.

## Timed modes

The time trial was the single again over a fresh bundle, and the same `binsolve.py` path answered it.

The mastery was the problem: five bundles, each with its own 67 MB Swift member, to download, decrypt, hash and solve inside a window of about 27 seconds. The notes say a serial runner would miss it, so the agent wrote `binmastery.py`. It fetches the five bundles at once in threads, because downloads are I/O-bound, and solves them in separate processes, because the AES decryption and the hashing are CPU-bound and were the real cost. Answer ids arrive as `setN.<field>`; the runner groups them by set, maps each process's answers back and submits all 400 in one call, at first only when every id had an answer. The notes put a run at about 21 seconds.

The runner stayed. It was still running the binary masteries on Day 31, when the notes list one bug in it that was never fixed: it didn't retry a dropped submit.

## Takeaways

1. **Follow the symbols once, then automate the invariant.** The disassembly showed where the record lived; the solver searches for what it is, a base64 run that decodes to a CRC-valid HCFG, and the same search answered the Nim binary the next day.
2. **The declared format picks the encoding.** One header gave a bit width, a raw constant and a name, because that is what the declared formats asked for.
3. **Validate instead of grepping.** The decoy was built for a strings search; a solver that only accepts a CRC-valid record never considers it.
4. **Split work by its bottleneck.** Threads for downloads, processes for decryption and hashing, one submit at the end.
