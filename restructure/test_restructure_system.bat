@echo off
REM Test the restructure safety system

echo ========================================
echo RESTRUCTURE SAFETY SYSTEM - SELF TEST
echo ========================================
echo.
echo Testing all components...
echo.

cd ..
python scripts\maintenance\self_test.py

echo.
pause
