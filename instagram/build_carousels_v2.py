"""카드뉴스 v2 — .claude/skills/frontend-design/적용규칙.md 를 적용한 버전 (2026-10-28).

사용: python3 instagram/build_carousels_v2.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets
파일: instagram/assets/v2_02_01.png ~ v2_02_07.png, v2_03_01.png ~ v2_03_07.png (표지 포함 각 7장)
       특정 묶음만 렌더링: node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets v2_03_

디자인 계획(02 성적이 낮아도 게임학과):
- 바탕 종이(#F4F6FB) + 네이비 잉크. 오렌지는 장마다 한 곳.
- 기억 요소 = 거대한 숫자 '5'와 등급 위치 눈금. 카드 상자 없음. 번호는 실제 순서(서류→면접)에만.
- 수치·사실은 posts/2026-10-01_게임학과-내신-5등급 (ZDNet 2026.09.09 등) 에서만.

디자인 계획(03 국비로 배우는 게임·웹툰, 2026-10-28 로컬 세션):
- 같은 종이 바탕·네이비 잉크. 02와 짝을 이루도록 표지의 기억 요소 = 거대한 숫자 '300만원'(5년 한도).
- 상자 없음. 번호는 실제 순서(신청 5단계)에만. 오렌지는 장마다 한 곳(가장 중요한 한 줄).
- 수치·사실은 posts/2026-10-19_대전-국비지원-교육 (고용24 국민내일배움카드 제도 안내, 2026.10.19 확인)과
  brand/profile.md(대전점 고용24 등록 과정 3개, 입과 전 상담+간단한 실기)에서만. 훈련비·자부담 금액은 쓰지 않는다.
"""
from build_assets import SRC, page

NAVY, ORANGE, PAPER, MIST = "#1E2A78", "#FF5A36", "#F4F6FB", "#7A82B4"

CSS = f"""
.canvas{{background:{PAPER};color:{NAVY}}}
.in{{position:absolute;left:96px;right:96px;top:96px;bottom:96px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:baseline;font-size:30px;font-weight:600;color:{MIST}}}
.top b{{color:{NAVY};font-weight:700}}
.foot{{margin-top:auto;display:flex;align-items:center;justify-content:space-between}}
.foot img{{height:34px;display:block}}
.foot span{{font-size:28px;color:{MIST};font-weight:600}}
.lead{{font-size:40px;line-height:1.45;font-weight:600;letter-spacing:-.8px}}
.body{{font-size:36px;line-height:1.5;font-weight:500;letter-spacing:-.6px;color:{NAVY}}}
.body p+p{{margin-top:22px}}
.small{{font-size:27px;line-height:1.5;color:{MIST};font-weight:500}}
h1{{font-weight:800;letter-spacing:-3px;line-height:1.08}}
.mark{{color:{ORANGE}}}
"""


def frame(n, body, chip="입시", series="성적이 낮아도 게임학과", total=7):
    top = f'<div class="top"><span><b>{chip}</b>&nbsp; {series}</span><span>{n}/{total}</span></div>' if n > 1 else ""
    foot = f'<div class="foot"><img src="logo/SBS아카데미게임학원_Color.png" alt="SBS아카데미게임학원"><span>{"대전점" if n < total else "@sbs_game_daejeon"}</span></div>'
    return page(1080, 1350, f'<div class="in">{top}{body}{foot}</div>', CSS)


# 1 표지 — 거대한 5 하나가 전부
S1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">내신</div>
<div style="font-size:620px;line-height:.86;font-weight:800;letter-spacing:-30px;margin-left:-18px;color:{NAVY}">5<span style="font-size:150px;letter-spacing:-4px;margin-left:10px;vertical-align:baseline">등급</span></div>
<h1 style="margin-top:56px;font-size:84px">게임학과,<br>갈 수 있을까요?</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">포트폴리오와 면접으로 가는 길을<br>7장으로 정리했어요.</p>
"""

# 2 결론
S2 = f"""
<h1 style="margin-top:60px;font-size:112px">포기할<br>필요 없어요.</h1>
<p class="lead" style="margin-top:48px">게임학과에는 내신보다 <u style="text-decoration-color:{ORANGE};text-decoration-thickness:8px;text-underline-offset:12px">포트폴리오와 면접</u>을<br>더 크게 보는 전형이 있어요.</p>
<div class="body" style="margin-top:72px">
<p>먼저 확인할 것은 두 가지예요.</p>
<p>내 5등급이 <b>어느 등급제</b>의 5등급인지,<br>가고 싶은 대학이 <b>어떤 전형</b>으로 뽑는지.</p>
</div>
"""

# 3 같은 5등급, 다른 위치 — 눈금 막대 (정보 구조)
def scale(label, lo, hi, note, hot):
    col = ORANGE if hot else NAVY
    return f"""
