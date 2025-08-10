@echo off
set ROOT=C:\AME
"%ROOT%\.venv\Scripts\python.exe" "%ROOT%\generator\expand.py"
"%ROOT%\.venv\Scripts\python.exe" "%ROOT%\generator\generate.py"
powershell -NoProfile -File "%ROOT%\tasks\deploy_pages.ps1" -ProjectRoot "%ROOT%" -ProjectName "tinytoolshub"
