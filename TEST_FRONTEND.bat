@echo off
REM =================================================================
REM MAYA FRONTEND TESTING SCRIPT
REM Automated by Claude for Skinny - Beginner-friendly!
REM =================================================================

echo ========================================
echo MAYA FRONTEND TEST SUITE
echo ========================================
echo.

cd /d "%~dp0omega-frontend"

echo [1/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found! Please install from https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js found: 
node --version
echo.

echo [2/5] Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm not found! This should come with Node.js
    pause
    exit /b 1
)
echo ✅ npm found:
npm --version
echo.

echo [3/5] Checking dependencies...
if not exist "node_modules" (
    echo ⚠️  node_modules not found. Installing dependencies...
    echo This may take a few minutes...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ npm install failed!
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed!
) else (
    echo ✅ Dependencies already installed
)
echo.

echo [4/5] Building production version...
echo This will test if everything compiles correctly...
npm run build
if %errorlevel% neq 0 (
    echo ❌ Build failed! Check errors above.
    echo.
    echo Saving build log to FRONTEND_BUILD_ERROR.log...
    npm run build > ..\FRONTEND_BUILD_ERROR.log 2>&1
    pause
    exit /b 1
)
echo ✅ Build successful!
echo.

echo [5/5] Starting development server...
echo.
echo ============================================
echo SERVER STARTING!
echo ============================================
echo.
echo The frontend will open at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server when done testing.
echo.
pause

npm run dev
