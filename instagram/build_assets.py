"""인스타그램 개설용 이미지 원본(HTML)을 만든다.

사용: python3 instagram/build_assets.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets
- 프로필 사진(1080×1080), 하이라이트 커버 5개(1080×1080), 첫 게시물 표지 9개(1080×1350, 4:5)
- 게시물 표지는 프로필 격자(3:4)에서 좌우 34px가 잘리므로 글자는 안쪽 80px 안에 둔다
- 로고는 사업부 공유폴더 원본(무단 수정 금지) — 색·비율을 바꾸지 않는다
"""
from pathlib import Path

SRC = Path(__file__).parent / "assets" / "src"
SRC.mkdir(parents=True, exist_ok=True)
FONT = "../../../.claude/skills/aeo-blog/assets/fonts"

BASE_CSS = f"""
@font-face{{font-family:P;src:url({FONT}/Pretendard-Regular.otf);font-weight:400}}
@font-face{{font-family:P;src:url({FONT}/Pretendard-SemiBold.otf);font-weight:600}}
@font-face{{font-family:P;src:url({FONT}/Pretendard-Bold.otf);font-weight:700}}
@font-face{{font-family:P;src:url({FONT}/Pretendard-ExtraBold.otf);font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#fff}}
.canvas{{position:relative;overflow:hidden;font-family:P;word-break:keep-all}}
"""

THEMES = {
    "navy": dict(bg="radial-gradient(900px 700px at 85% 10%,#2f3fa6 0%,rgba(47,63,166,0) 70%),linear-gradient(160deg,#141c58 0%,#1E2A78 60%,#24318c 100%)",
                 fg="#fff", sub="rgba(255,255,255,.8)", chip_bg="#FF5A36", chip_fg="#fff", hi="#FF5A36",
                 grid="rgba(255,255,255,.06)", logo="SBS아카데미게임학원_White.png", foot="rgba(255,255,255,.75)"),
    "light": dict(bg="radial-gradient(800px 600px at 90% 5%,rgba(255,90,54,.14),rgba(255,90,54,0) 70%),linear-gradient(160deg,#F4F6FB 0%,#E7EBF7 100%)",
                  fg="#1E2A78", sub="#4a5490", chip_bg="#1E2A78", chip_fg="#fff", hi="#FF5A36",
                  grid="rgba(30,42,120,.07)", logo="SBS아카데미게임학원_Color.png", foot="#5a63a0"),
    "orange": dict(bg="radial-gradient(800px 700px at 85% 0%,#ff8a6b 0%,rgba(255,138,107,0) 70%),linear-gradient(160deg,#FF5A36 0%,#f0471f 100%)",
                   fg="#fff", sub="rgba(255,255,255,.9)", chip_bg="#1E2A78", chip_fg="#fff", hi="#1E2A78",
                   grid="rgba(255,255,255,.09)", logo="SBS아카데미게임학원_White.png", foot="rgba(255,255,255,.85)"),
}

# 첫 게시물 9개 — 화면 격자 순서(왼쪽 위부터). 1~3은 고정 게시물
POSTS = [
    ("01_상담안내", "orange", "상담 안내", "입시·취업 상담,<br><b>1~2분</b>이면<br>신청돼요", "게임 · 웹툰 · 웹소설 · AI개발 · 애니메이션<br>프로필 링크에서 바로 신청하세요", "상담신청"),
    ("02_포폴면접전형", "navy", "입시", "성적이 낮아도<br><b>게임학과</b><br>갈 수 있을까?", "포트폴리오&amp;면접 전형으로<br>준비하는 방법", "입시"),
    ("03_국비과정", "light", "취업·국비", "<b>국비</b>로 배우는<br>게임·웹툰 과정", "내일배움카드 신청 5단계<br>게임·웹툰 과정 찾는 법", "취업국비"),
    ("04_게임학과종류", "navy", "입시", "게임학과,<br>다 같은 과가<br><b>아니에요</b>", "공학 · 미술 · 콘텐츠<br>3갈래 차이와 고르는 순서", "과정"),
    ("05_청강대게임과", "navy", "입시", "청강대 게임과<br><b>면접전형</b><br>준비 순서", "2027학년도 기준<br>분야별 포트폴리오 정리", "말풍선"),
    ("06_게임회사신입", "light", "취업", "게임회사 신입,<br><b>뭘 준비</b>할까?", "직군 5가지와<br>직군별 포트폴리오", "모니터"),
    ("07_게임원화가", "navy", "진로", "<b>게임원화가</b><br>되는 법", "캐릭터·배경 원화 차이<br>연습 순서 5단계", "펜"),
    ("08_3D모델링", "navy", "진로", "게임 3D 모델링,<br><b>툴 3개</b>로<br>시작해요", "3ds Max · 지브러쉬<br>서브스턴스 페인터", "큐브"),
    ("09_유니티입문", "light", "취업", "<b>유니티</b> 입문,<br>어디서부터?", "무료 조건 · 시작 5단계<br>필요한 C# 수준", "코드"),
]


