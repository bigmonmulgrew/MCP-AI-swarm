@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Environment Variable Updater (Multi-env)

set "PREFIX=sample.env"

echo ============================================
echo   Environment Variable Updater (Multi-env)
echo ============================================
echo.

REM --------------------------------------------------
REM Discover sample.env* files
REM --------------------------------------------------
set "FOUND_ANY=0"

echo Found files matching "%PREFIX%*":
echo --------------------------------------------

for %%F in (%PREFIX%*) do (
    echo   - %%F
    set "FOUND_ANY=1"
)

if "!FOUND_ANY!"=="0" (
    echo ERROR: No files found.
    exit /b 1
)


echo --------------------------------------------
echo.

REM --------------------------------------------------
REM Sync each discovered file
REM --------------------------------------------------
for %%F in (%PREFIX%*) do (
    call :sync_env "%%F"
)

echo.
echo ============================================
echo [OK] All environment files processed
echo ============================================
pause
exit /b



REM ==================================================
REM sync_env
REM %1 = sample file
REM ==================================================
:sync_env
setlocal EnableDelayedExpansion

set "SAMPLE_FILE=%~1"

REM ----- derive target file safely -----
if /i "%SAMPLE_FILE%"=="sample.env" (
    set "TARGET_FILE=.env"
) else (
    set "TARGET_FILE=.env%SAMPLE_FILE:sample.env=%"
)

echo.
echo --------------------------------------------
echo Syncing %TARGET_FILE% from %SAMPLE_FILE%
echo --------------------------------------------

REM ----- temp files -----
set "TEMP_NEW=%TARGET_FILE%.new"
set "TEMP_KEYS=%TARGET_FILE%.keys"
set "TEMP_EXTRA=%TARGET_FILE%.extra"
set "TEMP_ADDED=%TARGET_FILE%.added"

del "%TEMP_NEW%" "%TEMP_KEYS%" "%TEMP_EXTRA%" "%TEMP_ADDED%" >nul 2>&1

REM ----- create target if missing -----
if not exist "%TARGET_FILE%" (
    echo %TARGET_FILE% not found. Creating from %SAMPLE_FILE%...
    copy "%SAMPLE_FILE%" "%TARGET_FILE%" >nul
    endlocal
    goto :eof
)

REM ----- process sample file -----
for /f "usebackq delims=" %%L in (`findstr /n "^" "%SAMPLE_FILE%"`) do (
    set "line=%%L"
    set "line=!line:*:=!"
    call :process_line "%TARGET_FILE%" "%TEMP_NEW%" "%TEMP_KEYS%" "%TEMP_ADDED%"
)

REM ----- detect extra keys -----
for /f "tokens=1 delims==" %%A in (
    'findstr /r "^[^#][^=]*=" "%TARGET_FILE%"'
) do (
    if not "%%A"=="" (
        findstr /b /i "%%A=" "%TEMP_KEYS%" >nul
        if errorlevel 1 (
            echo %%A>>"%TEMP_EXTRA%"
        )
    )
)

REM ----- append extras -----
if exist "%TEMP_EXTRA%" (
    >>"%TEMP_NEW%" echo.
    >>"%TEMP_NEW%" echo # Extra variables kept from previous file
    echo Extra variables kept from previous file:
    for /f "usebackq delims=" %%X in ("%TEMP_EXTRA%") do (
        for /f "tokens=1,* delims==" %%C in ('findstr /b /i "%%X=" "%TARGET_FILE%"') do (
            >>"%TEMP_NEW%" echo %%C=%%D
            echo   + %%C
        )
    )
)

REM ----- replace target -----
copy "%TEMP_NEW%" "%TARGET_FILE%" /Y >nul

if exist "%TEMP_ADDED%" (
    echo.
    echo New variables added to %TARGET_FILE%:
    for /f "usebackq delims=" %%A in ("%TEMP_ADDED%") do (
        echo   + %%A
    )

)

del "%TEMP_NEW%" "%TEMP_KEYS%" "%TEMP_EXTRA%" "%TEMP_ADDED%" >nul 2>&1

echo [OK] %TARGET_FILE% synced successfully
endlocal
goto :eof


REM ==================================================
REM process_line
REM ==================================================
:process_line
setlocal EnableDelayedExpansion

set "TARGET=%~1"
set "OUT=%~2"
set "KEYS=%~3"
set "ADDED=%~4"

REM blank line
if "!line!"=="" (
    >>"%OUT%" echo.
    endlocal
    goto :eof
)

REM comment
if "!line:~0,1!"=="#" (
    >>"%OUT%" echo !line!
    endlocal
    goto :eof
)

REM key/value
for /f "tokens=1,* delims==" %%A in ("!line!") do (
    set "key=%%A"
    set "value=%%B"
)

if "!key!"=="" (
    endlocal
    goto :eof
)

>>"%KEYS%" echo !key!=

set "existing="
for /f "tokens=1,* delims==" %%C in (
    'findstr /b /i "!key!=" "%TARGET%"'
) do (
    set "existing=%%D"
)

if defined existing (
    >>"%OUT%" echo !key!=!existing!
) else (
    >>"%OUT%" echo !key!=!value!
    >>"%ADDED%" echo !key!
)

endlocal
goto :eof
