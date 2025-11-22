@echo off
REM MASTER HELP - Shows all available commands

cls
echo ═══════════════════════════════════════════════════════════════════
echo           MAYA REPOSITORY RESTRUCTURE - HELP MENU
echo ═══════════════════════════════════════════════════════════════════
echo.
echo  📁 Location: restructure\ folder
echo.
echo  Available Commands (just double-click any .bat file):
echo.
echo ───────────────────────────────────────────────────────────────────
echo  📚 DOCUMENTATION
echo ───────────────────────────────────────────────────────────────────
echo.
echo    RESTRUCTURE_START_HERE.md      Quick start guide
echo    SYSTEM_COMPLETE.md             Complete system documentation
echo    VISUAL_WORKFLOW.md             Visual workflow diagram
echo    ..\scripts\maintenance\README.md  Detailed technical docs
echo.
echo ───────────────────────────────────────────────────────────────────
echo  🔧 MAIN COMMANDS (Use these!)
echo ───────────────────────────────────────────────────────────────────
echo.
echo    test_restructure_system.bat    Test that everything works
echo    restructure_preview.bat        Preview changes (SAFE!)
echo    restructure_execute.bat        Execute restructure (with backup)
echo    restructure_undo.bat           Undo/rollback changes
echo    check_structure.bat            Check current structure
echo.
echo ───────────────────────────────────────────────────────────────────
echo  🚀 RECOMMENDED WORKFLOW
echo ───────────────────────────────────────────────────────────────────
echo.
echo    1. test_restructure_system.bat  ← Start here!
echo    2. restructure_preview.bat      ← See what will change
echo    3. restructure_execute.bat      ← Do it!
echo    4. restructure_undo.bat         ← Only if needed
echo.
echo ───────────────────────────────────────────────────────────────────
echo  💡 QUICK TIPS
echo ───────────────────────────────────────────────────────────────────
echo.
echo    • Always preview first (it's safe!)
echo    • Everything is backed up automatically
echo    • You can undo anytime with one command
echo    • Backups stored in: ..\.restructure_backups\
echo    • Cannot lose data - everything is protected
echo.
echo ───────────────────────────────────────────────────────────────────
echo  🆘 IF SOMETHING GOES WRONG
echo ───────────────────────────────────────────────────────────────────
echo.
echo    Just run: restructure_undo.bat
echo    Everything will be restored perfectly!
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Press any key to close this help menu...
pause >nul
