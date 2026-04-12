: << 'CMDBLOCK'
@echo off
setlocal enableextensions

:: Polyglot hook wrapper — valid in both CMD and bash
:: CMD: finds Git for Windows bash, then delegates to the extensionless script
:: bash: skips this block via heredoc, then exec's the script directly

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_NAME=post-observe"

:: Try Git for Windows standard locations
for %%B in (
    "C:\Program Files\Git\bin\bash.exe"
    "C:\Program Files (x86)\Git\bin\bash.exe"
) do (
    if exist %%B (
        %%B "%SCRIPT_DIR%%SCRIPT_NAME%" %*
        exit /b %ERRORLEVEL%
    )
)

:: Try PATH
where bash >/dev/null 2>/dev/null
if %ERRORLEVEL% equ 0 (
    bash "%SCRIPT_DIR%%SCRIPT_NAME%" %*
    exit /b %ERRORLEVEL%
)

:: No bash found — silent success (hook is optional)
exit /b 0
CMDBLOCK

# bash execution path — heredoc above is consumed as no-op
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec bash "$SCRIPT_DIR/post-observe" "$@"
