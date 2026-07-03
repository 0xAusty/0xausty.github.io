+++
title = "subenum — Fast Subdomain Enumerator"
date = 2026-05-12T09:00:00Z
draft = false

description = "A fast, async subdomain enumeration tool that merges passive sources with active resolution and wildcard filtering."

tech     = ["Python", "asyncio", "Docker"]
repo     = "https://github.com/0xausty/subenum"
demo     = ""
tags     = ["tooling", "reconnaissance", "automation"]

featured = true
weight   = 10
toc      = false
+++

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
docker run --rm 0xausty/subenum -d example.com -o results.json

# or locally
git clone https://github.com/0xausty/subenum
cd subenum && pip install -r requirements.txt
python subenum.py -d example.com --json | httpx -silent
```

```text
[*] example.com — 3 passive sources, 12,003 wordlist entries
[+] api.example.com
[+] dev.example.com
[+] vpn.example.com
[*] 47 live subdomains in 9.3s
```

> Replace the repo URL in the front matter with your real project. This entry is a
> template so you can see the exact format — copy it for your next tool.
