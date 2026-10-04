@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 학원 홈페이지 학생 포트폴리오 이미지를 내려받습니다. (작품 수에 따라 수 분~수십 분)
node portfolio.mjs %*
echo.
echo 결과: 이 폴더의 "학생작품" 폴더 / 학생작품\보기.html 로 한눈에 보기
pause
