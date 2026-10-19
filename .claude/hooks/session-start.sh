#!/bin/bash
# 웹(원격) 세션 시작 시 "그려줘"용 CLI(Codex·Antigravity)를 없을 때만 설치. 로그인은 하지 않음.
set -euo pipefail
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi
bash "$CLAUDE_PROJECT_DIR/tools/image-cli/setup.sh" || true
# agy 설치 경로를 세션 PATH에 추가
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CLAUDE_ENV_FILE"
fi
