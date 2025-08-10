# AME (Autonomous Money Engine) — Starter Kit

This is a minimal, **static-site** program that:
- Generates long-tail, useful micro-guides with embedded calculators.
- Ships a daily batch of new pages (you can schedule it).
- Is hostable on any static host (Cloudflare Pages recommended).
- Lets you later add affiliates (Amazon) and ads (AdSense).

## Quick start (Windows PowerShell)

```pwsh
# 1) Create a Python venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r generator\requirements.txt

# 2) Generate the site
python generator\generate.py

# 3) Open the site locally
# On Windows:
start dist\index.html
```

## Daily automation
Use `tasks\schedule_daily_build.ps1` to create a Windows Scheduled Task that rebuilds the site every day at 3:05am local time.

```pwsh
pwsh -File tasks\schedule_daily_build.ps1
```

## Deploying (Cloudflare Pages - simplest path)
1. Create a free Cloudflare account.
2. Create a new **Pages** project and connect the `/dist` output folder (or connect a git repo and build there).
3. Each time you run `python generator\generate.py`, upload or sync `dist/` to Pages.

> Later, add your **Amazon Associates tag** and **AdSense** ID in `site/config.yaml` to monetize automatically.
