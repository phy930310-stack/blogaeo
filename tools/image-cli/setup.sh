#!/usr/bin/env bash
# "그려줘"용 CLI 설치(없을 때만) + Antigravity 최소 권한 설정. 로그인은 하지 않는다(사용자가 직접).
# 공식 출처: Codex = npm @openai/codex / Antigravity = https://antigravity.google/cli/install.sh (SHA-512 검증 내장)
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
if ! command -v codex >/dev/null; then
  echo "[setup] Codex CLI 설치"; npm install -g @openai/codex >/dev/null 2>&1 || echo "[setup] Codex 설치 실패"
fi
if ! command -v agy >/dev/null; then
  echo "[setup] Antigravity CLI 설치"
  tmp=$(mktemp) && curl -fsSL https://antigravity.google/cli/install.sh -o "$tmp" && bash "$tmp" >/dev/null 2>&1 || echo "[setup] Antigravity 설치 실패"
  rm -f "$tmp"
fi
# Antigravity 최소 권한(이미지 폴더 생성·복사·이동만 허용, rm -rf 금지)
python3 - <<'PY'
import json, os
p = os.path.expanduser("~/.gemini/antigravity-cli/settings.json")
os.makedirs(os.path.dirname(p), exist_ok=True)
s = json.load(open(p)) if os.path.exists(p) and os.path.getsize(p) else {}
perm = s.setdefault("permissions", {})
allow = perm.setdefault("allow", []); deny = perm.setdefault("deny", [])
for r in ["command(mkdir -p images)", "command(cp)", "command(mv)", "command(ls)"]:
    if r not in allow: allow.append(r)
if "command(rm -rf)" not in deny: deny.append("command(rm -rf)")
json.dump(s, open(p, "w"), indent=2, ensure_ascii=False)
PY
printf "[setup] codex: %s / agy: %s\n" "$(codex --version 2>/dev/null || echo 없음)" "$(agy --version 2>/dev/null | tail -1 || echo 없음)"
codex login status 2>&1 | grep -q "Logged in" && echo "[setup] ChatGPT 로그인: 됨" || echo "[setup] ChatGPT 로그인: 필요 (codex login --device-auth)"
timeout 30 agy models >/dev/null 2>&1 && echo "[setup] 구글 로그인: 됨" || echo "[setup] 구글 로그인: 필요 (agy 실행)"
