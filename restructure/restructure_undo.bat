@echo off
REM Maya Repository Restructure - UNDO
REM Safely rolls back to pre-restructure state

echo ========================================
echo MAYA REPOSITORY RESTRUCTURE - UNDO
echo ========================================
echo.
echo This will restore your repository to its
echo state before the restructure.
echo.
echo WARNING: Any changes made AFTER the
echo restructure will be lost.
echo.
echo Press Ctrl+C to cancel, or
pause

cd ..
python scripts\maintenance\undo_restructure.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo RESTORE COMPLETE
    echo ========================================
    echo.
    echo Your repository has been restored.
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR OCCURRED
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
