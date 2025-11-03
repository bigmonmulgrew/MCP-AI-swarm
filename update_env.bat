@echo off
title MCO Tool - Update Environment Variables
echo ============================================
echo       MCO TOOL - UPDATE .ENV FILE
echo ============================================

REM Step 1: Ensure sample.env exists
if not exist "sample.env" (
    echo ERROR: sample.env not found. Please ensure it exists in this folder.
    pause
    exit /b
)

REM Step 2: If .env does not exist, create it from sample.env
if not exist ".env" (
    echo .env not found. Creating new one from sample.env...
    copy sample.env .env >nul
    echo Created .env successfully.
    pause
    exit /b
)

echo.
echo ============================================
echo Syncing .env with sample.env (preserving comments and spacing)...
echo ============================================

setlocal enabledelayedexpansion
set "TEMP_NEW=.env.new"
set "TEMP_OLD=.env"
set "TEMP_KEYS=.env.keys"
set "TEMP_EXTRA=.env.extra"

del "%TEMP_NEW%" >nul 2>&1
del "%TEMP_KEYS%" >nul 2>&1
del "%TEMP_EXTRA%" >nul 2>&1

REM Step 3: Loop through each line in sample.env
for /f "usebackq delims=" %%L in ("sample.env") do (
    set "line=%%L"
    call :process_line
)

REM Step 4: Detect extra keys that exist in .env but not in sample.env
for /f "tokens=1,* delims== eol=#" %%A in ('findstr /r "^[^#][^=]*=" "%TEMP_OLD%"') do (
    set "envkey=%%A"
    findstr /b /i "!envkey!=" "%TEMP_KEYS%" >nul
    if errorlevel 1 (
        echo !envkey!>>"%TEMP_EXTRA%"
        echo ##### Keeping extra variable: !envkey!
    )
)

REM Step 5: Append extra keys to the bottom of the file
if exist "%TEMP_EXTRA%" (
    >>"%TEMP_NEW%" echo.
    >>"%TEMP_NEW%" echo # Extra variables kept from previous .env
    for /f "usebackq delims=" %%X in ("%TEMP_EXTRA%") do (
        for /f "tokens=1,* delims== eol=#" %%C in ('findstr /b /i "%%X=" "%TEMP_OLD%"') do (
            >>"%TEMP_NEW%" echo %%X=%%D
        )
    )
)

REM Step 6: Replace old .env with formatted new one
copy "%TEMP_NEW%" ".env" /Y >nul
del "%TEMP_NEW%" "%TEMP_KEYS%" >nul 2>&1

echo.
if exist "%TEMP_EXTRA%" (
    echo ============================================
    echo [WARNING] The following variables exist in .env but not in sample.env:
    type "%TEMP_EXTRA%"
    echo ============================================
) else (
    echo No unmatched variables found.
)
del "%TEMP_EXTRA%" >nul 2>&1

echo [OK] .env update complete (spacing, values, and extras preserved)
echo ============================================
pause
exit /b


REM -------------------------------------------------------------------
REM Helper function :process_line
REM Adds a blank line before comments for readability
REM -------------------------------------------------------------------
:process_line
setlocal enabledelayedexpansion
set "trim=!line: =!"

if "!trim!"=="" (
    endlocal
    goto :eof
)

if "!trim:~0,1!"=="#" (
    >>"%TEMP_NEW%" echo.
    >>"%TEMP_NEW%" echo !line!
    endlocal
    goto :eof
)

REM Otherwise, it's a variable line
for /f "tokens=1,* delims== eol=#" %%A in ("!line!") do (
    set "key=%%A"
    set "value=%%B"
)

REM Save this key to TEMP_KEYS for later comparison
>>"%TEMP_KEYS%" echo !key!=

REM Check if it already exists in .env
set "existing="
for /f "tokens=1,* delims== eol=#" %%C in ('findstr /b /i "!key!=" "%TEMP_OLD%"') do (
    set "existing=%%D"
)

if defined existing (
    echo Keeping existing: !key!
    >>"%TEMP_NEW%" echo !key!=!existing!
) else (
    echo Adding new variable: !key!
    >>"%TEMP_NEW%" echo !key!=!value!
)

endlocal
goto :eof
