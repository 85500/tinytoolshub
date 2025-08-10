param(
  [string]$ProjectRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path).Replace('\tasks',''),
  [string]$Time = "03:10",
  [string]$ProjectName = "tinytoolshub"
)

$python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$expand = Join-Path $ProjectRoot "generator\expand.py"
$build = Join-Path $ProjectRoot "generator\generate.py"
$deploy = Join-Path $ProjectRoot "tasks\deploy_pages.ps1"

$Action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-NoLogo -NoProfile -Command `"$python `"$expand`"; $python `"$build`"; pwsh -File `"$deploy`" -ProjectRoot `"$ProjectRoot`" -ProjectName `"$ProjectName`"`""
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time
$Settings = New-ScheduledTaskSettingsSet -Hidden:$false -AllowStartIfOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "AME_AutoGrowAndDeploy" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Adds new pages, rebuilds, and deploys daily" -Force

Write-Host "Scheduled AME_AutoGrowAndDeploy daily at $Time."
