#!/usr/bin/env bash
# "그려줘" 실행기 — 구독 계정(OAuth)으로 로그인된 CLI로 이미지 생성 → ./images/날짜_도구명.png
#   사용: tools/image-cli/draw.sh --tool agy|codex|both --ratio square|portrait|landscape --prompt "<영어 프롬프트>"
# API 키를 쓰지 않는다. 로그인 안 되어 있으면 안내만 하고 멈춘다.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"
TOOL=agy; RATIO=square; PROMPT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --tool) TOOL="$2"; shift 2;;
    --ratio) RATIO="$2"; shift 2;;
    --prompt) PROMPT="$2"; shift 2;;
    *) echo "알 수 없는 옵션: $1" >&2; exit 2;;
  esac
done
[ -z "$PROMPT" ] && { echo "--prompt 가 필요합니다" >&2; exit 2; }
case "$RATIO" in
  square) AR="square 1:1"; ;; portrait) AR="vertical portrait 3:4"; ;; landscape) AR="horizontal landscape 16:9"; ;;
  *) echo "비율은 square|portrait|landscape" >&2; exit 2;;
esac
OUT="./images"; mkdir -p "$OUT"; DATE=$(date +%F)
MARK=$(mktemp); sleep 1

outname() { local f="$OUT/${DATE}_$1.png" n=2; while [ -e "$f" ]; do f="$OUT/${DATE}_$1_$n.png"; n=$((n+1)); done; echo "$f"; }
to_png() { # $1 원본 → $2 PNG (playwright로 변환, 실패하면 확장자 유지 복사)
  local src="$1" dst="$2"
  case "$src" in *.png) cp "$src" "$dst"; echo "$dst"; return;; esac
  if PW_SRC="$src" PW_DST="$dst" node -e '
const pw=require(process.env.PW||"/opt/node22/lib/node_modules/playwright");(async()=>{const b=await pw.chromium.launch();
const p=await b.newPage({viewport:{width:2048,height:2048}});await p.goto("file://"+process.env.PW_SRC);
const [w,h]=await p.evaluate(()=>[document.images[0].naturalWidth,document.images[0].naturalHeight]);
await p.setViewportSize({width:w+40,height:h+40});await p.waitForTimeout(300);
await p.locator("img").screenshot({path:process.env.PW_DST});await b.close()})().catch(e=>{console.error(e);process.exit(1)})' 2>/dev/null; then echo "$dst"
  else local alt="${dst%.png}.${src##*.}"; [ "$src" -ef "$alt" ] || cp "$src" "$alt"; echo "$alt"; fi
}
wait_new() { # $1 찾을 폴더, 최대 300초 대기 → 새 이미지 경로
  for _ in $(seq 1 60); do
    f=$(find "$1" -newer "$MARK" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' \) 2>/dev/null | head -1)
    [ -n "$f" ] && { echo "$f"; return 0; }; sleep 5
  done; return 1
}

run_agy() {
  command -v agy >/dev/null || { echo "[agy] 미설치 — tools/image-cli/setup.sh 실행 필요"; return 1; }
  timeout 40 agy models >/dev/null 2>&1 || { echo "[agy] 로그인 필요 — 'agy'를 인자 없이 실행해 구글 로그인"; return 1; }
  agy -p "Use your generate_image tool to create ONE image, aspect ratio ${AR}. Image prompt: ${PROMPT}. Do not write or modify any files; just generate the image." \
      --mode accept-edits --print-timeout 540s >/dev/null 2>&1
  local f; f=$(wait_new "$HOME/.gemini/antigravity-cli/brain") || { echo "[agy] 이미지가 만들어지지 않았습니다"; return 1; }
  echo "[agy] 저장: $(to_png "$f" "$(outname antigravity)")"
}
run_codex() {
  command -v codex >/dev/null || { echo "[codex] 미설치 — tools/image-cli/setup.sh 실행 필요"; return 1; }
  codex login status 2>&1 | grep -q "Logged in using ChatGPT" || { echo "[codex] 로그인 필요 — 'codex login --device-auth'"; return 1; }
  mkdir -p "$HOME/.codex/generated_images"
  codex exec -s read-only "Use ONLY your built-in image_gen tool to create ONE image, aspect ratio ${AR}. Image prompt: ${PROMPT}. If the built-in image_gen tool is unavailable, reply exactly IMAGE_TOOL_UNAVAILABLE and stop. Never use the CLI fallback or any API key." >/tmp/codex_draw.log 2>&1
  grep -q IMAGE_TOOL_UNAVAILABLE /tmp/codex_draw.log && { echo "[codex] 이 계정에서 내장 이미지 도구가 제공되지 않습니다(ChatGPT Free 요금제 추정)"; return 1; }
  local f; f=$(wait_new "$HOME/.codex/generated_images") || { echo "[codex] 이미지가 만들어지지 않았습니다"; return 1; }
  echo "[codex] 저장: $(to_png "$f" "$(outname codex)")"
}

case "$TOOL" in
  agy) run_agy;; codex) run_codex;; both) run_codex; run_agy;;
  *) echo "도구는 agy|codex|both" >&2; exit 2;;
esac
rm -f "$MARK"
