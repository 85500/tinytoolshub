param(
    [string]$ProjectRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path).Replace('\tasks','')
)

$pythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$scriptPath = Join-Path $ProjectRoot "generator\generate.py"
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At 3:05am
$settings = New-ScheduledTaskSettingsSet -Hidden:$false -AllowStartIfOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "AME_DailyBuild" -Action $action -Trigger $trigger -Settings $settings -Description "Builds AME static site daily" -Force
Write-Host "Scheduled AME_DailyBuild for 3:05am local time."
