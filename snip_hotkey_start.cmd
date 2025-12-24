@echo off
setlocal
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

:: start hidden (no window) via pythonw
start /min "" pythonw "snip_hotkey.py"

endlocal
exit /b 0