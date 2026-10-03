"""원고 폴더의 네이버_본문.txt / 티스토리_본문.html / meta.json 으로 붙여넣기 안내 파일 2개를 만들고 자동 점검한다.
사용: python3 .claude/skills/aeo-blog/scripts/build_guides.py posts/<폴더>

meta.json 예:
{
  "naver_title": "...", "tistory_title": "...",
  "naver_tags": ["게임학과", ...], "tistory_tags": ["게임학과", ...],
  "tistory_category": "게임학과 입시", "map_name": "SBS아카데미게임학원 대전점"
}
본문 표기 규칙
- 생성 이미지:  naver  [이미지: 파일명 / 사진 설명: 문구]
               tistory <p>[이미지 업로드: 파일명 / 대체텍스트: 문구]</p>
- 실제 사진:    [실제 사진 N: 촬영 가이드 / 사진 설명: 문구]   (tistory는 '/ 대체텍스트: 문구')
- 네이버 서식:  [소제목] … / [인용구] … / [지도]
"""
import json, re, sys, os

folder = sys.argv[1]
P = lambda f: os.path.join(folder, f)
meta = json.load(open(P("meta.json"), encoding="utf-8"))
naver = open(P("네이버_본문.txt"), encoding="utf-8").read()
tist = open(P("티스토리_본문.html"), encoding="utf-8").read()
problems = []

# ---------- 공통 점검 ----------
for name, body in (("네이버", naver), ("티스토리", tist)):
    if "※" in body:
        problems.append(f"{name}: 본문에 ※ 사용 (안내문으로 오인되어 삭제될 수 있음)")
    if "가상 사례" in body:
        if not re.search(r"\(가상 사례\)", body):
            problems.append(f"{name}: 가상 사례 소제목에 '(가상 사례)' 없음")
        if "재구성한 가상 사례" not in body:
            problems.append(f"{name}: 가상 사례 고지 문장 없음")
    keys = [k for k in ("자주 묻는 질문", "참고 자료", "042-716-7439") if k != "자주 묻는 질문" or k in body]
    order = [body.find(k) for k in keys]
    if -1 in order or order != sorted(order):
        problems.append(f"{name}: 글 끝 순서(FAQ → 참고 자료 → 연락처) 불일치")
    if "대전광역시 서구 대덕대로 179, 5층 (둔산동, 엠제이굿모닝어학원빌딩 501호)" not in body:
        problems.append(f"{name}: 주소(NAP) 표기가 brand/profile.md와 다름")

# ---------- 티스토리 ----------
if "<blockquote" in tist:
    problems.append("티스토리: <blockquote> 사용 (스킨이 가운데 정렬)")
for t in re.finditer(r"<table", tist):
    before = tist[max(0, t.start() - 200):t.start()]
    if "overflow-x:auto" not in before:
        problems.append("티스토리: 가로 스크롤 래퍼 없는 표 있음")
    cols = len(re.findall(r"<th[ >]", tist[t.start():tist.find("</tr>", t.start())]))
    if cols > 3:
        problems.append(f"티스토리: {cols}열 표 있음 (3열 이하 권장)")
