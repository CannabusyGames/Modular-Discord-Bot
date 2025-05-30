@echo off
setlocal

REM Get the absolute path to the folder this script is in
set SCRIPT_DIR=%~dp0

REM Launching the bot...
start "DealerBot - Bot" cmd /k python "%SCRIPT_DIR%lib\Main.py"

REM Launching the control panel...
start "DealerBot - ControlPanel" cmd /k python "%SCRIPT_DIR%lib\ControlPanel.py"

endlocal
exit
