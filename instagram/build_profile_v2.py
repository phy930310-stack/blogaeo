"""프로필 사진 v2 후보 (2026-10-28, frontend-design 적용규칙).

사용: python instagram/build_profile_v2.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets 프로필_v2
파일: instagram/assets/프로필_v2_A.png / _B.png / _C.png (1080×1080). 인스타는 원형으로 잘라 150px 안팎으로 보여 준다.

계획: 원형 안에서 읽히는 요소는 하나뿐이어야 한다 → 로고 원본(색·비율·요소 변경 금지)만 크게, 장식 없음.
  A 네이비 바탕 + 흰 로고           (피드·탐색 탭에서 가장 무난)
  B 종이 바탕(#F4F6FB) + 컬러 로고 + '대전점'  (카드뉴스 v2와 같은 톤)
  C 오렌지 바탕 + 흰 로고 + '대전점'  (작은 원에서 가장 눈에 띔)
원형 크롭을 고려해 로고는 가로 76%, 세로 중앙보다 조금 위에 둔다.
"""
from build_assets import SRC, page

NAVY, ORANGE, PAPER = "#1E2A78", "#FF5A36", "#F4F6FB"

def profile(bg, logo, fg, tag):
    css = f"""
.canvas{{background:{bg};color:{fg}}}
.in{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:48px}}
.in img{{width:{'820px' if not tag else '760px'};height:auto;display:block}}
.tag{{font-size:96px;font-weight:800;letter-spacing:-3px;line-height:1}}
"""
    body = f'<div class="in"><img src="logo/{logo}" alt="SBS아카데미게임학원">{f"<div class=tag>{tag}</div>" if tag else ""}</div>'
    return page(1080, 1080, body, css)

VARIANTS = {
    "A": (NAVY, "SBS아카데미게임학원_White.png", "#fff", ""),
    "B": (PAPER, "SBS아카데미게임학원_Color.png", NAVY, "대전점"),
    "C": (ORANGE, "SBS아카데미게임학원_White.png", "#fff", "대전점"),
}

if __name__ == "__main__":
    for k, v in VARIANTS.items():
        (SRC / f"프로필_v2_{k}.html").write_text(profile(*v), encoding="utf-8")
    print("written", len(VARIANTS))
