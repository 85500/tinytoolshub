# AME Phase 2 Update
This update adds:
- **Auto-expansion** (`generator/expand.py`) to create N new pages/day.
- **Cloudflare deploy scripts** (`tasks/setup_cloudflare.ps1`, `tasks/deploy_pages.ps1`, `tasks/schedule_full.ps1`).
- **Affiliate tag injection** for Amazon links via `site/config.yaml: amazon_tag`.
- **Two new calculators**: `percent-calc`, `filament-estimator`.
- **Offer rotator**: shuffles recommendations for light A/B.

## Apply the update
Unzip this over your existing AME folder (allow overwrite). Then run:

```pwsh
# From your AME folder
# 1) Rebuild venv deps (no new Python deps added, safe to skip)
.\.venv\Scripts\python.exe generator\generate.py

# 2) First-time Cloudflare setup + deploy (follow prompts)
pwsh -File tasks\setup_cloudflare.ps1

# 3) Schedule nightly growth + deploy at 3:10 AM
pwsh -File tasks\schedule_full.ps1
```

Add monetization later by editing `site\config.yaml`:
- `amazon_tag: yourtag-20`
- `adsense_client_id: ca-pub-XXXXXXXX`
