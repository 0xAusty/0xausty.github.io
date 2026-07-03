+++
# --- Auto-filled when you run:  hugo new projects/my-tool.md ---
title = "{{ replace .File.ContentBaseName "-" " " | title }}"
date = {{ .Date }}
draft = true

description = "One-sentence pitch of what this tool/research does and why it matters."

tech     = ["Python", "Docker"]    # shown as chips on the card + project page
repo     = "https://github.com/0xausty/your-repo"   # optional — omit to hide the button
demo     = ""                                        # optional live demo URL
tags     = ["tooling", "automation"]

featured = false                   # set true to surface this on the homepage
weight   = 0                       # lower = earlier in the grid (0 = by date)
toc      = false
+++

## Overview

What problem does it solve? Who is it for?

## Features

- Bullet the highlights.

## How it works

A short technical explanation — this is where you show depth.

## Usage

```bash
git clone https://github.com/0xausty/your-repo
cd your-repo
python main.py --help
```
