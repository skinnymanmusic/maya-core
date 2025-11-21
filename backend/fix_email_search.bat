@echo off
REM Phase 0: Email Search Fix
REM Executes the Python fix script

cd /d "%~dp0"

echo.
echo ============================================================
echo PHASE 0: EMAIL SEARCH FIX
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.14 or later.
    pause
    exit /b 1
)

REM Run the fix script
python fix_email_search.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Fix script failed. Check the output above.
    echo ============================================================
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS: Email search fix complete!
echo ============================================================
echo.
pause

