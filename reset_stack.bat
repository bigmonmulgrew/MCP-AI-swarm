@echo off
title MCO Tool - Reset and Rebuild Docker Stack
echo ============================================
echo        MCO TOOL DOCKER STACK RESET
echo ============================================

REM Step 1: Ensure .env exists
if not exist ".env" (
    echo .env file not found. Creating one from sample.env...
    if exist "sample.env" (
        copy sample.env .env >nul
        echo Created .env from sample.env
    ) else (
        echo ERROR: sample.env not found. Please create one first.
        pause
        exit /b
    )
) else (
    echo .env file found.
)

echo.
echo ============================================
echo Loading environment variables...
echo ============================================

REM Step 2: Load selected environment variables from .env
setlocal enabledelayedexpansion
for /f "usebackq tokens=1,2 delims== eol=#" %%A in (".env") do (
    if not "%%A"=="" set "%%A=%%B"
)
endlocal & (
    set "OLLAMA_PORT_E=%OLLAMA_PORT_E%"
    set "MCPS_PORT_E=%MCPS_PORT_E%"
    set "FRONTEND_PORT_E=%FRONTEND_PORT_E%"
)

echo   OLLAMA_PORT_E = %OLLAMA_PORT_E%
echo   MCPS_PORT_E    = %MCPS_PORT_E%
echo   FRONTEND_PORT_E = %FRONTEND_PORT_E%

echo.
echo ============================================
echo Rebuilding the Docker stack...
echo ============================================

REM Step 3: Stop and rebuild the full stack
docker compose down --volumes --remove-orphans
docker compose build --no-cache
docker compose up -d

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo ERROR: Docker stack failed to build.
    echo Please check your Docker configuration and try again.
    echo ============================================
    pause
    exit /b
)

echo.
echo ============================================
echo [OK] Docker stack rebuild complete!
echo ============================================

echo.
echo You can now test each container as follows:
echo.
echo   OLLAMA CONTAINER:
echo       docker exec -it ollama-container ollama list
echo       docker exec -it ollama-container ollama run llama3.2 "Hello"
echo.
echo   MCPS CONTAINER:
echo       Visit: http://localhost:%MCPS_PORT_E%/status
echo       or FastAPI docs: http://localhost:%MCPS_PORT_E%/docs
echo.
echo   FRONTEND CONTAINER:
echo       Visit: http://localhost:%FRONTEND_PORT_E%
echo       Click "Check MCPS Status" to confirm frontend ↔ MCPS link
echo.
echo ============================================
echo Stack is now running and ready for testing!
echo ============================================

pause
