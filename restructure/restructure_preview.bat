@echo off
REM Maya Repository Restructure - DRY RUN
REM Shows what will be changed without making any modifications

echo ========================================
echo MAYA REPOSITORY RESTRUCTURE - DRY RUN
echo ========================================
echo.
echo This will show you what changes will be made
echo WITHOUT actually modifying anything.
echo.
pause

cd ..
python scripts\maintenance\restructure_repo.py --dry-run

echo.
echo ========================================
echo DRY RUN COMPLETE
echo ========================================
echo.
echo If everything looks good, run:
echo    restructure_execute.bat
echo.
pause