<div style="margin-top:54px">
<div style="display:flex;justify-content:space-between;align-items:baseline"><span class="body" style="font-weight:700">{label}</span><span class="small">{note}</span></div>
<div style="position:relative;height:44px;margin-top:18px;background:#fff;border:3px solid {NAVY};border-radius:4px">
  <div style="position:absolute;top:0;bottom:0;left:{lo}%;width:{hi-lo}%;background:{col}"></div>
  <div style="position:absolute;top:-34px;left:{(lo+hi)/2}%;transform:translateX(-50%);font-size:30px;font-weight:800;color:{col}">5</div>
</div>
<div class="small" style="display:flex;justify-content:space-between;margin-top:10px"><span>상위 0%</span><span>100%</span></div>
</div>"""

S3 = f"""
<h1 style="margin-top:48px;font-size:88px">같은 5등급,<br>다른 위치예요.</h1>
{scale("9등급제 — 지금 고3", 40, 60, "2027 대입", False)}
{scale("5등급제 — 지금 고1·고2", 90, 100, "2028 대입부터", True)}
<p class="body" style="margin-top:60px">'5등급 합격 후기'를 볼 때는<br>어느 등급제 이야기인지 먼저 확인하세요.</p>
"""

# 4 전형 4가지 — 나열이므로 상자·번호 없이, 포트폴리오·면접만 크게
S4 = f"""
<h1 style="margin-top:48px;font-size:88px">게임학과 전형은<br>네 갈래예요.</h1>
<div class="body" style="margin-top:56px;line-height:1.7">
<p>학생부교과 &nbsp;<span class="small">내신이 핵심</span></p>
<p>학생부종합 &nbsp;<span class="small">성적과 활동, 면접을 함께</span></p>
<p>실기위주 &nbsp;<span class="small">시험장에서 그리는 실기가 당락을 좌우</span></p>
</div>
<div style="margin-top:44px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:70px;font-weight:800;letter-spacing:-2.5px;line-height:1.1">포트폴리오·면접</div>
<p class="body" style="margin-top:14px">준비해 온 작품과 면접으로 평가해요.<br>내신이 낮을 때 주력으로 잡는 전형이에요.</p>
</div>
"""

# 5 이렇게 뽑아요 — 실제 순서이므로 번호 사용
S5 = f"""
<h1 style="margin-top:48px;font-size:84px">포트폴리오·면접 전형,<br>이렇게 뽑아요.</h1>
<p class="small" style="margin-top:20px">예: 청강문화산업대 게임콘텐츠스쿨 면접전형 (2027학년도)</p>
<div style="margin-top:64px;display:flex;align-items:flex-end;gap:36px">
  <div style="font-size:230px;line-height:.8;font-weight:800;letter-spacing:-10px;color:{ORANGE}">88</div>
  <div class="body" style="padding-bottom:14px">명 모집</div>
</div>
<div class="body" style="margin-top:64px;line-height:1.7">
<p><b>1</b>&nbsp; 서류로 2배수를 먼저 뽑고</p>
<p><b>2</b>&nbsp; 심층면접으로 최종 선발</p>
</div>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: ZDNet Korea, 청강문화산업대 게임콘텐츠스쿨 (2026.09.09)<br>전형은 해마다 바뀌어요. 지원 전에 대학 모집요강을 확인하세요.</p>
"""

# 6 학년별 할 일 — 순서가 아니므로 번호 없음, 학년을 큰 글자로
def grade(g, text, hot=False):
    return f"""
