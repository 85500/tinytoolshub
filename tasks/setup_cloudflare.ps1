param(
  [string]$ProjectRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path).Replace('\tasks',''),
  [string]$ProjectName = "tinytoolshub"
)

Write-Host "Installing Node.js LTS (if missing) via winget..."
try { node -v | Out-Null } catch { winget install -e --id OpenJS.NodeJS.LTS -h }
Write-Host "Installing Wrangler CLI..."
npm i -g wrangler

Write-Host "Logging into Cloudflare (follow browser prompts)..."
wrangler login

Write-Host "Creating/ensuring Pages project '$ProjectName'..."
wrangler pages project create $ProjectName --production-branch main --compatibility-flags nodejs_compat --accept-tos

Write-Host "Deploying dist/ ..."
$dist = Join-Path $ProjectRoot "dist"
wrangler pages deploy $dist --project-name $ProjectName --branch main
