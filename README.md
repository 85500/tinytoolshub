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

## Redirect Preflight — paid offline tool

Redirect Preflight checks a website migration's redirect CSV before deployment. It flags loops, conflicting rules, chains and duplicates, then exports a review report and deduplicated candidate rules.

- [Try the 25-row checker and view the product](https://redirect-preflight-ji.silver-pika-6542.chatgpt.site/)
- [Buy the offline edition — $29 once](https://redirect-preflight-ji.silver-pika-6542.chatgpt.site/buy)
- [Migration preflight checklist](guides/redirect-map-preflight-checklist.md)

The paid ZIP contains a self-contained HTML checker for up to 20,000 rows / 5 MB, an example CSV and instructions. Use it on your own business and client projects. Files are processed locally; no API credits or subscription are needed. The checker does not crawl websites or verify live HTTP responses. Delivery follows verified payment. [Terms and 14-day refund requests](https://redirect-preflight-ji.silver-pika-6542.chatgpt.site/terms).

**Disclosure:** Redirect Preflight is sold by this project's owner, Jon Ireland. This listing is a product announcement, not an independent review or a claim of established revenue.
