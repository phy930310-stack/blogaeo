@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [1/3] Node.js check
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js not found. Installing with winget...
  winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
  if errorlevel 1 (
    echo [FAIL] Please install Node.js LTS from https://nodejs.org and run setup.cmd again.
    pause
    exit /b 1
  )
  echo Node.js installed. Close this window and run setup.cmd again.
  pause
  exit /b 0
)
node -v
echo [2/3] Installing packages (browser download skipped: uses installed Chrome/Edge)
set PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
call npm install --no-audit --no-fund
if errorlevel 1 (
  echo [FAIL] npm install failed.
  pause
  exit /b 1
)
echo [3/3] Config
if not exist config.json copy config.example.json config.json >nul
if not exist posts mkdir posts
echo.
echo Done. Check blogUrl in config.json, then run login.cmd
pause
