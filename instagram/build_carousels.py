"""인스타그램 카드뉴스 본문 장(2장~마지막 장)을 만든다. 1장(표지)은 build_assets.py.

사용: python3 instagram/build_carousels.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets
- 수치·사실은 원본 블로그 글(출처 표기된 것)에서만 가져온다. 근거는 instagram/README.md 표 참고
- 입시 글은 포트폴리오&면접 전형 중심으로 맺는다(brand/profile.md 입시 포지셔닝)
- 디자인 원칙: .claude/skills/frontend-design/적용규칙.md (2026-10-28 추가 — 현재 결과물은 적용 전)
"""
from build_assets import SRC, THEMES, page

FORM = "프로필 링크 → 상담 신청"


def slide(theme, n, total, chip, heading, body):
    t = THEMES[theme]
    light = theme == "light"
    box_bg = "#fff" if light else "rgba(255,255,255,.08)"
    box_bd = "rgba(30,42,120,.10)" if light else "rgba(255,255,255,.16)"
    box_sh = "0 16px 36px rgba(30,42,120,.10)" if light else "none"
    muted = "#5a63a0" if light else "rgba(255,255,255,.72)"
    css = f"""
.canvas{{background:{t['bg']};color:{t['fg']}}}
.in{{position:absolute;left:100px;right:100px;top:110px;bottom:120px;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;justify-content:space-between}}
.chip{{padding:12px 26px;border-radius:999px;background:{t['chip_bg']};color:{t['chip_fg']};font-size:32px;font-weight:700}}
.pg{{font-size:32px;font-weight:700;color:{muted}}}
h2{{margin-top:44px;font-size:76px;line-height:1.2;font-weight:800;letter-spacing:-2.5px}}
h2 b{{color:{t['hi']}}}
.lead{{margin-top:22px;font-size:36px;line-height:1.5;color:{muted};font-weight:600}}
.body{{margin-top:46px;display:flex;flex-direction:column;gap:22px}}
.box{{background:{box_bg};border:2px solid {box_bd};box-shadow:{box_sh};border-radius:28px;padding:28px 34px}}
.box.hot{{border-color:{t['hi']};border-width:4px}}
.box h3{{font-size:42px;font-weight:800;letter-spacing:-1px}}
.box h3 em{{font-style:normal;color:{t['hi']}}}
.box p{{margin-top:10px;font-size:33px;line-height:1.5;color:{muted};font-weight:600}}
.row{{display:flex;gap:22px}}.row .box{{flex:1}}
.num{{display:inline-flex;width:58px;height:58px;border-radius:18px;background:{t['hi']};color:#fff;align-items:center;justify-content:center;font-size:34px;font-weight:800;margin-right:18px;vertical-align:middle}}
.src{{margin-top:auto;font-size:26px;line-height:1.5;color:{muted};font-weight:400}}
.foot{{position:absolute;left:100px;right:100px;bottom:56px;display:flex;align-items:center;justify-content:space-between}}
.foot img{{height:34px}}.foot span{{font-size:28px;font-weight:700;color:{muted}}}
"""
    body_html = f"""<div class="in"><div class="top"><span class="chip">{chip}</span><span class="pg">{n} / {total}</span></div>
{heading}{body}</div>
<div class="foot"><img src="logo/{t['logo']}" alt="SBS아카데미게임학원"><span>{'저장해 두고 다시 보세요 🔖' if n < total else '@sbs_game_daejeon'}</span></div>"""
    return page(1080, 1350, body_html, css)


def cta(theme, n, total, chip, title, lines, note):
    body = f"""<h2>{title}</h2><div class="body">
<div class="box hot"><h3>📝 {FORM}</h3><p>1~2분이면 끝나요. 남겨 주신 방법으로 상담팀이 연락드려요.</p></div>
<div class="box"><h3>📞 042-716-7439</h3><p>운영시간 09:00~22:00 · 카톡 1:1 상담도 프로필 링크에</p></div>
<div class="box"><h3>📍 대전 둔산동</h3><p>대전광역시 서구 대덕대로 179, 5층<br>(둔산동, 엠제이굿모닝어학원빌딩 501호)</p></div>
</div><p class="src">{note}</p>"""
    return slide(theme, n, total, chip, "", body)


