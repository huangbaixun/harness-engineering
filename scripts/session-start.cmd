: << 'CMDBLOCK'
@echo off
setlocal enableextensions disabledelayedexpansion
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_NAME=session-start"
for %%B in (
    "C:\Program Files\Git\bin\bash.exe"
    "C:\Program Files (x86)\Git\bin\bash.exe"
) do (
    if exist %%B (
        set "HARNESS_BASH=%%~B"
        goto harness_run
    )
)
where bash >nul 2>nul
if errorlevel 1 goto harness_missing
set "HARNESS_BASH=bash"
:harness_run
"%HARNESS_BASH%" "%SCRIPT_DIR%%SCRIPT_NAME%" %*
exit /b %ERRORLEVEL%
:harness_missing
echo [harness-hook] Git Bash / MSYS2 is required; hook was not executed. 1>&2
exit /b 2
CMDBLOCK
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec bash "$SCRIPT_DIR/session-start" "$@"