<div style="display:flex;gap:30px;align-items:flex-start;margin-top:40px">
<div style="flex:none;width:170px;font-size:92px;font-weight:800;letter-spacing:-4px;line-height:1;color:{ORANGE if hot else NAVY}">{g}</div>
<p class="body" style="padding-top:14px">{text}</p></div>"""

S6 = f"""
<h1 style="margin-top:48px;font-size:88px">지금 10월,<br>학년별로 할 일</h1>
{grade("고2", "2028 모집요강 확인, 포트폴리오 첫 작품 시작.<br>겨울방학에 작품에 집중해요.", True)}
{grade("고1", "내신을 챙기면서 게임 관련 진로 활동을<br>학생부에 남겨요. 2학년 전에 전공 방향 정하기.")}
{grade("고3", "지원한 대학의 면접 준비 마무리.<br>정시 일정은 대학별로 꼭 확인해요.")}
"""

# 7 상담 — 버튼 흉내 대신 문장으로
S7 = f"""
<h1 style="margin-top:60px;font-size:92px">우리 학교, 우리 학년이면<br>어떤 전형일까요?</h1>
<p class="lead" style="margin-top:44px">모집요강을 같이 펼쳐 놓고<br>전형별 준비 순서를 정리해 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ───────────────────────── 03 국비로 배우는 게임·웹툰 ─────────────────────────
K_CHIP, K_SERIES = "취업·국비", "국비로 배우는 게임·웹툰"

# 1 표지 — 거대한 300만원 하나가 전부 (02의 '5등급'과 짝)
K1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">내일배움카드, 5년간</div>
<div style="margin-top:20px;display:flex;align-items:baseline;color:{NAVY};white-space:nowrap">
  <span style="font-size:350px;line-height:.86;font-weight:800;letter-spacing:-20px;margin-left:-12px">300</span>
  <span style="font-size:124px;font-weight:800;letter-spacing:-4px;margin-left:10px">만원</span>
</div>
<h1 style="margin-top:110px;font-size:84px">국비로 게임·웹툰,<br>배울 수 있어요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">카드 신청부터 대전점 과정까지<br>7장으로 정리했어요.</p>
"""

# 2 결론 — 순서는 카드 먼저
K2 = f"""
<h1 style="margin-top:60px;font-size:112px">카드 먼저,<br>과정은 그다음.</h1>
<p class="lead" style="margin-top:48px"><u style="text-decoration-color:{ORANGE};text-decoration-thickness:8px;text-underline-offset:12px">국민내일배움카드</u>를 발급받고,<br>고용24에서 '대전'과 분야로 검색하면 돼요.</p>
<div class="body" style="margin-top:72px">
<p>한도는 통장에 들어오는 현금이 아니라<br>훈련비를 결제할 때 쓰는 금액이에요.</p>
<p>내 부담금(자부담)은 과정마다 달라요.</p>
</div>
"""

# 3 카드 한눈에 — 숫자를 왼쪽 큰 글자로, 상자 없이
def fact(num, unit, label, note, hot=False):
    col = ORANGE if hot else NAVY
    return f"""
<div style="display:flex;gap:34px;align-items:flex-start;margin-top:46px">
<div style="flex:none;width:300px;line-height:1;color:{col}"><span style="font-size:112px;font-weight:800;letter-spacing:-5px">{num}</span><span style="font-size:48px;font-weight:800;letter-spacing:-1px;margin-left:6px">{unit}</span></div>
<div style="padding-top:18px"><p class="body" style="font-weight:700">{label}</p><p class="small" style="margin-top:6px">{note}</p></div></div>"""

K3 = f"""
<h1 style="margin-top:48px;font-size:88px">내일배움카드,<br>숫자 세 개만 기억해요.</h1>
{fact("300", "만원", "지원 한도, 5년간", "요건을 채우면 1회 200만원 추가<br>(총 500만원 이내)")}
{fact("0~55", "%", "자부담", "정부승인 훈련비 기준.<br>직종·과정 유형에 따라 달라요", True)}
{fact("5", "년", "유효기간", "남은 한도는 기간이 지나면 사라져요")}
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 고용24 「국민내일배움카드」 제도 안내 (2026.10.19 확인)<br>한도·자부담·절차는 바뀔 수 있어요. 고용24에서 최신 내용을 확인하세요.</p>
"""

# 4 신청 5단계 — 실제 순서이므로 번호 사용
def step(n, text, note="", hot=False):
    return f"""