# ── 02 성적이 낮아도 게임학과 (원본: posts/2026-10-01_게임학과-내신-5등급, 2027학년도 기준) ──
C02 = [
    ("입시", "<h2>결론부터 말하면,<br><b>포기할 필요 없어요</b></h2><p class='lead'>게임학과에는 내신보다 포트폴리오와 면접을<br>더 크게 보는 전형이 있어요.</p>",
     "<div class='body'><div class='box'><h3>먼저 확인할 것 1</h3><p>내 5등급이 <b>어느 등급제</b>의 5등급인지</p></div>"
     "<div class='box'><h3>먼저 확인할 것 2</h3><p>가고 싶은 대학이 <b>어떤 전형</b>으로 뽑는지</p></div></div>"),
    ("입시", "<h2>같은 5등급,<br><b>다른 위치</b>예요</h2><p class='lead'>현 고3은 9등급제, 현 고1·고2는 5등급제</p>",
     "<div class='body'><div class='row'><div class='box'><h3>9등급제 5등급</h3><p>현 고3 (2027 대입)<br>누적 상위 40~60%<br><b>중간 구간</b></p></div>"
     "<div class='box hot'><h3>5등급제 5등급</h3><p>현 고1·고2 (2028 대입~)<br>누적 상위 90~100%<br><b>가장 아래 구간</b></p></div></div>"
     "<div class='box'><p>'5등급 합격 후기'를 볼 때는 어느 등급제 이야기인지 꼭 확인하세요.</p></div></div>"),
    ("입시", "<h2>게임학과 전형,<br><b>4가지</b>로 나뉘어요</h2>",
     "<div class='body'><div class='box'><h3>학생부교과</h3><p>내신이 핵심</p></div>"
     "<div class='box'><h3>학생부종합</h3><p>성적 + 활동 + 면접을 함께</p></div>"
     "<div class='box'><h3>실기위주</h3><p>시험장에서 보는 실기가 당락을 좌우</p></div>"
     "<div class='box hot'><h3><em>포트폴리오·면접</em></h3><p>준비해 온 작품과 면접으로 평가</p></div></div>"),
    ("입시", "<h2>포트폴리오·면접 전형,<br><b>이렇게 뽑아요</b></h2><p class='lead'>예) 청강문화산업대 게임콘텐츠스쿨 면접전형</p>",
     "<div class='body'><div class='box'><h3><span class='num'>1</span>서류로 2배수 선발</h3></div>"
     "<div class='box'><h3><span class='num'>2</span>심층면접</h3></div>"
     "<div class='box hot'><h3>모집 인원 88명</h3><p>2027학년도 기준</p></div></div>"
     "<p class='src'>출처: ZDNet Korea 청강문화산업대 게임콘텐츠스쿨 기사(2026.09.09)<br>전형은 해마다 바뀌어요. 지원 전 대학 모집요강을 확인하세요.</p>"),
    ("입시", "<h2>지금(10월),<br><b>학년별로 할 일</b></h2>",
     "<div class='body'><div class='box hot'><h3>고2</h3><p>2028 모집요강 확인 · 포트폴리오 첫 작품 시작<br>→ 겨울방학에 작품 집중</p></div>"
     "<div class='box'><h3>고1</h3><p>내신 관리 + 게임 관련 진로 활동을 학생부에<br>→ 2학년 전에 전공 방향 정하기</p></div>"
     "<div class='box'><h3>고3</h3><p>지원한 대학 면접 준비 마무리<br>정시 일정은 대학별로 꼭 확인</p></div></div>"),
]