faq = tist.split("자주 묻는 질문</h2>")[1].split("<h2")[0] if "자주 묻는 질문</h2>" in tist else ""
pairs = [(re.sub("<[^>]+>", "", q).strip().removeprefix("Q.").strip(), re.sub("<[^>]+>", "", a).strip())
         for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>", faq, re.S)]
# FAQ 정책: 본문에서 답하지 못한 실제 질문이 있을 때만 2~3개. 없으면 FAQ 섹션·FAQPage 모두 생략
if faq and not (2 <= len(pairs) <= 3):
    problems.append(f"티스토리: FAQ 문항 {len(pairs)}개 (있다면 2~3개)")
if ("자주 묻는 질문" in naver) != bool(pairs):
    problems.append("네이버·티스토리 FAQ 유무가 다름")
ld = {"@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
script = ('<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n</script>") if pairs else ""
t_imgs = re.findall(r"\[이미지 업로드: (\S+) / 대체텍스트: ([^\]]+)\]", tist)
t_real = re.findall(r"\[(실제 사진 \d): ([^/\]]+) / 대체텍스트: ([^\]]+)\]", tist)

def lines(items, fmt):
    return "\n".join(fmt(i, x) for i, x in enumerate(items, 1)) or "   (없음)"

tg = f"""==================================================
티스토리 붙여넣기 안내 (메모장으로 여세요)
==================================================

순서: ⓪ 카테고리 → ① 제목 → ② 본문 → ③ 이미지 → ④ FAQ 코드 → ⑤ 태그 → ⑥ 발행 전 확인 → 발행


⓪ 카테고리 — 발행 설정 창에서 선택 (없으면 블로그 관리 → 카테고리 관리에서 먼저 생성)
--------------------------------------------------
{meta.get('tistory_category', '게임학과 입시')}


① 제목 — 제목 칸에 붙여넣기
--------------------------------------------------
{meta['tistory_title']}


② 본문
--------------------------------------------------
글쓰기 → 우측 상단 '기본모드' → 'HTML' → 티스토리_본문.html 을 메모장으로 열어(오른쪽 클릭 → 연결 프로그램 → 메모장) 전체 복사(Ctrl+A, Ctrl+C) → 붙여넣기


③ 이미지 — 기본모드로 바꾼 뒤 [이미지 업로드: …] / [실제 사진 …] 자리에 업로드 → 이미지 클릭 → 대체텍스트 입력 → 안내 줄 삭제
--------------------------------------------------
[생성 이미지]
{lines(t_imgs, lambda i, x: f"   {i}) {x[0]}{chr(10)}      → 대체텍스트: {x[1]}")}

[실제 사진 — 직접 촬영]
{lines(t_real, lambda i, x: f"   {x[0]}: {x[1].strip()}{chr(10)}      → 대체텍스트: {x[2]}")}


④ FAQ 코드 — 맨 마지막 작업! HTML 모드 → 코드 창 맨 아래(Ctrl+End)에 붙여넣기 → 이후 모드 전환 없이 바로 발행
--------------------------------------------------
{script or "(이 글은 FAQ가 없어 생략합니다)"}


⑤ 태그 — 태그 칸에 붙여넣기 (한 덩어리로 들어가면 하나씩 입력)
--------------------------------------------------
{', '.join(meta['tistory_tags'])}


⑥ 발행 전 확인 — 아래는 '지우면 안 되는 본문'입니다
--------------------------------------------------
[ ] 소제목 끝 "(가상 사례)" 와 박스 첫 줄 고지 문장이 남아 있다
[ ] "참고 자료" 목록이 연락처 위에 남아 있다
[ ] [이미지 업로드: …] / [실제 사진 …] 안내 줄이 남아 있지 않다
[ ] 카테고리를 선택했다


발행 후 확인: 글 열기 → Ctrl+U → Ctrl+F 로 FAQPage 검색 → 찾아지면 성공
              (또는 발행 주소를 Claude에게 주면 자동 점검)
"""

# ---------- 네이버 ----------
if "<" in re.sub(r"<!--.*?-->", "", naver, flags=re.S) and re.search(r"<(table|div|p|h\d)", naver):
    problems.append("네이버: HTML 태그가 본문에 있음")
if "|" in naver and re.search(r"^\|.*\|$", naver, re.M):
    problems.append("네이버: 표(| |) 사용 — 목록이나 이미지로 대체")
n_imgs = re.findall(r"\[이미지: (\S+) / 사진 설명: ([^\]]+)\]", naver)
n_real = re.findall(r"\[(실제 사진 \d): ([^/\]]+) / 사진 설명: ([^\]]+)\]", naver)
if "[지도]" not in naver:
    problems.append("네이버: [지도] 표시 없음")

ng = f"""==================================================
네이버 붙여넣기 안내 (메모장으로 여세요)
==================================================

순서: ① 제목 → ② 본문 → ③ 서식 → ④ 사진 → ⑤ 지도 → ⑥ 태그 → ⑦ 발행 전 확인


① 제목 — 제목 칸에 붙여넣기
--------------------------------------------------
{meta['naver_title']}


② 본문
--------------------------------------------------
네이버_본문.txt 를 메모장으로 열어 전체 복사(Ctrl+A → Ctrl+C) → 본문에 붙여넣기


③ 서식 적용 (가독성에 가장 큰 영향)
--------------------------------------------------
- 본문 전체 선택 → 글자 크기 15
- [소제목] 으로 시작하는 줄 → 툴바 '소제목' 서식 → "[소제목] " 글자 삭제
  (소제목 서식이 없으면: 굵게 + 글자 크기 19)
- [인용구] 로 시작하는 요약 부분 → 툴바 '인용구' → '라인' 스타일 → 왼쪽 정렬 → "[인용구] " 글자 삭제


④ 사진 — 안내 줄 자리에 올리고, 사진 아래 '사진 설명' 칸에 입력 → 안내 줄 삭제
--------------------------------------------------
[생성 이미지]
{lines(n_imgs, lambda i, x: f"   {i}) {x[0]}{chr(10)}      → 사진 설명: {x[1]}")}

[실제 사진 — 직접 촬영]
{lines(n_real, lambda i, x: f"   {x[0]}: {x[1].strip()}{chr(10)}      → 사진 설명: {x[2]}")}

   촬영 공통: 가로 4:3 / 밝게 / 얼굴·이름·모니터 속 개인정보가 보이지 않게 / 글자 합성·스톡 사진 금지
             네이버와 티스토리에는 같은 사진 말고 다른 컷 사용


⑤ 지도
--------------------------------------------------
맨 아래 [지도] 줄 자리 → 툴바 '장소' → "{meta.get('map_name', 'SBS아카데미게임학원 대전점')}" 검색 → 추가 → [지도] 줄 삭제


⑥ 태그 — 태그 칸에 붙여넣기 (한 덩어리로 들어가면 하나씩 입력)
--------------------------------------------------
{' '.join('#' + t for t in meta['naver_tags'])}


⑦ 발행 전 확인 — 아래는 '지우면 안 되는 본문'입니다
--------------------------------------------------
[ ] 소제목 "… (가상 사례)" 와 바로 아래 고지 문장이 남아 있다
[ ] "참고 자료" 목록이 연락처 위에 남아 있다
[ ] 연락처 아래에 지도가 들어갔다
[ ] 본문에 "[" 로 시작하는 안내 표시가 남아 있지 않다 (Ctrl+F 로 "[" 검색)
"""

# ---------- 플랫폼 차별화 점검 (네이버가 티스토리도 수집하므로 유사문서 위험 관리) ----------
import difflib
def _clean(x):
    x = re.sub(r"<script.*?</script>", "", x, flags=re.S); x = re.sub(r"<[^>]+>", "\n", x)
    x = re.sub(r"&[a-z]+;", " ", x); return re.sub(r"\[[^\]]*\]", "", x)
def _sents(x):
    return [y for y in (re.sub(r"\s+", " ", z).strip(" ·①②③④-—") for z in re.split(r"(?<=[.?!요다])\s+|\n", x)) if len(y) >= 15]
# 참고 자료·연락처(고정 문구)와 가상 사례 고지 문장은 두 플랫폼이 같아야 하므로 비교에서 제외
_cut = lambda x: x.split("참고 자료")[0].replace("재구성한 가상 사례", "")
_n, _t = _cut(_clean(naver)), _cut(_clean(tist))
_ns, _ts = _sents(_n), _sents(_t)
# 사실·수치 문장은 표현만 바꿔도 비슷할 수밖에 없으므로, 85% 이상 비슷한 문장 수와 5글자 조각 겹침률로 판단
_near = [a for a in _ns if any(difflib.SequenceMatcher(None, a, b).ratio() >= 0.85 for b in _ts)]
_g = lambda x: {re.sub(r"\s", "", x)[i:i + 5] for i in range(len(re.sub(r"\s", "", x)) - 5)}
_jac = len(_g(_n) & _g(_t)) / max(1, len(_g(_n) | _g(_t)))
print(f"플랫폼 차별화: 거의 같은 문장 {len(_near)}개 / 5글자 조각 겹침률 {_jac:.0%} (기준: 5개 이하, 20% 이하)")
if len(_near) > 5 or _jac > 0.20:
    problems.append(f"네이버·티스토리 문장이 너무 비슷함 (거의 같은 문장 {len(_near)}개, 겹침률 {_jac:.0%}) — 어미만 바꾸지 말고 문장 구조·예시를 다시 쓸 것")
    for a in _near[:8]:
        problems.append(f"  ≈ {a[:60]}")

open(P("티스토리_붙여넣기안내.txt"), "w", encoding="utf-8").write(tg)
# 업로더(tools/tistory-uploader)가 본문 끝에 붙일 FAQ 코드
if script:
    open(P("티스토리_FAQ코드.html"), "w", encoding="utf-8").write(script + "\n")
elif os.path.exists(P("티스토리_FAQ코드.html")):
    os.remove(P("티스토리_FAQ코드.html"))
open(P("네이버_붙여넣기안내.txt"), "w", encoding="utf-8").write(ng)
print(f"FAQ {len(pairs)}문항 / 티스토리 이미지 {len(t_imgs)}+실제 {len(t_real)} / 네이버 이미지 {len(n_imgs)}+실제 {len(n_real)}")
print("점검: 이상 없음" if not problems else "점검 결과:\n- " + "\n- ".join(problems))
sys.exit(1 if problems else 0)
