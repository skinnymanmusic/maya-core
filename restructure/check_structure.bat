@echo off
REM Maya Repository Integrity Check
REM Validates repository structure is clean and organized

echo ========================================
echo MAYA REPOSITORY INTEGRITY CHECK
echo ========================================
echo.
echo Checking for structure violations...
echo.

cd ..
python scripts\maintenance\structure_integrity_checker.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Repository structure is clean!
) else (
    echo.
    echo ✗ Structure violations found.
    echo   See suggestions above to fix.
)

echo.
pause