def page(w, h, body, css=""):
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{BASE_CSS}{css}</style></head>
<body><div class="canvas" style="width:{w}px;height:{h}px">{body}</div></body></html>"""


def cover(theme, chip, title, sub, icon):
    t = THEMES[theme]
    css = f"""
.canvas{{background:{t['bg']};color:{t['fg']}}}
.grid{{position:absolute;inset:0;background-image:linear-gradient({t['grid']} 2px,transparent 2px),linear-gradient(90deg,{t['grid']} 2px,transparent 2px);
  background-size:60px 60px;mask-image:linear-gradient(200deg,#000 0%,transparent 60%)}}
.in{{position:absolute;left:110px;right:110px;top:150px;bottom:150px;display:flex;flex-direction:column}}
.chip{{align-self:flex-start;padding:16px 32px;border-radius:999px;background:{t['chip_bg']};color:{t['chip_fg']};font-size:40px;font-weight:700}}
h1{{margin-top:56px;font-size:112px;line-height:1.16;font-weight:800;letter-spacing:-4px}}
h1 b{{color:{t['hi']};font-weight:800}}
.sub{{margin-top:44px;font-size:44px;line-height:1.5;color:{t['sub']};font-weight:600;letter-spacing:-1px}}
.foot{{margin-top:auto;display:flex;align-items:center;justify-content:space-between}}
.foot img{{height:44px;width:auto;display:block}}
.foot span{{font-size:34px;font-weight:700;color:{t['foot']}}}
.big{{position:absolute;right:100px;bottom:220px;opacity:.95}}
.bar{{position:absolute;left:110px;top:110px;width:90px;height:10px;border-radius:5px;background:{t['hi']}}}
"""
    stroke = "#1E2A78" if theme == "light" else "#fff"
    big = f'<svg class="big" width="320" height="320" viewBox="0 0 180 180" fill="none" stroke="{stroke}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round">{ICONS[icon]}</svg>'
    if theme == "orange":
        big = big.replace("#FF5A36", "#1E2A78")
    body = f"""<div class="grid"></div><i class="bar"></i>{big}<div class="in">
<div class="chip">{chip}</div><h1>{title}</h1><p class="sub">{sub}</p>
<div class="foot"><img src="logo/{t['logo']}" alt="SBS아카데미게임학원"><span>대전점 →</span></div></div>"""
    return page(1080, 1350, body, css)


ICONS = {
    "입시": '<path d="M90 30L10 66l80 36 80-36z"/><path d="M40 80v34c15 15 33 21 50 21s35-6 50-21V80"/><path d="M160 72v40"/><circle cx="160" cy="122" r="7" fill="#FF5A36" stroke="#FF5A36"/>',
    "취업국비": '<rect x="18" y="52" width="144" height="98" rx="14"/><path d="M64 52V36a10 10 0 0110-10h32a10 10 0 0110 10v16"/><path d="M18 92h144"/><rect x="78" y="82" width="24" height="20" rx="4" fill="#FF5A36" stroke="#FF5A36"/>',
    "과정": '<path d="M48 40h84c20 0 33 14 37 33l6 37c3 20-17 31-31 17l-14-14H51l-14 14C23 141 3 130 6 110l6-37C16 54 29 40 48 40z"/><path d="M40 82h30M55 67v30" stroke="#FF5A36"/><circle cx="122" cy="72" r="6" fill="#fff"/><circle cx="138" cy="88" r="6" fill="#fff"/><circle cx="106" cy="88" r="6" fill="#fff"/><circle cx="122" cy="104" r="6" fill="#fff"/>',
    "상담신청": '<rect x="34" y="18" width="112" height="144" rx="14"/><path d="M60 58h60M60 88h60M60 118h34"/><path d="M118 132l10 10 22-26" stroke="#FF5A36"/>',
    "펜": '<path d="M124 24l32 32-80 80-42 10 10-42z"/><path d="M108 40l32 32"/><path d="M28 160c22-6 32 10 54 0" stroke="#FF5A36"/>',
    "큐브": '<path d="M90 14l66 36v80l-66 36-66-36V50z"/><path d="M24 50l66 36 66-36M90 86v80"/><circle cx="90" cy="86" r="8" fill="#FF5A36" stroke="#FF5A36"/>',
    "코드": '<path d="M56 48L18 90l38 42M124 48l38 42-38 42"/><path d="M104 36L76 144" stroke="#FF5A36"/>',
    "말풍선": '<path d="M20 30h96a12 12 0 0112 12v48a12 12 0 01-12 12H62l-28 22v-22H20a12 12 0 01-12-12V42a12 12 0 0112-12z"/><path d="M144 66h16a12 12 0 0112 12v40a12 12 0 01-12 12h-6v20l-22-20h-34" stroke="#FF5A36"/>',
    "모니터": '<rect x="14" y="22" width="152" height="104" rx="12"/><path d="M62 158h56M90 126v32"/><path d="M60 62l-18 14 18 14M120 62l18 14-18 14" stroke="#FF5A36"/>',
    "오시는길": '<path d="M90 166s-56-56-56-96a56 56 0 01112 0c0 40-56 96-56 96z"/><circle cx="90" cy="70" r="20" stroke="#FF5A36"/>',
}


HIGHLIGHTS = ["입시", "취업국비", "과정", "상담신청", "오시는길"]


def highlight(icon):
    css = """
.canvas{background:radial-gradient(600px 600px at 70% 20%,#2f3fa6 0%,rgba(47,63,166,0) 70%),#1E2A78}
.ic{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
"""
    body = f"""<div class="ic"><svg width="440" height="440" viewBox="0 0 180 180" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">{ICONS[icon]}</svg></div>"""
    return page(1080, 1080, body, css)


def profile():
    css = """
.canvas{background:radial-gradient(700px 600px at 80% 10%,#2f3fa6 0%,rgba(47,63,166,0) 70%),linear-gradient(160deg,#141c58 0%,#1E2A78 70%);color:#fff}
.in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:56px}
.in img{width:820px;height:auto;display:block}
.dj{display:flex;align-items:center;gap:26px;font-size:150px;font-weight:800;letter-spacing:-4px}
.dj i{width:34px;height:34px;border-radius:50%;background:#FF5A36;box-shadow:0 0 40px #FF5A36}
"""
    body = """<div class="in"><img src="logo/SBS아카데미게임학원_White.png" alt="SBS아카데미게임학원"><div class="dj"><i></i>대전점</div></div>"""
    return page(1080, 1080, body, css)


if __name__ == "__main__":
    (SRC / "프로필.html").write_text(profile(), encoding="utf-8")
    for name in HIGHLIGHTS:
        (SRC / f"하이라이트_{name}.html").write_text(highlight(name), encoding="utf-8")
    for fname, theme, chip, title, sub, icon in POSTS:
        (SRC / f"게시물_{fname}.html").write_text(cover(theme, chip, title, sub, icon), encoding="utf-8")
    print("written", len(list(SRC.glob("*.html"))), "html files")
