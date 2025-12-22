@echo off
setlocal
set SCRIPT_DIR=C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey
cd /d "%SCRIPT_DIR%"

:: stop existing snip_hotkey.py (python / pythonw) by command line match
powershell -NoLogo -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'snip_hotkey.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1

:: start hidden (no window) via pythonw (pyw launcher)
powershell -NoLogo -WindowStyle Hidden -Command ^
  "Start-Process -WindowStyle Hidden -FilePath 'pyw' -ArgumentList '\"snip_hotkey.py\"' -WorkingDirectory '%SCRIPT_DIR%'"

endlocal
exit /b 0
