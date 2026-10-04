"""네이버 붙여넣기용 HTML 생성 — 네이버_본문.txt → 네이버_붙여넣기용.html
사용: python3 .claude/skills/aeo-blog/scripts/build_naver_html.py posts/<폴더>

- 브라우저로 열고 [본문 복사] 버튼 → 네이버 편집기 본문에 Ctrl+V
- 생성 이미지는 파일 안에 넣어(data URI) 함께 복사되게 한다
- 실제 사진·지도 자리는 노란 안내 줄 1줄 (사진/지도 넣은 뒤 그 줄만 삭제)
- 제목·태그는 별도 [복사] 버튼 (본문 복사에 섞이지 않음)
"""
import base64, html, json, re, sys
from pathlib import Path

d = Path(sys.argv[1])
meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
lines = (d / "네이버_본문.txt").read_text(encoding="utf-8").splitlines()

BODY = "font-size:15px;line-height:1.8;color:#222;margin:0;"
H2 = "font-size:19px;font-weight:bold;line-height:1.6;color:#1E2A78;margin:0;"
QT = "font-size:15px;line-height:1.8;color:#333;margin:0;"
CAP = "font-size:13px;line-height:1.6;color:#888;text-align:center;margin:0;"
MARK = "font-size:14px;line-height:1.6;background:#FFF3B0;color:#6B5500;margin:0;"


def esc(s):
    return html.escape(s, quote=False)


def link(s):  # http 주소를 링크로
    return re.sub(r"(https?://\S+)", lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)


def img_tag(name):
    f = d / "images" / name
    b64 = base64.b64encode(f.read_bytes()).decode()
    return f'<p style="text-align:center;margin:0;"><img src="data:image/png;base64,{b64}" alt="" style="width:100%;max-width:700px;"></p>'


out, quote, imgs, photos = [], False, 0, 0
for raw in lines:
    s = raw.rstrip()
    if quote and not s:
        quote = False
    if not s:
        out.append('<p style="margin:0;"><br></p>')
        continue
    m = re.match(r"\[이미지:\s*(.+?)\s*/\s*사진 설명:\s*(.+?)\]$", s)
    if m:
        out.append(img_tag(m.group(1)))
        out.append(f'<p style="{CAP}">{esc(m.group(2))}</p>')
        imgs += 1
        continue
    m = re.match(r"\[실제 사진 (\d+):\s*(.+?)\s*/\s*사진 설명:\s*(.+?)\]$", s)
    if m:
        out.append(f'<p style="{MARK}">📷 [실제 사진 {m.group(1)} 넣는 자리] {esc(m.group(2))} — 사진 설명: {esc(m.group(3))}</p>')
        photos += 1
        continue
    if s == "[지도]":
        out.append(f'<p style="{MARK}">📍 [지도 넣는 자리] 툴바 \'장소\' → "{esc(meta.get("map_name", ""))}" 검색 → 추가 → 이 줄 삭제</p>')
        continue
    if s.startswith("[소제목]"):
        out.append(f'<p style="{H2}"><b>{esc(s[5:].strip())}</b></p>')
        continue
    if s.startswith("[인용구]"):
        quote = True
        out.append(f'<p style="{QT}"><b>💡 {esc(s[5:].strip())}</b></p>')
        continue
    if s.startswith("Q. "):
        out.append(f'<p style="{BODY}"><b>{esc(s)}</b></p>')
        continue
    if s.startswith("─"):
        out.append(f'<p style="{BODY}color:#bbb;">{esc(s)}</p>')
        continue
    if s.startswith("참고 자료"):
        out.append(f'<p style="{BODY}font-size:13px;color:#888;"><b>{esc(s)}</b></p>')
        continue
    style = QT if quote else BODY
    out.append(f'<p style="{style}">{link(esc(s))}</p>')

body = "\n".join(out)
# 참고 자료 블록(제목 줄 다음 ~ 빈 줄 전)은 작은 회색 글씨로
body = re.sub(r'(<p style="[^"]*"><b>참고 자료[^<]*</b></p>\n)((?:<p style="' + re.escape(BODY) + r'">[^\n]*</p>\n)+)',
              lambda m: m.group(1) + m.group(2).replace(BODY, BODY + "font-size:13px;color:#888;"), body)

tags = " ".join("#" + t for t in meta["naver_tags"])
page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>네이버 붙여넣기 — {esc(d.name)}</title>
<style>
body{{margin:0;background:#EEF1F7;font-family:'Malgun Gothic',sans-serif}}
.panel{{position:sticky;top:0;z-index:9;background:#1E2A78;color:#fff;padding:14px 20px;font-size:14px;line-height:1.7}}
.panel b{{color:#FFB199}} .row{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:4px 0}}
.panel button{{background:#FF5A36;color:#fff;border:0;border-radius:6px;padding:8px 14px;font-weight:bold;cursor:pointer;font-size:14px}}
.panel button.sub{{background:#fff;color:#1E2A78}}
.val{{background:rgba(255,255,255,.12);padding:4px 8px;border-radius:4px}}
#ok{{color:#9EF0B5;font-weight:bold}}
#post{{max-width:700px;margin:24px auto;background:#fff;padding:40px 36px;font-family:'Nanum Gothic','Malgun Gothic',sans-serif}}
</style></head><body>
<div class="panel">
<div class="row"><button onclick="copyPost()">① 본문 복사</button><button class="sub" onclick="copyText('t')">제목 복사</button><button class="sub" onclick="copyText('g')">태그 복사</button><span id="ok"></span></div>
<div class="row">제목: <span class="val" id="t">{esc(meta['naver_title'])}</span></div>
<div class="row">태그: <span class="val" id="g">{esc(tags)}</span></div>
<div>네이버 글쓰기 → 제목 칸에 제목 붙여넣기 → 본문 첫 줄 클릭 → <b>Ctrl+V</b> → 노란 줄 자리에 실제 사진 {photos}장·지도 넣고 노란 줄 삭제 → 태그 입력 → 발행</div>
</div>
<div id="post">
{body}
</div>
<script>
function flash(m){{const o=document.getElementById('ok');o.textContent=m;setTimeout(()=>o.textContent='',2500)}}
function copyPost(){{const r=document.createRange();r.selectNodeContents(document.getElementById('post'));const s=getSelection();s.removeAllRanges();s.addRange(r);const ok=document.execCommand('copy');s.removeAllRanges();flash(ok?'본문 복사됨 — 네이버 본문에 Ctrl+V':'복사 실패 — 본문을 드래그해 Ctrl+C')}}
function copyText(id){{navigator.clipboard.writeText(document.getElementById(id).innerText).then(()=>flash('복사됨'),()=>{{const r=document.createRange();r.selectNodeContents(document.getElementById(id));const s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy');s.removeAllRanges();flash('복사됨')}})}}
</script>
</body></html>
"""
(d / "네이버_붙여넣기용.html").write_text(page, encoding="utf-8")
print(f"네이버_붙여넣기용.html: 생성 이미지 {imgs}장 포함 / 실제 사진 자리 {photos} / 지도 자리 1")
