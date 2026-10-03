@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ===== Post 4 =====
node upload.mjs clean 4
echo.
echo ===== Post 5 =====
node upload.mjs clean 5
pause
