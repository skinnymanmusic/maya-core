@echo off
REM Maya Repository Restructure - EXECUTE
REM Actually performs the restructure with full safety backups

echo ========================================
echo MAYA REPOSITORY RESTRUCTURE - EXECUTE
echo ========================================
echo.
echo WARNING: This will restructure your repository.
echo.
echo Safety features:
echo  - Complete backup created first
echo  - All references automatically updated
echo  - Full validation before and after
echo  - One-command undo available
echo.
echo Press Ctrl+C to cancel, or
pause

cd ..
python scripts\maintenance\restructure_repo.py --execute

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Your repository has been restructured.
    echo.
    echo If you need to undo:
    echo    cd restructure
    echo    restructure_undo.bat
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR OCCURRED
    echo ========================================
    echo.
    echo Something went wrong. You can undo with:
    echo    cd restructure
    echo    restructure_undo.bat
    echo.
)

pause