# ── 03 국비로 배우는 게임·웹툰 (원본: posts/2026-10-19_대전-국비지원-교육, 고용24 기준) ──
C03 = [
    ("취업·국비", "<h2>국민내일배움카드,<br><b>한눈에</b></h2><p class='lead'>정부가 직업훈련 비용을 지원하는 제도예요.</p>",
     "<div class='body'><div class='box hot'><h3>지원 한도 5년간 300만원</h3><p>요건 충족 시 최대 500만원</p></div>"
     "<div class='box'><h3>자부담 0~55%</h3><p>과정 유형 등에 따라 달라요</p></div>"
     "<div class='box'><h3>유효기간 5년</h3><p>남은 한도는 기간이 지나면 사라져요</p></div></div>"
     "<p class='src'>출처: 고용24 「국민내일배움카드」 제도 안내 (2026.10.19 확인)</p>"),
    ("취업·국비", "<h2>신청은<br><b>5단계</b>예요</h2>",
     "<div class='body'><div class='box'><h3><span class='num'>1</span>고용24 가입</h3></div>"
     "<div class='box'><h3><span class='num'>2</span>내일배움카드 신청</h3></div>"
     "<div class='box'><h3><span class='num'>3</span>과정 검색</h3><p>지역 '대전' + 게임·웹툰·유니티</p></div>"
     "<div class='box'><h3><span class='num'>4</span>훈련기관 상담·입과 절차</h3></div>"
     "<div class='box'><h3><span class='num'>5</span>수강 신청·결제</h3></div></div>"),
    ("취업·국비", "<h2>'국가기간·전략산업<br>직종훈련'은 <b>뭐가 달라요?</b></h2>",
     "<div class='body'><div class='box'><h3>정부가 지정한 훈련</h3><p>기간산업이나 인력이 부족한 전략산업 분야 인재를 기르기 위한 과정이에요.</p></div>"
     "<div class='box hot'><h3>같은 카드로 수강</h3><p>다만 지원 조건과 자부담이 일반 과정과 다를 수 있어요.</p></div>"
     "<div class='box'><h3>정확한 금액은?</h3><p>고용24에서 과정명을 검색해 상세 페이지로 확인하세요.</p></div></div>"),
    ("취업·국비", "<h2>대전점 고용24<br><b>등록 과정 3개</b></h2>",
     "<div class='body'><div class='box'><h3>게임그래픽</h3><p>국민내일배움카드 과정</p></div>"
     "<div class='box hot'><h3>게임프로그래밍(유니티)</h3><p>국가기간·전략산업직종훈련</p></div>"
     "<div class='box'><h3>웹툰</h3><p>국민내일배움카드 과정</p></div>"
     "<div class='box'><p>입과 전에 상담과 간단한 실기로<br>기초를 확인해요.</p></div></div>"),
    ("취업·국비", "<h2>자주 묻는 <b>질문</b></h2>",
     "<div class='body'><div class='box'><h3>Q. 한도를 현금으로 받나요?</h3><p>아니에요. 고용24 등록 과정의 훈련비를 결제할 때 쓰는 금액이에요.</p></div>"
     "<div class='box'><h3>Q. 대학생·직장인도 되나요?</h3><p>대부분 발급받을 수 있어요. 재학 여부나 소득 등에 따라 조건이 다를 수 있으니 고용24에서 확인하세요.</p></div></div>"
     "<p class='src'>지원 한도·자부담·신청 절차는 바뀔 수 있어요. 고용24에서 최신 내용을 확인하세요.</p>"),
]

SETS = {
    "02": ("navy", C02, ("입시", "<b>우리 학교·학년</b>이면<br>어떤 전형일까?", "모집요강을 같이 펼쳐 놓고 전형별 준비 순서를 정리해 드려요.")),
    "03": ("light", C03, ("취업·국비", "국비 과정,<br><b>대상인지</b> 궁금하다면", "과정별 대상 여부와 입과 절차를 안내해 드려요.")),
}

if __name__ == "__main__":
    count = 0
    for key, (theme, slides, (chip, title, note)) in SETS.items():
        total = len(slides) + 2  # 표지 + 본문 + 마지막(상담)
        for i, (c, heading, body) in enumerate(slides, start=2):
            (SRC / f"캐러셀_{key}_{i:02d}.html").write_text(slide(theme, i, total, c, heading, body), encoding="utf-8")
            count += 1
        (SRC / f"캐러셀_{key}_{total:02d}.html").write_text(cta(theme, total, total, chip, title, [], note), encoding="utf-8")
        count += 1
    print("written", count, "slides")
