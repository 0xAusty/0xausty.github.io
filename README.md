# 0xAusty — Cybersecurity Portfolio

A fast, low-maintenance portfolio blog for security **projects** and **Hack The Box /
CTF writeups**, built with [Hugo](https://gohugo.io) and deployed automatically to
GitHub Pages.

**The whole workflow is: write one markdown file → `git push` → it's live.**

- 🌑 Dark-by-default with a light toggle · 🔎 full-text search · 🏷️ filterable tags
- 📋 one-click copy on every code block · 🖥️ terminal styling · 🖼️ click-to-zoom images
- 📁 collapsible spoilers · 💡 callout boxes · 🧭 auto table of contents
- 📡 RSS · 🗺️ sitemap · 🔗 Open Graph/Twitter cards · ♿ accessible & responsive

---

## 1. Prerequisites

You need the **extended** edition of Hugo (it compiles the SCSS). This project is pinned
to **Hugo v0.163.3** — match it locally to match what deploys.

| OS | Command |
|----|---------|
| Windows | `winget install Hugo.Hugo.Extended` |
| macOS | `brew install hugo` |
| Linux | `sudo snap install hugo` or grab the `.deb` from [releases](https://github.com/gohugoio/hugo/releases) |

Check it worked (note the `+extended`):

```bash
hugo version
# hugo v0.163.3 ... +extended ...
```

Git is the only other requirement.

---

## 2. Run it locally

```bash
hugo server
```

Open <http://localhost:1313>. The site live-reloads as you edit — leave it running while
you write. To preview posts still marked `draft = true`, use `hugo server -D`.

---

## 3. Project structure

```
.
├── hugo.toml                 # ← ALL your settings live here (name, bio, colours, nav, links)
├── .htmltest.yml             # dead-link checking config (used by CI)
├── archetypes/               # templates used by `hugo new` (writeups, detections, projects)
├── content/
│   ├── _index.md             # homepage (text comes from hugo.toml)
│   ├── about.md              # About page — edit your bio/skills/certs here
│   ├── portfolio.md          # /portfolio/ — grouped by skill area (the resume URL)
│   ├── writeups/             # one .md file per writeup
│   ├── detections/           # one .md file per detection rule
│   ├── projects/             # one .md file per project
│   └── blog/                 # short notes (optional)
├── layouts/                  # the theme (HTML templates + shortcodes) — rarely touched
├── assets/
│   ├── css/main.scss         # design tokens (colours, spacing, fonts) in one place
│   └── js/                   # copy buttons, theme toggle, lightbox, search
├── static/
│   ├── images/               # your screenshots and images go here
│   └── (add resume.pdf here, then set params.resume in hugo.toml)
└── .github/workflows/
    ├── deploy.yml            # auto-build + deploy on every push to main
    └── ci.yml                # build + dead-link check + secret scan
```

---

## 4. Add a new writeup

```bash
hugo new writeups/forest.md
```

This creates `content/writeups/forest.md` pre-filled from the archetype. Open it, write
your walkthrough, and set `draft = false` when ready. Front matter reference:

```toml
+++
title = "HTB: Forest — AS-REP Roasting to DA"
date = 2026-07-01T10:00:00Z
draft = false
description = "One-line summary shown in lists, search, and social cards."

# Taxonomies — keys are PLURAL (this is a Hugo rule; see §8).
platforms    = "Hack The Box"          # single value
oses         = ["Windows"]             # host OS only — AD is a tag, not an OS (§8)
difficulties = "Medium"                # Easy | Medium | Hard | Insane
tools        = ["nmap", "bloodhound", "impacket"]
tags         = ["kerberos", "as-rep-roasting", "active-directory"]

skills = ["Active Directory"]          # groups it on /portfolio/

toc        = true      # show the table-of-contents sidebar
disclaimer = true      # show the "authorized targets only" note
+++

Your walkthrough in **markdown**...
```

### Rich content you can use in any post

| What | How |
|------|-----|
| **Callout** (info/tip/warning/danger) | `{{</* callout type="tip" title="Note" */>}}text{{</* /callout */>}}` |
| **Spoiler** (hidden until clicked) | `{{</* spoiler summary="Reveal flag" */>}}`HTB{...}`{{</* /spoiler */>}}` |
| **Screenshot** with caption + zoom | `{{</* img src="/images/foo.png" alt="..." caption="..." */>}}` |
| **Terminal** window | `{{</* terminal title="kali@htb" */>}}$ nmap ...{{</* /terminal */>}}` |
| **Code block** with copy button | ` ```bash ` fenced block (copy button is automatic) |

The archetype (`archetypes/writeups.md`) already contains one of each, so a fresh
`hugo new` gives you a working example to edit.

---

## 4b. Add a new detection

```bash
hugo new detections/suspicious-lsass-access.md
```

Same shape as a writeup, with detection-engineering taxonomies instead:

```toml
+++
title = "Suspicious LSASS Handle Access"
date = 2026-08-12T10:00:00Z
draft = false
description = "One-line summary of what this rule detects."

mitre-techniques = ["T1003.001"]          # ATT&CK IDs — drives the /mitre-techniques/ index
platforms        = "Windows"              # shared with writeups; see §8
log-sources      = ["Sysmon", "Windows Security"]
tags             = ["detection-engineering", "credential-access"]
skills           = ["Detection Engineering"]   # groups it on /portfolio/
toc = true
+++
```

The Detections list page builds its filter chips from whatever your detections
actually use, so you never have to register a technique or log source anywhere.

---

## 4c. Add a Huntress CTF 2026 page

The `/huntress-ctf-2026/` section is driven by a data file, `data/huntress_ctf_2026.json`:
one catalog entry per challenge (key, day, lane, title, prompt, modes, artifacts, results)
plus the event totals. The hub, the lane pages and the "at a glance" card at the top of
every challenge page are rendered from that catalog, so a content page only adds prose and
never restates a number. A challenge page is tied to its entry by `catalog_key`, which must
match exactly. A `catalog_key` that matches no entry fails the build on purpose:
`hugo --panicOnWarning` stops with the file name and the key.

Generate the stub with `hugo new huntress-ctf-2026/<key>.md` (the archetype reads the
catalog) or, without Hugo, with the helper script; both fill the key, title, release date
and the lane's default tags and skills from the catalog:

```bash
python scripts/ctf_new.py --list                          # catalog keys that have no page yet
python scripts/ctf_new.py day06-pool-party                # field note stub   (depth = "note")
python scripts/ctf_new.py day06-pool-party --depth full   # full write-up stub (depth = "full")
```

The script keeps the static part of `archetypes/huntress-ctf-2026.md` (its `{{ if }}` /
`{{ with }}` blocks are Hugo's job and count as false), fills `title`, `date`, `catalog_key`,
`depth`, `tags` and `skills` itself, adds a comment with the entry's day, lane, Game Master id
and `web_no` (the web lane's own numbering), writes `content/huntress-ctf-2026/<key>.md` as a
draft, and refuses to overwrite an existing page. Standard library only; works from any shell.

```toml
+++
title = "Pool Party"
date = 2026-10-06                 # the challenge's release date (from the catalog)
draft = true
params.kind = "challenge"         # see note below; series pages use layout = "series" instead
catalog_key = "day06-pool-party"  # MUST match a key in data/huntress_ctf_2026.json
depth = "full"                    # "full" (curated write-up) | "note" (short field note)
featured = false                  # true → listed under "Start here" on the hub (newest first, max 5)
description = "One line: the key insight or the skill this shows."
solved_by = ["agent", "hand"]     # autopilot | agent | hand | homebase, most important first
# Each value renders as one line under the glance card:
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   hand      → "Solved by hand (Austin)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
tools = ["python"]
tags = ["reverse-engineering", "java"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/
toc = true
+++
```

For a challenge the catalog marks unsolved, both generators write `solved_by = []` so no
page claims a solve it did not get.

`kind` is written as `params.kind` because Hugo reserves the bare key and has refused it
since v0.144; through the `params` map it still reaches the templates as `.Params.kind`.

Set `draft = false` to publish. The catalog decides *what* the hub shows for every
challenge; a page only changes *how*: a published page turns the title into a link, swaps
the prompt excerpt for your `description`, adds a "Full write-up" or "Field note" badge,
and counts towards the "N write-ups" figure on the hub. Lane intros live in
`content/huntress-ctf-2026/lanes/<lane>.md` (`layout = "lane"`), and prose chapters such as
*How I played* are series pages (`layout = "series"`) in the same folder.

---

## 5. Add a new project

```bash
hugo new projects/my-tool.md
```

```toml
+++
title = "my-tool — What It Does"
date = 2026-07-01T10:00:00Z
draft = false
description = "One-sentence pitch shown on the card."
tech     = ["Python", "Docker"]        # chips shown on the card
repo     = "https://github.com/0xausty/my-tool"   # omit to hide the button
demo     = ""                          # optional live demo URL
featured = true                        # true = show on the homepage
weight   = 10                          # lower sorts earlier
+++

## Overview
...
```

---

## 5b. The /portfolio/ page (your resume URL)

`/portfolio/` lists your work **grouped by skill area instead of by date**, which is
what you want when a hiring manager opens one link.

It is driven by a `skills` taxonomy. Any page in any section opts in:

```toml
skills = ["Active Directory", "Detection Engineering"]
```

A page appears under every skill it lists. Headings are alphabetical; newest first
within each. **A page with no `skills` value does not appear** — this is a curated
view, not a full archive, so you decide what a recruiter sees. Keep the skill names
consistent (they are literal strings) and reuse the vocabulary from your resume.

---

## 6. Add images

1. Drop the file in `static/images/` (e.g. `static/images/forest-bloodhound.png`).
2. Reference it from a post with the `img` shortcode (leading `/`):

```markdown
{{</* img src="/images/forest-bloodhound.png" alt="BloodHound path" caption="Shortest path to DA." */>}}
```

Clicking any image opens it full-screen (lightbox). Images are lazy-loaded automatically.

Replace these starter placeholders with your own when you can:
`static/images/og-default.png` (1200×630 social card) and `static/images/avatar.png`
(then uncomment the photo block at the top of `content/about.md`).

---

## 7. Customize your site (the important bit)

Almost everything is in **`hugo.toml`** under `[params]`:

| Want to change... | Edit |
|-------------------|------|
| Name / tagline / hero bio | `params.author`, `params.tagline`, `params.heroBio` |
| Social links (GitHub, LinkedIn, email…) | `params.github`, `params.linkedin`, `params.email`, … (empty `""` = hidden) |
| **Accent colour** (re-themes the whole site) | `params.accentColor` |
| Starting theme | `params.defaultTheme` (`"dark"` or `"light"`) |
| Top navigation | the `[menu]` block |
| SEO description / keywords / social image | `params.description`, `params.keywords`, `params.ogImage` |
| Your bio, skills, certs | `content/about.md` |

Deeper design changes (spacing, fonts, extra colours) live as **design tokens** at the
top of `assets/css/main.scss` — change a value once, it applies everywhere.

---

## 8. How taxonomies work (why keys are plural)

In Hugo, the front-matter key for a taxonomy is its **plural** name, even when the value
is a single item. That's why you write `difficulties = "Medium"` (not `difficulty`).

| Taxonomy | Used by | Example values |
|----------|---------|----------------|
| `platforms` | writeups **and** detections | Hack The Box, TryHackMe / Windows, Splunk |
| `oses` | writeups | Linux, Windows, macOS |
| `difficulties` | writeups | Easy, Medium, Hard, Insane |
| `tools` | writeups | nmap, burp, ffuf |
| `mitre-techniques` | detections | T1003.001, T1059.001 |
| `log-sources` | detections | Sysmon, Windows Security, Zeek |
| `tags` | anything | privilege-escalation, active-directory |
| `skills` | anything (drives `/portfolio/`) | Active Directory, Detection Engineering |

Each gets an automatic browse page (e.g. `/tags/`, `/mitre-techniques/t1003.001/`).

**Active Directory is a tag, not an OS.** It is a product/service running on Windows,
not an operating system, so it belongs in `tags` (as `active-directory`) with `oses`
reserved for the actual host OS. The writeups archetype reflects this.

**`platforms` is deliberately shared** between writeups and detections, because that is
how it was specified — but the two use it for different things ("Hack The Box" vs
"Splunk"), so `/platforms/` mixes both vocabularies. To stop that, the filter chips on
each list page are built from the terms **that section actually uses**, rather than from
`site.Taxonomies`, so detection platforms never appear as writeup filters or vice versa.
If the mixing on `/platforms/` itself ever bothers you, split it into a separate
`detection-platform` taxonomy in `hugo.toml` and swap the key in
`layouts/partials/detection-badges.html`.

---

## 8b. CI

`.github/workflows/ci.yml` runs on every push to `main` and every pull request:

1. **Build** — `hugo --panicOnWarning`, so a deprecation or template warning fails the run.
2. **Dead links** — [htmltest](https://github.com/wjdp/htmltest) over the built HTML, configured in `.htmltest.yml`.
3. **Secrets** — [gitleaks](https://github.com/gitleaks/gitleaks) across both the working tree and full git history.

All three tool versions are pinned. To reproduce a CI failure locally:

```bash
hugo --gc --minify --panicOnWarning && htmltest
```

If external link checking ever gets flaky because an upstream host rate-limits CI, set
`CheckExternal: false` in `.htmltest.yml` — internal link checking still runs.

---

## 9. Deploy (automatic)

Every push to `main` triggers `.github/workflows/deploy.yml`, which builds the site and
publishes it to GitHub Pages. You never run a deploy command by hand.

**One-time GitHub setup** (see the go-live checklist below) — the only manual step is
switching Pages to build from GitHub Actions.

### Custom domain (optional)

1. Create `static/CNAME` containing just your domain, e.g.:
   ```
   blog.example.com
   ```
2. Set `baseURL = "https://blog.example.com/"` in `hugo.toml`.
3. At your DNS provider, add a `CNAME` record for the subdomain pointing to
   `0xausty.github.io` (for an apex/root domain, add GitHub Pages' four `A` records
   instead — see [GitHub's DNS docs](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site)).
4. In the repo, **Settings → Pages → Custom domain**, enter the domain and enable
   *Enforce HTTPS*.

Without a custom domain, the site lives at `https://<your-username>.github.io/`.

---

## 10. 🚀 Go-live checklist

1. **Create the repo.** For a root site, name it exactly `<your-username>.github.io`
   (this project is set up for `0xausty.github.io`). A different name also works — it'll
   just live at `<user>.github.io/<repo>/`.
2. **Enable Pages FIRST:** repo **Settings → Pages → Build and deployment → Source =
   “GitHub Actions.”**

   > ⚠️ Do this **before** your first push. The `actions/configure-pages` step defaults to
   > `enablement: false`, so if Pages isn't on yet it calls `GET /repos/.../pages`, gets a
   > 404, and the very first workflow run fails with *"Get Pages site failed."* Enabling
   > Pages afterwards does **not** re-run it — you'd have to trigger a re-run manually.
   > (If that happens: **Actions → Deploy Hugo site to Pages → Re-run all jobs**.)
3. **Personalize** `hugo.toml` (name, links, accent colour) and `content/about.md`, and
   replace the placeholder images. Add a real `static/resume.pdf` and set
   `resume = "/resume.pdf"` in `hugo.toml` if you want the Resume button.
4. **Push it:**
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo>.git
   git push -u origin main
   ```
5. Watch the **Actions** tab — the "Deploy Hugo site to Pages" workflow runs and, when
   green, your site is live at the URL shown.
6. *(Optional)* add a custom domain (§9).

### Publishing your next post — every time after that

```bash
hugo new writeups/my-new-box.md   # write it, set draft = false
git add . && git commit -m "Add My New Box writeup"
git push
```

That's it. The site rebuilds and redeploys automatically in ~1 minute.

---

Built with Hugo. Theme and templates are self-contained in `layouts/` and `assets/` —
no external theme to update.
