@echo off
cd /d "C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey"
for /f "tokens=2 delims=," %%P in ('tasklist /FI "IMAGENAME eq pwsh.exe" /FI "WINDOWTITLE eq snip_hotkey" /FO CSV /NH') do taskkill /PID %%P /F >nul 2>&1
start "snip_hotkey" /min pwsh -NoLogo -Command "cd \"C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\"; py snip_hotkey.py"
exit /b 0
