@echo off
chcp 65001 >nul
title Claude 리모트 컨트롤 (이 창을 닫으면 연결이 끊깁니다)
rem 작업 폴더: 업로더·원고가 있는 블로그 폴더. 경로가 바뀌면 아래 한 줄만 고치세요.
set "WORKDIR=D:\정리파일\박현용\블로그"

if not exist "%WORKDIR%" (
  echo [중단] 폴더를 찾을 수 없습니다: %WORKDIR%
  echo 이 파일을 메모장으로 열어 WORKDIR 경로를 고쳐 주세요.
  pause
  exit /b 1
)
where claude >nul 2>nul
if errorlevel 1 (
  echo [중단] Claude Code가 설치되어 있지 않습니다.
  echo PowerShell에서 다음을 실행한 뒤 다시 시도하세요:  irm https://claude.ai/install.ps1 ^| iex
  pause
  exit /b 1
)

cd /d "%WORKDIR%"
echo 작업 폴더: %CD%
echo Claude 앱의 Code 목록에 컴퓨터 아이콘 세션이 나타나면 연결 완료입니다.
echo 이 창은 닫지 말고 최소화해 두세요.
echo.

:run
claude remote-control
echo.
echo 리모트 컨트롤이 종료되었습니다. 30초 뒤 다시 연결합니다. (그만하려면 이 창을 닫으세요)
timeout /t 30
goto run
