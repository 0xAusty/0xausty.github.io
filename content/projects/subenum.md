+++
title = "subenum — Fast Subdomain Enumerator"
date = 2026-05-12T09:00:00Z
draft = false

description = "SAMPLE ENTRY (not a real project) — shows the layout for a tool writeup. Replace with something you actually built."

tech     = ["Python", "asyncio", "Docker"]
# repo/demo intentionally empty: this is a fictional example, so no dead links
# are rendered. Add your real URLs here and the buttons appear automatically.
repo     = ""
demo     = ""
tags     = ["tooling", "reconnaissance", "automation"]

featured = true
weight   = 10
toc      = false
+++

{{< callout type="warning" title="This is a sample entry, not real work" >}}
`subenum` is a **fictional** tool included to demonstrate the project page format.
It is not something I built and there is no repository behind it. Replace this file
with a real project — see the README for how.
{{< /callout >}}

## Overview

**subenum** is a command-line reconnaissance tool that discovers subdomains for a target
domain. It combines passive sources (certificate transparency, public DNS datasets) with
active brute-force resolution, then filters out wildcard noise so the output is
assessment-ready. Built to be fast, scriptable, and easy to drop into a recon pipeline.

## Features

- **Async resolver** — thousands of DNS lookups per second with `asyncio`.
- **Passive + active** — merges CT logs and public datasets with wordlist brute-forcing.
- **Wildcard detection** — automatically strips false positives from wildcard DNS.
- **Clean output** — plain list, JSON, or pipe straight into `httpx` / `nuclei`.
- **Dockerized** — one command to run, no dependency hell.

## How it works

Passive sources give breadth; active resolution gives depth. subenum queries CT logs and
DNS aggregators for known names, then brute-forces a wordlist against the target. Every
candidate is resolved concurrently through a bounded worker pool. Before reporting, it
sends known-random probes to detect wildcard responses and discards anything matching that
signature — the part most naive scripts get wrong.

## Usage

```bash
# with Docker
docker run --rm <your-user>/subenum -d example.com -o results.json

# or locally
git clone https://github.com/<your-user>/subenum
cd subenum && pip install -r requirements.txt
python subenum.py -d example.com --json | httpx -silent
```

Illustrative output (also fictional):

```text
[*] example.com — 3 passive sources, 12,003 wordlist entries
[+] api.example.com
[+] dev.example.com
[+] vpn.example.com
[*] 47 live subdomains in 9.3s
```