<div style="display:flex;gap:30px;align-items:flex-start;margin-top:34px">
<div style="flex:none;width:92px;font-size:84px;font-weight:800;letter-spacing:-3px;line-height:1;color:{ORANGE if hot else NAVY}">{n}</div>
<div style="padding-top:16px"><p class="body" style="font-weight:700">{text}</p>{f'<p class="small" style="margin-top:4px">{note}</p>' if note else ''}</div></div>"""

K4 = f"""
<h1 style="margin-top:48px;font-size:88px">신청은<br>다섯 단계예요.</h1>
{step(1, "고용24 가입", "work24.go.kr")}
{step(2, "내일배움카드 신청")}
{step(3, "과정 검색", "지역 '대전' + 게임·웹툰·유니티·그래픽", True)}
{step(4, "훈련기관 상담·입과 절차", "과정마다 상담, 테스트가 있을 수 있어요")}
{step(5, "수강 신청·결제", "자부담이 있으면 함께 내요")}
"""

# 5 국가기간·전략산업직종훈련 — 핵심 한 줄만 오렌지 선으로
K5 = f"""
<h1 style="margin-top:48px;font-size:84px">'국가기간·전략산업<br>직종훈련'은 뭐가 달라요?</h1>
<div class="body" style="margin-top:56px;line-height:1.7">
<p>국가 경제에 중요한 기간산업이나<br>인력이 부족한 전략산업 분야 인재를<br>기르려고 정부가 지정한 훈련이에요.</p>
</div>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:64px;font-weight:800;letter-spacing:-2px;line-height:1.15">같은 카드로 들어요.</div>
<p class="body" style="margin-top:14px">다만 지원 조건과 자부담이<br>일반 과정과 다를 수 있어요.</p>
</div>
<p class="body" style="margin-top:52px">정확한 훈련비와 내 부담금은<br>고용24에서 과정명을 검색해 확인하세요.</p>
"""

# 6 대전점 등록 과정 3개 — 순서가 아니므로 번호 없음
def course(name, kind, hot=False):
    return f"""
<div style="margin-top:46px">
<div style="font-size:72px;font-weight:800;letter-spacing:-2.5px;line-height:1.1;color:{ORANGE if hot else NAVY}">{name}</div>
<p class="small" style="margin-top:10px;font-size:30px">{kind}</p></div>"""

K6 = f"""
<h1 style="margin-top:48px;font-size:88px">고용24에 있는<br>대전점 과정, 셋.</h1>
{course("게임그래픽", "국민내일배움카드 과정")}
{course("게임프로그래밍(유니티)", "국가기간·전략산업직종훈련", True)}
{course("웹툰", "국민내일배움카드 과정")}
<p class="body" style="margin-top:auto;padding-bottom:40px">세 과정 모두 입과 전에<br>상담과 간단한 실기로 기초를 확인해요.</p>
"""

# 7 상담
K7 = f"""
<h1 style="margin-top:60px;font-size:92px">내가 대상인지,<br>자부담은 얼마인지</h1>
<p class="lead" style="margin-top:44px">과정별 대상 여부와 입과 절차를<br>상담에서 정리해 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

SETS = {
    "02": ("입시", "성적이 낮아도 게임학과", [S1, S2, S3, S4, S5, S6, S7]),
    "03": (K_CHIP, K_SERIES, [K1, K2, K3, K4, K5, K6, K7]),
}

if __name__ == "__main__":
    n = 0
    for key, (chip, series, slides) in SETS.items():
        for i, body in enumerate(slides, start=1):
            (SRC / f"v2_{key}_{i:02d}.html").write_text(frame(i, body, chip, series, len(slides)), encoding="utf-8")
            n += 1
    print("written", n)
