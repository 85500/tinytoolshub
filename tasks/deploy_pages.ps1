param(
  [string]$ProjectRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path).Replace('\tasks',''),
  [string]$ProjectName = "tinytoolshub"
)
$dist = Join-Path $ProjectRoot "dist"
wrangler pages deploy $dist --project-name $ProjectName --branch main
