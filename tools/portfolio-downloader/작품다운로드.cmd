@echo off
chcp 65001 >nul
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo [중단] Node.js가 없습니다. 티스토리 업로더의 setup.cmd를 먼저 실행하거나 https://nodejs.org 에서 LTS를 설치해 주세요.
  pause
  exit /b 1
)
if not exist "node_modules\playwright" (
  echo 처음 실행: 필요한 부품을 설치합니다. 1~2분 걸립니다...
  set PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
  call npm install --no-audit --no-fund
  if errorlevel 1 (
    echo [중단] 설치에 실패했습니다. 이 창을 캡처해 Claude에게 보내 주세요.
    pause
    exit /b 1
  )
)
echo 학원 홈페이지 학생 포트폴리오 이미지를 내려받습니다. (작품 수에 따라 수 분~수십 분)
node portfolio.mjs %*
if errorlevel 1 (
  echo [오류] 위 메시지를 캡처해 Claude에게 보내 주세요.
) else (
  echo 결과: 이 폴더의 "학생작품" 폴더 / 학생작품\보기.html 로 한눈에 보기
)
pause
