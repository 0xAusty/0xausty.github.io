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
├── archetypes/               # templates used by `hugo new` (writeups.md, projects.md)
├── content/
│   ├── _index.md             # homepage (text comes from hugo.toml)
│   ├── about.md              # About page — edit your bio/skills/certs here
│   ├── writeups/             # one .md file per writeup
│   ├── projects/             # one .md file per project
│   └── blog/                 # short notes (optional)
├── layouts/                  # the theme (HTML templates + shortcodes) — rarely touched
├── assets/
│   ├── css/main.scss         # design tokens (colours, spacing, fonts) in one place
│   └── js/                   # copy buttons, theme toggle, lightbox, search
├── static/
│   ├── images/               # your screenshots and images go here
│   └── (add resume.pdf here, then set params.resume in hugo.toml)
└── .github/workflows/deploy.yml   # auto-build + deploy on every push
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
oses         = ["Windows", "Active Directory"]   # one or more
difficulties = "Medium"                # Easy | Medium | Hard | Insane
tools        = ["nmap", "bloodhound", "impacket"]
tags         = ["kerberos", "as-rep-roasting", "active-directory"]

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

See `content/writeups/sample-htb-relay.md` for a full working example of all of these.

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

See `content/projects/subenum.md` for a full example.

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

Recruiters browse by **platform, OS, difficulty, tools, and tags**. In Hugo, the
front-matter key for a taxonomy is its **plural** name, even when the value is a single
item. That's why you write `difficulties = "Medium"` (not `difficulty`). Defined taxonomies:

`platforms` · `oses` · `difficulties` · `tools` · `tags`

Each gets an automatic browse page (e.g. `/tags/`, `/difficulties/medium/`), and the
Writeups page builds its filter chips from them automatically — no config needed.

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
