+++
title = "Warmups"
date = 2026-11-02
draft = true
layout = "lane"
lane = "warmups"
weight = 10

description = "One blob a day and a new encoding layer on top of the last, from Base64 to Brainfuck: a solver that validates every decode against known plaintext instead of trusting what looks decoded."

tags   = ["ctf", "encodings", "classical-ciphers", "automation"]
skills = ["Automation & Tooling"]
toc    = true
+++

The warmup lane handed out one blob a day, and the layers compounded over the month. Each day stacked another classic encoding on top of the ones before it, so by the end a single answer could be sitting under Base64, ROT13, hex, binary, decimal, octal, URL percent-encoding, HTML entities, backslash escapes, Base32, Base64url, string reversal, Atbash, a Caesar shift with an unknown offset, ROT47, Morse, Baconian groups, rail-fence transposition, UTF-16 in either byte order under hex, netstrings, Ascii85, Unicode code points, Brainfuck and its Ook! dialect, and gzip or zlib under Base64.

The masteries scaled that up. Each one was 30 to 70 numbered lines, every line with its own chain of layers, and every line decoding to the same kind of answer: a slug of three dictionary words and two digits. At that volume, a decoder that stops as soon as its output looks decoded is not good enough.

So the solver I built, `wusolve.py`, does not trust appearances. Every decode is checked against the instruction sentence the blob is known to contain and against a dictionary for the words in the slug, and when a layer needs a key, `kpa.py` recovers it from that known plaintext. A decode that fails the check is not an answer, however readable it looks.
