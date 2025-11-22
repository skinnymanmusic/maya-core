@echo off
echo ========================================
echo   Maya v3.0 - Deploy Fix to Railway
echo ========================================
echo.

cd /d C:\Users\delin\maya-ai

echo [1/4] Checking git status...
git status
echo.

echo [2/4] Adding requirements.txt...
git add backend\requirements.txt
echo.

echo [3/4] Committing changes...
git commit -m "Fix: Add missing tenacity dependency for email retry logic"
echo.

echo [4/4] Pushing to GitHub...
git push
echo.

echo ========================================
echo   ✅ DEPLOYMENT TRIGGERED!
echo ========================================
echo.
echo Railway is now deploying your fix...
echo Check your Railway dashboard: https://railway.app
echo.
echo This window will close in 10 seconds...
timeout /t 10
