"""카드뉴스 v2 — .claude/skills/frontend-design/적용규칙.md 를 적용한 버전 (2026-10-28).

사용: python3 instagram/build_carousels_v2.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets
파일: instagram/assets/v2_02_01.png ~ v2_02_06.png (6장, 2026-10-29 개정), v2_03_01.png ~ v2_03_07.png (7장), v2_04_01.png ~ v2_04_06.png (6장), v2_05_01.png ~ v2_05_06.png (6장), v2_06_01.png ~ v2_06_06.png (6장, 2026-11-01), v2_07_01.png ~ v2_07_06.png (6장, 2026-11-02), v2_08_01.png ~ v2_08_06.png (6장, 2026-11-03), v2_09_01.png ~ v2_09_06.png (6장, 2026-11-04), v2_10_01.png ~ v2_10_06.png (6장, 2026-11-05), v2_11_01.png ~ v2_11_06.png (6장, 2026-11-06), v2_12_01.png ~ v2_12_06.png (6장, 2026-11-07), v2_13_01.png ~ v2_13_06.png (6장, 2026-11-09), v2_14_01.png ~ v2_14_06.png (6장, 2026-11-09), v2_15_01.png ~ v2_15_06.png (6장, 2026-11-11), v2_16_01.png ~ v2_16_06.png (6장, 2026-11-12)
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

디자인 계획(04 게임학과, 이름은 수십 개·갈래는 셋, 2026-10-30 로컬 세션):
- 같은 종이 바탕·네이비 잉크. 표지의 기억 요소 = 거대한 숫자 '3'(갈래 셋). 상자 없음. 번호는 실제 순서(고르는 3단계)에만.
- 수치·사실은 posts/2026-10-03_게임학과-종류 (홍익대 세종 게임학부 전공 계열, 공주대 게임디자인학과, 목원대 두 학과·실기 90%,
  청강대 게임콘텐츠스쿨 면접전형 88명 — ZDNet 2026.09.09) 에서만. 문구는 humanize-korean 윤문본.
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


# ───────────────────────── 02 성적 0%, 포트폴리오 100% (2026-10-29 개정, 6장) ─────────────────────────
# 목표는 상담 유입. 청강대를 앞세워 "내신을 안 보는 전형"을 알리고, 내 성적으로 되는지는 상담에서 보게 한다.
# 문구는 humanize-korean 윤문본 그대로. 수치: ZDNet 2026.09.09(청강대 88·50명), 계원예대 2026 요강(면접 100%),
# 전문대학 2027 수시 2차 접수 11.11~25. 오렌지는 장마다 한 곳.

def pct(label, num, hot=False, size=300):
    col = ORANGE if hot else NAVY
    return f"""
<div style="margin-top:26px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">{label}</div>
<div style="font-size:{size}px;line-height:.9;font-weight:800;letter-spacing:-16px;margin-left:-10px;color:{col}">{num}<span style="font-size:{size//2}px;letter-spacing:-3px;margin-left:8px">%</span></div>"""

# 1 표지 — 0%와 100%, 숫자 둘이 전부
S1 = f"""
{pct("성적", "0")}
{pct("포트폴리오", "100", True)}
<h1 style="margin-top:64px;font-size:66px;letter-spacing:-2px">청강대 게임과부터 미대까지,<br>내신 없이 들어가는 전형이 있어요.</h1>
"""

# 2 청강대 면접전형 — 100%와 모집 인원
S2 = f"""
<h1 style="margin-top:44px;font-size:84px">청강대는 면접전형으로<br>제일 많이 뽑아요.</h1>
<p class="small" style="margin-top:22px">게임콘텐츠스쿨 면접전형</p>
<div style="margin-top:10px;display:flex;align-items:flex-end;gap:28px">
  <div style="font-size:210px;line-height:.85;font-weight:800;letter-spacing:-10px;color:{NAVY}">100<span style="font-size:100px;letter-spacing:-2px">%</span></div>
  <p class="body" style="padding-bottom:12px">면접</p>
</div>
<p class="body" style="margin-top:28px">포트폴리오로 평가해요. <b style="color:{ORANGE}">내신은 안 봐요.</b></p>
<div style="margin-top:44px;display:flex;gap:72px">
  <div><div style="font-size:120px;line-height:.9;font-weight:800;letter-spacing:-5px">88<span style="font-size:48px;letter-spacing:-1px;margin-left:6px">명</span></div><p class="small" style="margin-top:10px">수시 1차</p></div>
  <div><div style="font-size:120px;line-height:.9;font-weight:800;letter-spacing:-5px">50<span style="font-size:48px;letter-spacing:-1px;margin-left:6px">명</span></div><p class="small" style="margin-top:10px">수시 2차</p></div>
</div>
<p class="body" style="margin-top:40px">애니메이션 스쿨, 웹툰 스쿨도<br>면접전형은 똑같아요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: ZDNet Korea 2026.09.09, 청강대 2027학년도 모집요강</p>
"""

# 3 청강대 말고도
S3 = f"""
<h1 style="margin-top:48px;font-size:88px">청강대 말고도<br>그런 데가 있어요.</h1>
<div class="body" style="margin-top:64px;line-height:1.6">
<p>계원예대 게임미디어과도<br><span style="font-size:64px;font-weight:800;letter-spacing:-2px">면접 100%</span>예요.</p>
<p style="margin-top:40px">미대 쪽에도 손그림 실기 없이<br>포트폴리오랑 면접으로 뽑는 전형이 있어요.</p>
</div>
<p class="lead" style="margin-top:72px">그림으로 대학 가는 길이<br><u style="text-decoration-color:{ORANGE};text-decoration-thickness:8px;text-underline-offset:12px">실기 하나만은 아니거든요.</u></p>
"""

# 4 내 성적으로 되나요?
S4 = f"""
<h1 style="margin-top:48px;font-size:72px;letter-spacing:-2px">그럼 다들 물어요.</h1>
<h1 style="margin-top:14px;font-size:100px">“내 성적으로<br>되나요?”</h1>
<div class="body" style="margin-top:56px;line-height:1.6">
<p>내 성적에 따라 위치가 다르게 보여요.</p>
<p>대학마다 비교과 요건이 따로 있고<br>게임·웹툰·애니·디자인은 내는 포트폴리오가 다 달라요.</p>
</div>
<p class="lead" style="margin-top:auto;padding-bottom:40px">성적표랑 학생부 들고 오시면<br><b style="color:{ORANGE}">전형별로 같이 봐 드려요.</b></p>
"""

# 5 수시 2차 일정 — 학년은 큰 글자, 번호 없음
def grade(g, text, hot=False):
    return f"""
<div style="display:flex;gap:30px;align-items:flex-start;margin-top:44px">
<div style="flex:none;width:250px;font-size:84px;font-weight:800;letter-spacing:-4px;line-height:1;color:{ORANGE if hot else NAVY}">{g}</div>
<p class="body" style="padding-top:12px">{text}</p></div>"""

S5 = f"""
<h1 style="margin-top:48px;font-size:84px">수시 2차 원서접수</h1>
<div style="margin-top:30px;font-size:118px;line-height:1;font-weight:800;letter-spacing:-5px;color:{ORANGE}">11월 11일 ~ 25일</div>
{grade("고3", "지금 있는 작품으로 어디까지 되는지<br>바로 확인해야 하고요.")}
{grade("고1·고2", "겨울방학 전에 포트폴리오<br>방향부터 잡아야 해요.")}
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 전문대학 2027학년도 수시 2차 일정 안내</p>
"""

# 6 상담 — 버튼 흉내 대신 문장으로
S6 = f"""
<h1 style="margin-top:60px;font-size:92px">내 성적으로<br>어느 전형까지 되는지</h1>
<p class="lead" style="margin-top:44px">성적표 한 장 들고 오세요.<br>게임·웹툰·애니·디자인, 그림으로 가는 학과라면<br>전형별 가능성이랑 준비 순서를 정리해 드려요.</p>
<div class="body" style="margin-top:72px;line-height:1.8">
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
<p class="lead" style="margin-top:34px;color:{MIST}">상담부터 카드 신청까지<br>7장으로 정리했어요.</p>
"""

# 2 결론 — 순서는 상담 먼저 (brand/profile.md 2026-10-28: 입과 테스트가 있어 카드부터 만들면 입과가 안 될 수 있음)
K2 = f"""
<h1 style="margin-top:60px;font-size:112px">상담 먼저,<br>카드는 그다음.</h1>
<p class="lead" style="margin-top:48px">학원 상담에서 <u style="text-decoration-color:{ORANGE};text-decoration-thickness:8px;text-underline-offset:12px">과정과 입과 절차</u>를 확인한 뒤<br>내일배움카드를 신청하는 순서를 권해요.</p>
<div class="body" style="margin-top:72px">
<p>카드부터 만들면 과정에 따라<br>입과가 안 될 수 있어요.</p>
<p>한도는 통장에 들어오는 현금이 아니라<br>훈련비를 결제할 때 쓰는 금액이에요.</p>
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
{step(1, "학원 상담·과정 확인", "대상 여부와 입과 절차(간단한 실기)를 먼저 확인해요", True)}
{step(2, "고용24 가입", "work24.go.kr")}
{step(3, "내일배움카드 신청")}
{step(4, "과정 검색·입과 절차", "지역 '대전' + 과정명")}
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
<p class="lead" style="margin-top:44px">과정별 대상 여부와 입과 절차를<br>상담에서 정리해 드려요. 카드 신청은 그다음에.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ───────────────────────── 04 게임학과, 이름은 수십 개·갈래는 셋 (2026-10-30, 6장) ─────────────────────────
G_CHIP, G_SERIES = "입시", "게임학과, 갈래는 셋"

# 1 표지 — 거대한 '3' 하나
G1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">게임학과 이름은 수십 개, 갈래는</div>
<div style="margin-top:8px;display:flex;align-items:baseline;color:{NAVY};white-space:nowrap">
  <span style="font-size:420px;line-height:.86;font-weight:800;letter-spacing:-20px;margin-left:-14px">3</span>
  <span style="font-size:124px;font-weight:800;letter-spacing:-4px;margin-left:14px">갈래</span>
</div>
<h1 style="margin-top:96px;font-size:84px">이름만 보고 원서 쓰면<br><span class="mark">엉뚱한 과</span>에 가요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">게임디자인학과인데 그림을 안 배우기도 해요.</p>
"""

# 2 세 갈래 — 순서가 아니므로 번호 없음
def track(name, learn, job, hot=False):
    return f"""
<div style="margin-top:44px">
<div style="font-size:72px;font-weight:800;letter-spacing:-2.5px;line-height:1.1;color:{ORANGE if hot else NAVY}">{name}</div>
<p class="body" style="margin-top:12px">{learn}</p>
<p class="small" style="margin-top:6px">{job}</p></div>"""

G2 = f"""
<h1 style="margin-top:48px;font-size:88px">세 갈래,<br>배우는 게 달라요.</h1>
{track("공학계", "C++·C#, 언리얼·유니티 같은 엔진", "프로그래머로 이어져요")}
{track("미술계", "드로잉·원화, 3D 모델링, UI", "원화가·3D 아티스트로 이어져요", True)}
{track("콘텐츠·융합", "게임 기획·시나리오에<br>그래픽·프로그래밍 기초를 얹어요", "기획자·레벨 디자이너로 이어져요")}
"""

# 3 같은 이름, 다른 과
def school(name, text):
    return f"""
<div style="margin-top:40px;padding-left:28px;border-left:6px solid rgba(30,42,120,.18)">
<div style="font-size:44px;font-weight:800;letter-spacing:-1.5px;line-height:1.2">{name}</div>
<p class="body" style="margin-top:10px">{text}</p></div>"""

G3 = f"""
<h1 style="margin-top:48px;font-size:88px">같은 이름인데<br>다른 과예요.</h1>
{school("홍익대(세종) 게임학부", "한 학부 안에서 게임소프트웨어전공은 공학계,<br>게임그래픽디자인전공은 미술계로 따로 뽑아요.")}
{school("공주대 게임디자인학과", "이름에 '디자인'이 있지만<br>기획·그래픽·프로그래밍을 같이 배워요.")}
{school("목원대", "코드 중심의 게임소프트웨어공학과와<br>그림 실기로 뽑는 게임콘텐츠학과가 따로 있어요.")}
<p class="lead" style="margin-top:auto;padding-bottom:40px">원서 전에 모집요강의 <b style="color:{ORANGE}">계열 표기</b>와<br>학과 교과목을 꼭 같이 봐야 해요.</p>
"""

# 4 갈래 따라 입시가 달라요 — 숫자는 왼쪽 큰 글자
def adm(num, unit, label, note, hot=False):
    col = ORANGE if hot else NAVY
    return f"""
<div style="display:flex;gap:34px;align-items:flex-start;margin-top:40px">
<div style="flex:none;width:300px;line-height:1;color:{col}"><span style="font-size:104px;font-weight:800;letter-spacing:-5px">{num}</span><span style="font-size:48px;font-weight:800;letter-spacing:-1px;margin-left:6px">{unit}</span></div>
<div style="padding-top:14px"><p class="body" style="font-weight:700">{label}</p><p class="small" style="margin-top:6px">{note}</p></div></div>"""

G4 = f"""
<h1 style="margin-top:48px;font-size:88px">갈래가 다르면<br>입시도 달라요.</h1>
<p class="body" style="margin-top:30px">공학계는 교과 성적과 학생부를 보는 전형이 중심이에요.</p>
{adm("90", "%", "실기 — 미술계", "목원대 게임콘텐츠학과 실기전형<br>학생부 10% + 실기 90%")}
{adm("88", "명", "면접전형 — 콘텐츠·융합계", "청강대 게임콘텐츠스쿨, 포트폴리오로 평가", True)}
<p class="lead" style="margin-top:auto;padding-bottom:40px">성적이 걱정이면 볼 곳은<br><b style="color:{ORANGE}">미술계·콘텐츠계의 포트폴리오·면접 전형</b>이에요.</p>
<p class="small" style="padding-bottom:40px">출처: 목원대 2027학년도 수시 모집요강, ZDNet Korea 2026.09.09</p>
"""

# 5 고르는 순서 — 실제 순서이므로 번호 사용
G5 = f"""
<h1 style="margin-top:48px;font-size:88px">고르는 순서는<br>거꾸로예요.</h1>
{step(1, "하고 싶은 일부터 정해요", "코드가 좋으면 프로그래머, 그리는 게 좋으면 아티스트,<br>규칙과 이야기를 짜는 게 좋으면 기획자", True)}
{step(2, "그 직군이 어느 갈래인지 확인해요")}
{step(3, "학교별로 세 가지를 비교해요", "모집요강의 계열 표기, 학과 교과목, 지원할 전형의 반영 비율")}
"""

# 6 상담
G6 = f"""
<h1 style="margin-top:60px;font-size:92px">어느 갈래가 맞는지,<br>거기서 내 성적으로<br>되는 전형은 뭔지</h1>
<p class="lead" style="margin-top:44px">관심 학교 모집요강을 같이 놓고 봐 드려요.<br>게임과든 미대든 그림으로 가는 학과라면요.</p>
<div class="body" style="margin-top:72px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ───────────────────────── 05 청강대 면접전형, 준비 순서 (2026-10-31, 6장) ─────────────────────────
# 근거: posts/2026-10-06_청강대-게임과-포트폴리오 (ZDNet Korea 2026.09.09 — 2027학년도 정원 238명, 면접전형 수시 1차 88·2차 50명,
# 실기전형 60명·4절지 4시간, 서류 2배수→심층 면접 15분 이내, 원본 지참, 분야별 제출물; 전문대 수시 2차 접수 11.11~25).
# 기억 요소 = 거대한 '15분'. 상자 없음. 번호는 실제 순서(면접 진행 3단계·준비 순서 4단계)에만. 오렌지는 장마다 한 곳. 문구는 humanize-korean light 윤문본.
C_CHIP, C_SERIES = "입시", "청강대 면접전형, 준비 순서"

# 1 표지 — 거대한 '15분'
C1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">청강대 게임콘텐츠스쿨 면접, 1인당</div>
<div style="margin-top:8px;display:flex;align-items:baseline;color:{NAVY};white-space:nowrap">
  <span style="font-size:420px;line-height:.86;font-weight:800;letter-spacing:-20px;margin-left:-14px">15</span>
  <span style="font-size:124px;font-weight:800;letter-spacing:-4px;margin-left:14px">분</span>
</div>
<h1 style="margin-top:96px;font-size:84px">내 작품을 <span class="mark">말로</span><br>설명해야 해요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">그림만 잘 그리면 될 줄 알았다면<br>준비 순서를 다시 잡아야 해요.</p>
"""

# 2 면접전형으로 138명 — 숫자는 왼쪽 큰 글자
C2 = f"""
<h1 style="margin-top:48px;font-size:88px">면접전형으로<br>138명을 뽑아요.</h1>
<p class="small" style="margin-top:18px;font-size:30px">2027학년도 게임콘텐츠스쿨 정원 238명 중에서요.</p>
{adm("88", "명", "수시 1차 면접전형", "포트폴리오를 포함한 서류 + 심층 면접")}
{adm("50", "명", "수시 2차 면접전형", "11월 접수, 아직 남아 있는 길", True)}
<p class="body" style="margin-top:40px">실기전형(60명)은 시험장에서 4절지에<br>4시간 동안 그려요. 면접전형은 미리 만든<br>작품으로 평가받아서 그림 말고<br>기획·프로그래밍으로도 지원할 수 있어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: ZDNet Korea 2026.09.09 (2027학년도 모집 내용)</p>
"""

# 3 진행 — 실제 순서이므로 번호 사용
C3 = f"""
<h1 style="margin-top:48px;font-size:88px">면접은<br>이렇게 진행돼요.</h1>
{step(1, "서류 심사로 2배수를 골라요", "포트폴리오는 필수예요")}
{step(2, "심층 면접, 1인당 15분 이내", "제출한 작품을 놓고 물어봐요", True)}
{step(3, "면접 당일 원본을 가져가요", "제출한 포트폴리오의 원본을 꼭 챙겨요")}
<p class="lead" style="margin-top:auto;padding-bottom:40px">15분은 생각보다 짧아요. 작품마다<br>왜 만들었는지, 어떻게 만들었는지, 다시 만든다면<br>뭘 바꿀지를 <b style="color:{ORANGE}">1분 안에</b> 말할 수 있어야 해요.</p>
"""

# 4 분야별 제출물 — 순서가 아니므로 번호 없음
def submit(name, text, hot=False):
    return f"""
<div style="margin-top:30px;display:flex;gap:30px;align-items:baseline">
<div style="flex:none;width:300px;font-size:56px;font-weight:800;letter-spacing:-2px;line-height:1.1;color:{ORANGE if hot else NAVY}">{name}</div>
<p class="body" style="font-weight:600">{text}</p></div>"""

C4 = f"""
<h1 style="margin-top:48px;font-size:88px">분야마다<br>내는 게 달라요.</h1>
{submit("기획", "창작기획서, A4 50매 이내")}
{submit("그래픽", "창작물 이미지와 제작 과정", True)}
{submit("프로그래밍", "핵심 소스 코드와 기술명세서")}
{submit("QA&amp;비즈니스", "역기획서와 테스트 케이스")}
<p class="body" style="margin-top:52px">완성작만 모아 두면 그래픽은 빈칸이 생겨요.<br>스케치와 중간 과정까지 같이 내야 하거든요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">2027학년도 기준. 세부 형식은 해당 연도 모집요강과 가이드북에서 확인하세요.</p>
"""

# 5 준비 순서 — 접수일에서 거꾸로, 실제 순서이므로 번호 사용
C5 = f"""
<h1 style="margin-top:48px;font-size:88px">접수일에서<br>거꾸로 잡아요.</h1>
<p class="lead" style="margin-top:18px;color:{MIST}">수시 2차 원서접수 <b style="color:{ORANGE}">11월 11일~25일</b></p>
{step(1, "이번 주", "지원 분야를 하나로 정하고 모집요강의 제출 형식을 확인해요")}
{step(2, "접수 전까지", "기존 작품 중 분야에 맞는 것을 고르고<br>제작 과정·설명 문서를 채워요")}
{step(3, "접수 후 면접까지", "작품마다 1분 설명을 만들고 예상 질문으로 모의 면접을 해요")}
{step(4, "면접 당일", "제출본과 같은 원본을 따로 챙겨요")}
"""

# 6 상담
C6 = f"""
<h1 style="margin-top:60px;font-size:92px">내 작품으로<br>면접전형, 될까요?</h1>
<p class="lead" style="margin-top:44px">지금 가진 작품을 같이 보고<br>지원 분야와 접수까지의 순서를 정리해 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""


# ───────────────────────── 06 게임회사 신입, 뭘 준비할까? (2026-11-01 로컬 세션, 6장) ─────────────────────────
# 대상은 취업(비전공·직장인·졸업반). 기억 요소 = 거대한 숫자 '5'(직군 다섯). 상자 없음. 번호는 실제 순서(채용 3단계)에만.
# 수치·사실은 posts/2026-10-03_게임회사-취업-준비 (2025 대한민국 게임백서 2024년 실적 보도, 넥슨 2026 넥토리얼 보도 2026.08.25,
# 게임사 공개 채용 자료)에서만. 학력·연봉·합격률처럼 글에 없는 수치는 쓰지 않는다. 문구는 humanize-korean 검수본.
J_CHIP, J_SERIES = "취업", "게임회사 신입, 뭘 준비할까?"

# 1 표지 — 거대한 '5'
J1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">게임회사 신입 채용, 직군은</div>
<div style="margin-top:8px;display:flex;align-items:baseline;color:{NAVY};white-space:nowrap">
  <span style="font-size:420px;line-height:.86;font-weight:800;letter-spacing:-20px;margin-left:-14px">5</span>
  <span style="font-size:124px;font-weight:800;letter-spacing:-4px;margin-left:14px">갈래</span>
</div>
<h1 style="margin-top:96px;font-size:84px">포트폴리오보다<br><span class="mark">직군</span>을 먼저 정해요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">학력보다 직군에 맞는 결과물로<br>뽑는 회사가 많아요.</p>
"""

# 2 다섯 직군과 준비물 — 순서가 아니므로 번호 없음
J2 = f"""
<h1 style="margin-top:48px;font-size:88px">다섯 직군,<br>준비물이 달라요.</h1>
{submit("기획", "기획서, 기존 게임 분석서")}
{submit("프로그래밍", "직접 만든 게임과 코드(GitHub)", True)}
{submit("아트", "지원 직군에 맞춘 작품집")}
{submit("QA", "테스트 케이스, 버그 리포트 예시")}
{submit("사업·운영", "게임 운영·지표 분석 자료")}
<p class="body" style="margin-top:52px">기획·프로그래밍·아트가 게임을 만들고<br>QA가 품질을 확인하고 사업·운영이 서비스해요.</p>
"""

# 3 업계 규모 — 숫자는 왼쪽 큰 글자
J3 = f"""
<h1 style="margin-top:48px;font-size:88px">일하는 사람은<br>8만 7천여 명.</h1>
<p class="small" style="margin-top:18px;font-size:30px">2024년 8만 7,576명. 1년 사이 3.1% 늘었어요.</p>
{fact("62", "%", "제작·배급업에서 일해요", "5만 4,285명. 게임을 개발하고<br>서비스하는 쪽이에요", True)}
{fact("23.8", "조", "국내 게임산업 매출", "2024년, 23조 8천억 원 규모")}
<p class="lead" style="margin-top:auto">성장이 예전보다 느려졌다는 분석도 있어요.<br>막연한 기대 대신 지원할 직군의 공고를<br>직접 보면서 준비해야 해요.</p>
<p class="small" style="margin-top:22px;padding-bottom:40px">출처: 2025 대한민국 게임백서(2024년 실적) 보도 기준</p>
"""

# 4 채용 3단계 — 실제 순서이므로 번호 사용
J4 = f"""
<h1 style="margin-top:48px;font-size:88px">신입 채용은<br>세 단계예요.</h1>
{step(1, "서류·포트폴리오", "지원서와 직군별 결과물을 함께 내요")}
{step(2, "직무 테스트", "개발은 코딩, 아트는 실기, 기획은 과제", True)}
{step(3, "면접", "포트폴리오 작업 과정을 설명하고<br>팀·인사 면접이 이어져요")}
<p class="body" style="margin-top:52px">방식은 해마다 바뀌어요. 넥슨은 2026년 신입<br>프로그래머 인턴십에서 코딩 테스트를 AI 면접으로<br>바꾸고 AI 활용 역량 평가를 새로 넣었어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 넥슨 2026 넥토리얼 모집 보도 (2026.08.25)</p>
"""

# 5 직군별 포트폴리오 — 순서가 아니므로 번호 없음
J5 = f"""
<h1 style="margin-top:48px;font-size:88px">양보다<br>직군과의 적합도예요.</h1>
{submit("프로그래머", "플레이할 수 있는 게임 1~2개와 코드,<br>내가 만든 부분을 짧게 설명")}
{submit("아티스트", "스케치부터 완성까지의 과정,<br>3D는 여러 각도에서", True)}
{submit("기획자", "시스템 기획서 1편과 게임 분석서,<br>숫자로 쓴 밸런스 표")}
{submit("QA", "테스트 케이스와<br>재현 절차가 분명한 버그 리포트")}
<p class="lead" style="margin-top:auto;padding-bottom:40px">결과물만 늘어놓지 말고 어떤 문제를<br>어떻게 풀었는지가 보여야 해요.</p>
"""

# 6 상담
J6 = f"""
<h1 style="margin-top:60px;font-size:92px">비전공인데<br>게임회사, 될까요?</h1>
<p class="lead" style="margin-top:44px">가고 싶은 직군의 채용 공고를 같이 보며<br>포트폴리오 준비 순서를 잡아 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""


# ───────────────────────── 07 게임원화가, 뭘 그려야 할까? (2026-11-02 로컬 세션, 6장) ─────────────────────────
# 대상은 취업·진로(그림 좋아하는 고등학생·취준생). 기억 요소 = 거대한 글자 '설계도'(원화는 감상용 그림이 아니라 설계도).
# 상자 없음. 번호는 실제 순서(기획서→원화→3D, 연습 5단계)에만. 오렌지는 장마다 한 곳.
# 수치·사실은 posts/2026-10-04_게임원화가-되는-법 (인벤 현직자 인터뷰, 한국콘텐츠진흥원 게임국가기술자격 안내)에서만.
# 연봉·채용 인원·합격률처럼 글에 없는 수치는 쓰지 않는다. 문구는 humanize-korean 검수본.
A_CHIP, A_SERIES = "취업", "게임원화가, 뭘 그려야 할까?"

# 1 표지 — 거대한 '설계도'
A1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">게임원화가가 그리는 건 그림이 아니라</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:280px;line-height:.9;font-weight:800;letter-spacing:-14px;margin-left:-10px">설계도</span>
</div>
<h1 style="margin-top:96px;font-size:84px">멋진 그림보다<br><span class="mark">분명한</span> 그림이 먼저예요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">3D·2D 담당자가 보고 그대로<br>만들 수 있어야 하거든요.</p>
"""

# 2 원화가 쓰이는 자리 — 기획서→원화→3D 실제 순서이므로 번호 사용
A2 = f"""
<h1 style="margin-top:48px;font-size:88px">글을 처음<br>그림으로 바꿔요.</h1>
{step(1, "기획서", "'푸른 망토를 두른 견습 마법사'<br>같은 글만 있어요")}
{step(2, "원화", "이 글을 처음 그림으로 바꾸는 사람이<br>원화가예요", True)}
{step(3, "3D·애니메이션", "모델러가 그림을 보고 모델을 만들고<br>애니메이터가 움직임을 붙여요")}
<p class="body" style="margin-top:52px">그래서 분위기만 멋진 것보다 모양·색·재질이<br>다른 사람이 헷갈리지 않을 만큼<br>분명한 게 더 중요해요.</p>
"""

# 3 캐릭터와 배경 — 순서가 아니므로 번호 없음
A3 = f"""
<h1 style="margin-top:48px;font-size:88px">캐릭터와 배경,<br>중심을 하나 둬요.</h1>
{submit("캐릭터", "외형·의상·무기·표정.<br>인체 구조와 옷 주름, 실루엣 감각", True)}
{submit("배경", "마을·던전·건물·소품.<br>원근법과 구도, 빛과 색")}
<p class="body" style="margin-top:52px">처음부터 딱 정할 필요는 없지만<br>포트폴리오를 만들 땐 한쪽에 무게를 둬요.</p>
<p class="lead" style="margin-top:auto">신입은 보통 정해진 콘셉트를 받아<br>아이템이나 소품처럼 구체적인 물건을<br>그리는 일부터 시작해요.</p>
<p class="small" style="margin-top:22px;padding-bottom:40px">출처: 인벤 게임 원화가 현직자 인터뷰</p>
"""

# 4 연습 5단계 — 실제 순서이므로 번호 사용
A4 = f"""
<h1 style="margin-top:48px;font-size:88px">채색 욕심보다<br>형태가 먼저예요.</h1>
{step(1, "인체·크로키", "1~2분 안에 사람 동작 잡기, 매일 조금씩")}
{step(2, "원근·구도", "상자, 건물, 소품을 원근법으로")}
{step(3, "명암·색", "빛 방향에 따라 어둡고 밝은 단계 나누기")}
{step(4, "디지털 툴", "포토샵 같은 프로그램의 레이어·브러시")}
{step(5, "설정 디자인", "같은 캐릭터를 여러 버전으로 그리고<br>검은 실루엣만 봐도 구분되는지 확인", True)}
"""

# 5 포트폴리오 네 가지 — 순서가 아니므로 번호 없음
A5 = f"""
<h1 style="margin-top:48px;font-size:88px">회사는 이걸 봐요.<br>"바로 제작에 쓸 수 있나?"</h1>
{submit("설정 시트", "앞·옆·뒤, 의상 디테일, 색상표", True)}
{submit("배경·소품", "공간 하나와 그 안의 소품까지")}
{submit("작업 과정", "아이디어 스케치 여러 장과<br>최종안을 고른 이유")}
{submit("장르 맞춤", "실사풍 RPG와 캐주얼 게임은<br>원하는 그림이 달라요")}
<p class="lead" style="margin-top:auto;padding-bottom:40px">서류 다음엔 정해진 시간 안에 그리는<br>아트 테스트를 보는 곳이 많아요. 시간을 재고<br>설정화 한 장을 끝내는 연습을 해 두세요.</p>
"""

# 6 상담
A6 = f"""
<h1 style="margin-top:60px;font-size:92px">그림은 많은데<br>원화가, 될까요?</h1>
<p class="lead" style="margin-top:44px">지금까지 그린 그림을 같이 보고<br>캐릭터·배경 방향과 연습 순서를 잡아 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""


# ───────────────────────── 08 게임 3D 모델링, 툴 3개로 시작해요 (2026-11-03, 6장) ─────────────────────────
# 수치·사실은 posts/2026-10-13_게임-3D-모델링 (각 프로그램 공식 안내, 게임 에셋 제작 워크플로)에서만.
# 교육용 라이선스는 조건이 바뀌므로 '공식 페이지 확인'으로만 쓴다. 문구는 humanize-korean 검수본.
M_CHIP, M_SERIES = "진로", "게임 3D 모델링, 툴 3개로 시작해요"

# 1 표지 — 거대한 '소품부터'
M1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">3D 모델링 첫 작품은 캐릭터가 아니라</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:220px;line-height:.95;font-weight:800;letter-spacing:-12px;margin-left:-8px">소품부터</span>
</div>
<h1 style="margin-top:96px;font-size:84px">검 한 자루를<br><span class="mark">게임에 넣는</span> 데까지.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">맥스·지브러쉬·서브스턴스를<br>한 바퀴 돌려 보는 게 먼저예요.</p>
"""

# 2 게임용 3D가 다른 이유 — 순서가 아니므로 번호 없음
M2 = f"""
<h1 style="margin-top:48px;font-size:88px">게임은 1초에 수십 번<br>화면을 새로 그려요.</h1>
<p class="body" style="margin-top:40px">영화 CG는 한 장면을 오래 계산해도 되지만<br>게임은 그럴 수 없어요. 그래서 모델을<br>무겁게 만들 수가 없어요.</p>
{submit("하이폴리", "디테일을 마음껏 넣은<br>무거운 원본")}
{submit("로우폴리", "면을 줄여 정리한,<br>게임에서 실제로 쓰는 모델", True)}
{submit("베이킹", "원본의 울퉁불퉁한 디테일을<br>가벼운 모델용 그림으로 옮기기")}
<p class="lead" style="margin-top:auto;padding-bottom:40px">이 셋만 알아도 게임 3D가<br>어떻게 돌아가는지 감이 와요.</p>
"""

# 3 프로그램 세 개의 역할 — 순서가 아니므로 번호 없음
M3 = f"""
<h1 style="margin-top:48px;font-size:88px">프로그램 셋이<br>역할을 나눠요.</h1>
{submit("3ds Max", "모양 잡기, 면 정리, UV까지.<br>뼈대를 만드는 프로그램", True)}
{submit("지브러쉬", "찰흙처럼 조각해서 근육,<br>옷 주름, 갑옷 흠집을 넣어요")}
{submit("서브스턴스<br>페인터", "디테일을 굽고 녹슨 쇠·가죽·나무<br>같은 재질을 칠해요")}
<p class="body" style="margin-top:52px">3ds Max는 자격이 되는 학생이면<br>교육용 라이선스를 받을 수 있어요.<br>조건은 공식 교육 페이지에서 확인하세요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: Autodesk·Maxon·Adobe 공식 안내 (2026.10.13 확인)</p>
"""

# 4 제작 6단계 — 실제 순서이므로 번호 사용
M4 = f"""
<h1 style="margin-top:36px;font-size:84px">만드는 순서, 여섯 단계.</h1>
{step(1, "기본 형태 · 3ds Max", "비율과 큰 덩어리 잡기")}
{step(2, "디테일 조각 · 지브러쉬", "주름, 근육, 흠집")}
{step(3, "리토폴로지 · 3ds Max", "게임용 가벼운 모델로 면 다시 정리")}
{step(4, "UV 펼치기 · 3ds Max", "3D 표면을 평면으로, 귤껍질 까듯이")}
{step(5, "베이킹·텍스처 · 서브스턴스", "디테일 굽고 색·거칠기·금속감 칠하기")}
{step(6, "엔진 확인 · 유니티·언리얼", "실제 게임 화면에서 점검", True)}
"""

# 5 첫 작품 3단계 — 실제 순서이므로 번호 사용
M5 = f"""
<h1 style="margin-top:48px;font-size:88px">캐릭터부터 하면<br>중간에 멈추기 쉬워요.</h1>
<p class="body" style="margin-top:30px">인체 구조·면 정리·뼈대 넣기가 한꺼번에 몰리거든요.</p>
{step(1, "소품 하나", "검, 상자, 랜턴을 맥스에서<br>서브스턴스까지 한 바퀴", True)}
{step(2, "소품 세트", "대장간, 방 한 칸. 크기·스타일 맞추기")}
{step(3, "캐릭터·생물", "지브러쉬 조각과 인체 구조")}
<p class="body" style="margin-top:44px;font-weight:600">포트폴리오엔 완성 이미지 말고도 격자선 화면,<br>하이·로우폴리 비교, 텍스처 맵,<br>엔진 안 스크린샷까지 넣어요.</p>
"""

# 6 상담
M6 = f"""
<h1 style="margin-top:60px;font-size:92px">유튜브 보고 따라 하다<br>멈췄다면?</h1>
<p class="lead" style="margin-top:44px">목표에 맞춰 첫 작품과<br>맥스·지브러쉬·서브스턴스 연습 순서를<br>같이 정해 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""


# ───────────────────────── 09 유니티 입문, 어디서부터? (2026-11-04 로컬 세션, 6장) ─────────────────────────
# 목표는 상담 유입. 수치·사실은 posts/2026-10-19_유니티-입문 (Unity 공식 가격·플랜 안내 2026.10.19 확인, 시작 5단계, C# 기초, 독학 vs 과정)과
# brand/profile.md(게임프로그래밍(유니티) 과정은 고용24 등록, 입과 전 상담+간단한 실기)에서만. 훈련비·자부담 금액은 쓰지 않는다.
# 기억 요소 = 거대한 글자 '끝까지'(튜토리얼 따라 하기가 아니라 작은 게임 하나를 끝까지). 오렌지는 장마다 한 곳.

U_CHIP, U_SERIES = "취업", "유니티 입문, 어디서부터?"

# 1 표지 — 거대한 '끝까지'
U1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">튜토리얼은 따라 할 때만 되고 혼자선 안 된다면</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:220px;line-height:.95;font-weight:800;letter-spacing:-12px;margin-left:-8px">끝까지</span>
</div>
<h1 style="margin-top:96px;font-size:84px">작은 게임 하나를<br><span class="mark">완성하는</span> 게 먼저예요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">유니티는 무료로 시작하고<br>C#은 다섯 가지만 알면 돼요.</p>
"""

# 2 무료 플랜 — 숫자 하나
U2 = f"""
<h1 style="margin-top:48px;font-size:88px">유니티,<br>돈 내야 하나요?</h1>
{fact("20", "만 달러", "지난 12개월 매출·자금이 이 아래면", "Unity Personal 플랜 무료 (2026년 기준)", True)}
<p class="body" style="margin-top:56px">개인이나 작은 팀은 여기에 다 들어가요.<br>Unity 6부터는 Personal도 시작 화면(스플래시)을<br>끌 수 있고, 한때 논란이던 '런타임 요금'은<br>취소됐어요.</p>
<p class="body" style="margin-top:40px">유니티는 모바일·PC 게임에 두루 쓰이고<br>스크립트는 C#으로 써요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: Unity 공식 가격·플랜 안내 (2026.10.19 확인)<br>조건은 바뀔 수 있어요. 공식 가격 페이지에서 확인하세요.</p>
"""

# 3 시작 5단계 — 실제 순서이므로 번호 사용
U3 = f"""
<h1 style="margin-top:36px;font-size:84px">시작은 다섯 단계예요.</h1>
{step(1, "Unity Hub 설치", "에디터 버전 고르고 2D·3D 템플릿으로 새 프로젝트")}
{step(2, "에디터 화면 익히기", "Scene·Game·Hierarchy·Inspector·Project 다섯 창")}
{step(3, "오브젝트와 컴포넌트", "모든 건 오브젝트, 기능은 컴포넌트를 붙여서")}
{step(4, "C# 스크립트로 움직이기", "키 입력으로 캐릭터 이동, 부딪히면 점수")}
{step(5, "작은 게임 완성", "시작 화면부터 게임 오버까지, 빌드까지", True)}
"""

# 4 C# 다섯 가지 — 순서가 아니므로 번호 없음
U4 = f"""
<h1 style="margin-top:48px;font-size:88px">C#은 이만큼만<br>알면 시작돼요.</h1>
{submit("변수", "점수·체력·속도 저장")}
{submit("조건문<br>반복문", "충돌 판정, 적 여러 마리 처리")}
{submit("함수<br>클래스", "기능 묶기, 스크립트 구조", True)}
<p class="body" style="margin-top:52px">Start()는 시작할 때 한 번,<br>Update()는 매 프레임마다 실행돼요.<br>이것만 이해해도 입문 예제는 따라가요.</p>
<p class="lead" style="margin-top:auto;padding-bottom:40px">나머지는 게임을 만들면서<br>필요할 때 익히면 돼요.</p>
"""

# 5 독학 vs 과정 — 핵심 한 줄만 오렌지 선
U5 = f"""
<h1 style="margin-top:48px;font-size:88px">독학으로<br>충분할까요?</h1>
<p class="body" style="margin-top:40px">취미로 만들어 보는 정도면<br>Unity Learn 무료 튜토리얼로 충분해요.</p>
<div style="margin-top:48px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">기한 안에 포트폴리오를<br>끝내야 한다면 달라요.</div>
<p class="body" style="margin-top:14px">코드 리뷰와 진도 관리가 있는<br>환경이 도움이 돼요.</p>
</div>
<p class="body" style="margin-top:48px">대전점 게임프로그래밍(유니티) 과정은<br>고용24 등록 과정이라 내일배움카드로<br>들을 수 있어요. 입과 전에 상담과<br>간단한 실기로 기초를 확인해요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">순서는 상담 → 과정 확인 → 카드 신청. 훈련비·자부담은 고용24에서 과정명으로 확인하세요.</p>
"""

# 6 상담
U6 = f"""
<h1 style="margin-top:60px;font-size:92px">따라 할 때만 되고<br>혼자선 안 된다면?</h1>
<p class="lead" style="margin-top:44px">C# 기초 정리부터 첫 미니 게임,<br>국비 과정이 되는지까지<br>상담에서 같이 봐 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""


# ───────────────────────── 10 언리얼 입문, 블루프린트부터 (2026-11-05, 6장) ─────────────────────────
# 수치·사실은 posts/2026-11-01_언리얼-엔진-입문 (에픽게임즈 라이선스·FAQ, 언리얼 엔진 5.8 공식 문서, 게임잡·더팀스 공고, 2026.11.01 확인) 에서만.
E_CHIP, E_SERIES = "취업", "언리얼 입문, 블루프린트부터"

# 1 표지 — 거대한 '블루프린트'
E1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">유니티 쓰다 넘어오든 처음이든, 첫 달은</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:168px;line-height:.95;font-weight:800;letter-spacing:-9px;margin-left:-6px">블루프린트</span>
</div>
<h1 style="margin-top:96px;font-size:84px">코드 없이 엔진 구조를<br><span class="mark">먼저</span> 익혀요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">언리얼은 무료로 시작하고<br>C++는 둘째 달부터 붙여요.</p>
"""

# 2 무료 조건 — 숫자 하나
E2 = f"""
<h1 style="margin-top:48px;font-size:88px">언리얼,<br>돈 내야 하나요?</h1>
{fact("100", "만 달러", "제품 하나의 총매출이 이 아래면", "로열티 0 · 넘는 부분에만 5% (2026년 기준)", True)}
<p class="body" style="margin-top:56px">배우는 단계에서는 돈 들 일이 없어요.<br>에픽게임즈 스토어에서 판 매출은<br>로열티가 면제되고요.</p>
<p class="body" style="margin-top:40px">지금 최신은 5.8이에요. 언리얼 6은<br>2027년 말 얼리 액세스 예고라<br>기다릴 이유는 없어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 에픽게임즈 언리얼 엔진 라이선스·FAQ (2026.11.01 확인)<br>조건은 바뀔 수 있어요. 출시 전에 공식 라이선스 페이지를 확인하세요.</p>
"""

# 3 유니티와 차이 — 순서가 아니므로 번호 없음
E3 = f"""
<h1 style="margin-top:48px;font-size:88px">유니티와<br>뭐가 다른가요?</h1>
{submit("규칙<br>쓰는 법", "유니티는 C# 한 가지<br>언리얼은 블루프린트 + C++", True)}
{submit("무료<br>조건", "유니티 연매출 20만 달러 이하<br>언리얼 제품 매출 100만 달러까지")}
{submit("PC<br>부담", "유니티는 보통 노트북<br>언리얼은 메모리 32GB 권장")}
<p class="body" style="margin-top:48px">PC·콘솔 실사 그래픽이 목표면<br>언리얼을 먼저 켜는 게 자연스러워요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: Unity 플랜 안내(2026.10)·언리얼 엔진 5.8 공식 문서(2026.11.01 확인). 언리얼 권장 사양은 메모리 32GB, 그래픽 메모리 8GB 이상.<br>어느 쪽이 더 좋다는 뜻은 아니에요.</p>
"""

# 4 배우는 순서 5단계 — 실제 순서이므로 번호 사용
E4 = f"""
<h1 style="margin-top:36px;font-size:84px">순서는 다섯 단계예요.</h1>
{step(1, "템플릿 고치기 (2~4주)", "3인칭 템플릿을 블루프린트로, 액터·컴포넌트·이벤트")}
{step(2, "작은 게임 완성 (1~2개월)", "시작 화면부터 게임 오버까지, 실행 파일로")}
{step(3, "C++ 도입 (1~2개월)", "캐릭터·아이템 클래스를 C++로, 블루프린트에서 상속")}
{step(4, "장르 다른 게임 하나 더", "액션 다음엔 퍼즐이나 레이싱")}
{step(5, "포트폴리오 정리", "플레이 영상·실행 파일·깃허브·해결 과정 문서", True)}
"""

# 5 공고와 국비 — 핵심 한 줄만 오렌지 선
E5 = f"""
<h1 style="margin-top:48px;font-size:88px">신입 공고,<br>어디까지 요구하나요?</h1>
<p class="body" style="margin-top:40px">확인한 신입·인턴 공고 두 건은<br>모두 C++와 포트폴리오를 적었어요.<br>1차 면접에 코딩 테스트를 넣은 곳도 있고요.</p>
<div style="margin-top:48px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">블루프린트만으로는<br>프로그래머 지원이 어려워요.</div>
<p class="body" style="margin-top:14px">둘째 달부터는 C++를 꼭 넣어야 해요.</p>
</div>
<p class="body" style="margin-top:48px">대전점 게임프로그래밍 과정은 유니티·언리얼을<br>모두 다뤄요. 고용24 등록 국비 과정은<br>유니티 기준이라 언리얼 중심이면<br>상담에서 과정 구성을 먼저 확인해요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 하이퍼센트 신입 공고(2026.09 등록)·더팀스 웹젠레드스타 공고. 순서는 상담 → 과정 확인 → 카드 신청.</p>
"""

# 6 상담
E6 = f"""
<h1 style="margin-top:60px;font-size:92px">유니티로 갈지<br>언리얼로 갈지 고민이라면?</h1>
<p class="lead" style="margin-top:44px">가고 싶은 회사 공고를 같이 열어 보고<br>엔진 선택부터 C++ 비중,<br>국비 과정 여부까지 봐 드려요.</p>
<div class="body" style="margin-top:80px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ───────────────────────── 11 3D 애니메이터, 신입 문은 리깅부터 (2026-11-06) ─────────────────────────
# 근거: posts/2026-11-02_게임-3D-애니메이터-되는-법 (게임잡 시프트업 2026.10.13·스마일게이트 2026.10.12 공고,
# 크래프톤 채용 공고, Unity 6.6 매뉴얼·에픽 Control Rig 문서, Animworks 쇼릴 가이드 2026.03, brand/profile.md)
# 기억 요소 = 거대한 글자 '리깅'. 상자 없음. 번호는 실제 순서(배우는 5단계)에만. 오렌지는 장마다 한 곳.
R_CHIP, R_SERIES = "취업", "3D 애니메이터, 리깅부터"

# 1 표지 — 거대한 '리깅'
R1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">캐릭터를 움직이게 하고 싶다면, 첫 문은</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-10px;margin-left:-8px">리깅</span>
</div>
<h1 style="margin-top:90px;font-size:84px">애니메이터 자리는<br>경력을 <span class="mark">먼저</span> 봤어요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">2026년 10월 게임사 공고 세 건 기준,<br>경력 무관 자리는 리깅 담당이었어요.</p>
"""

# 2 세 직군 — 순서가 아니므로 번호 없음
R2 = f"""
<h1 style="margin-top:48px;font-size:88px">같은 팀인데<br>직군이 셋이에요.</h1>
{submit("애니<br>메이터", "캐릭터 동작·전투 연출<br>시프트업 공고는 경력 3년 이상")}
{submit("리거", "뼈대·스킨·컨트롤러 제작<br>스마일게이트 공고는 경력 무관", True)}
{submit("테크니컬<br>애니메이터", "리깅 툴·엔진 애니메이션 시스템<br>크래프톤 공고는 경력 4년 이상")}
<p class="body" style="margin-top:44px">리거 자리는 계약 1년이었지만 신입도 지원할 수 있었고<br>서류 뒤에 과제 테스트가 있을 수 있다고 적혀 있었어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 시프트업(2026.10.13 등록)·스마일게이트(2026.10.12 등록) 공고, 크래프톤 채용 공고 (2026.11.02 확인)<br>세 건을 본 결과라 회사마다 달라요. 지원 전에 공고 원문을 확인하세요.</p>
"""

# 3 리깅과 애니메이션의 차이 — 핵심 한 줄만 오렌지 선
R3 = f"""
<h1 style="margin-top:48px;font-size:88px">리깅이랑 애니메이션,<br>뭐가 다른가요?</h1>
{submit("리깅", "모델 안에 뼈대를 넣고 표면을 붙인 뒤<br>움직일 손잡이(컨트롤러)를 다는 일")}
{submit("애니<br>메이션", "그 손잡이를 시간 축에서 움직여<br>동작의 타이밍과 무게감을 만드는 일")}
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">인형에 관절과 줄을 다는 일,<br>그 인형을 연기시키는 일.</div>
</div>
<p class="body" style="margin-top:48px">캐릭터 하나가 화면에서 움직이기까지는<br>모델링 → 리깅 → 애니메이션 → 엔진 구현<br>네 단계를 거쳐요. 작은 회사는 한 사람이<br>리깅과 애니메이션을 같이 맡기도 해요.</p>
"""

# 4 배우는 순서 5단계 — 실제 순서이므로 번호 사용
R4 = f"""
<h1 style="margin-top:36px;font-size:84px">툴보다 움직임의 원리가 먼저예요.</h1>
{step(1, "움직임의 기본 원리", "타이밍·스페이싱·예비 동작, 튀는 공과 추로 시작")}
{step(2, "툴 하나", "3ds Max 또는 Maya, 집에서는 블렌더로 연습해도 돼요")}
{step(3, "리깅 기초", "뼈대·스키닝·간단한 컨트롤러, 처음엔 기성 리그로")}
{step(4, "인게임 동작 세트", "아이들·걷기·달리기·공격·피격을 반복 사이클로", True)}
{step(5, "엔진 구현", "유니티 Animator Controller·언리얼 애니메이션 블루프린트")}
"""

# 5 포트폴리오 — 숫자 하나
R5 = f"""
<h1 style="margin-top:48px;font-size:88px">포트폴리오는<br>영상 하나예요.</h1>
{fact("60", "~90초", "릴 영상 한 편", "신입은 더 짧아도 돼요. 제일 잘 된 클립을 맨 앞에,<br>두 번째로 잘 된 클립을 맨 뒤에", True)}
<p class="body" style="margin-top:48px">넣을 것은 아이들·걷기·달리기·공격·회피,<br>리액션 한두 컷, 엔진 안에서 찍은 화면이에요.<br>클립마다 내가 맡은 범위를 적어요.</p>
<p class="body" style="margin-top:36px">수준이 평균인 클립, 과한 카메라 움직임,<br>눈에 띄는 배경음악은 빼요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: Animworks 하비 뉴먼 「Game Animation Showreel」(2026.03)·시프트업 공고의 포트폴리오 안내 (2026.11.02 확인)<br>회사마다 보는 기준이 달라요. 지원 공고의 제출 안내를 먼저 확인하세요.</p>
"""

# 6 상담
R6 = f"""
<h1 style="margin-top:60px;font-size:92px">모델은 만들었는데<br>못 움직이겠다면?</h1>
<p class="lead" style="margin-top:44px">지금 수준을 같이 보고 리깅과 애니메이션 중<br>무엇부터 할지, 첫 릴 영상까지<br>연습 순서를 정리해 드려요.</p>
<p class="body" style="margin-top:40px">대전점 국비(고용24) 과정은<br>게임그래픽·게임프로그래밍·웹툰이에요.<br>순서는 상담 → 과정 확인 → 카드 신청.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ───────────────────────── 세트 12: 게임 QA, 문서 세 개부터 (2026-11-07, 근거 posts/2026-11-04_게임-QA-되는-법) ─────────────────────────
Q_CHIP, Q_SERIES = "취업", "게임 QA, 문서 세 개부터"

# 1 표지 — 거대한 'QA'
Q1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">게임 많이 한 게 전부라면, 첫 문은</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-6px;margin-left:-6px">QA</span>
</div>
<h1 style="margin-top:90px;font-size:84px">신입 공고는 학력·경력을<br><span class="mark">안</span> 봤어요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">넥슨네트웍스·NC소프트·엔씨큐에이 공고 기준,<br>대신 직접 쓴 문서를 봐요.</p>
"""

# 2 QA의 하루 4단계 — 실제 순서이므로 번호 사용
Q2 = f"""
<h1 style="margin-top:48px;font-size:88px">게임을 즐기는 일이 아니라<br>기록하는 일이에요.</h1>
{step(1, "테스트 설계", "기획서를 읽고 어떤 기능을 어떤 조건에서<br>확인할지 테스트 케이스로 적어요")}
{step(2, "테스트 실행", "기능·탐색·호환성 테스트를 적은 대로 돌려요")}
{step(3, "버그 보고", "재현 절차와 기대·실제 결과를 써서<br>기획자·개발자에게 넘겨요", True)}
{step(4, "회귀 확인", "수정된 빌드에서 같은 절차를 다시 돌려요")}
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 넥슨네트웍스 게임QA 인턴 공고(2026.08)·NC소프트 게임QA 신입 공고 (2026.11.04 확인)</p>
"""

# 3 공고가 보는 것 — 순서가 아니므로 번호 없음
Q3 = f"""
<h1 style="margin-top:48px;font-size:88px">공고는 학력 대신<br>이걸 봐요.</h1>
{submit("필수", "학력·경력 무관이 많아요.<br>버그 기술서, 게임 플레이 경력 목록 제출", True)}
{submit("우대", "프로그래밍(C#·Python 등),<br>ISTQB 자격증, 자동화·이슈 관리 도구")}
{submit("형태", "계약직·채용연계형 인턴이 많아요.<br>넥슨네트웍스 인턴은 6개월 뒤 전환 평가")}
<p class="body" style="margin-top:44px">엔씨큐에이는 자기소개서와 함께<br>플레이 경력 목록·버그 기술서를 필수로 받았어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 넥슨네트웍스(2026.01·08)·NC소프트·엔씨큐에이(2025.04 마감)·스마일게이트 Test Engineer(2026.10.23 등록) 공고 (2026.11.04 확인)<br>회사마다 달라요. 지원 전에 공고 원문을 확인하세요.</p>
"""

# 4 지원 전 문서 세 개 — 순서 아님
Q4 = f"""
<h1 style="margin-top:48px;font-size:88px">포트폴리오는<br>문서 세 개예요.</h1>
{submit("버그<br>리포트", "하는 게임 하나로 3개.<br>다른 사람이 똑같이 재현할 수 있게", True)}
{submit("테스트<br>케이스", "기능 하나, 조건별 기대 결과를 표로.<br>20~30개면 구조가 보여요")}
{submit("플레이<br>목록", "어떤 게임을 얼마나 했는지.<br>실력보다 폭과 기록이에요")}
<p class="body" style="margin-top:44px">셋 다 지금 하는 게임 하나로 만들 수 있고<br>공고가 요구하는 버그 기술서·테스트 케이스<br>작성 경험에 그대로 대응해요.</p>
"""

# 5 버그 리포트 — 핵심 한 줄만 오렌지 선
Q5 = f"""
<h1 style="margin-top:48px;font-size:88px">버그 리포트는<br>남이 재현할 수 있게.</h1>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">"가끔 멈춘다"는<br>버그 리포트가 아니에요.</div>
</div>
<p class="body" style="margin-top:48px">기본 순서는 일곱 칸이에요.<br>제목 → 환경(기기·OS·빌드 버전) → 재현 절차<br>→ 기대 결과 → 실제 결과 → 발생 빈도<br>→ 첨부(스크린샷·영상).</p>
<p class="body" style="margin-top:36px">느낌으로 적으면 개발자가 원인을 못 찾아요.<br>번호 순서대로 따라 하면 똑같이 나와야 해요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">ISTQB 기초 레벨(CTFL)은 응시 제한이 없어요. 일정·응시료는 KSTQB 공식 안내에서 확인하세요.</p>
"""

# 6 상담
Q6 = f"""
<h1 style="margin-top:60px;font-size:92px">게임 많이 한 것 말고<br>보여 줄 게 없다면?</h1>
<p class="lead" style="margin-top:44px">하는 게임 하나로 버그 리포트와<br>테스트 케이스부터 같이 써 봐요.</p>
<p class="body" style="margin-top:40px">대전점에 QA 전용 과정은 없어요.<br>게임프로그래밍(유니티)·게임기획 과정에서<br>기획서를 읽고 구조를 파악하는 힘을 길러요.<br>순서는 상담 → 과정 확인 → 카드 신청.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ---------- 13 게임 C++, 책 말고 게임 하나 (2026-11-09, posts/2026-11-05_게임-개발-cpp-공부-순서) ----------
P_CHIP, P_SERIES = "취업", "게임 C++, 책 말고 게임 하나"

# 1 표지 — 거대한 'C++'
P1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">책을 두 번 읽어도 게임이 안 만들어진다면</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-6px;margin-left:-6px">C++</span>
</div>
<h1 style="margin-top:90px;font-size:84px">문법책 끝내기가 아니라<br>게임 <span class="mark">하나</span> 끝내기예요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">언리얼 5.8 문서·게임잡 신입 공고 기준,<br>기초 5단계 뒤 과제 세 개로 확인해요.</p>
"""

# 2 왜 아직 C++인가 — 순서 아님
P2 = f"""
<h1 style="margin-top:48px;font-size:88px">엔진도 공고도<br>아직 C++예요.</h1>
{submit("언리얼", "공식 문서가 C++ 섹션을<br>'C++ 경험이 있다'는 전제로 써요")}
{submit("신입 공고", "하이퍼센트 언리얼 신입, 이스트게임즈<br>클라이언트·서버 공고 키워드에 C++", True)}
{submit("예외", "모바일·유니티 공고(기어세컨드)는<br>C#·유니티 중심, C# 코드 제출")}
<p class="body" style="margin-top:44px">목표가 언리얼·PC·콘솔·서버면 C++,<br>모바일·유니티면 C#부터예요.<br>넥슨 넥토리얼 2026은 "C++ 또는 C#"이었어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 언리얼 엔진 5.8 공식 문서, 게임잡 신입 공고(2026.08~09 등록), 넥슨 넥토리얼 2026 모집 안내 (2026.11.05 확인)</p>
"""

# 3 기초 5단계 — 실제 순서이므로 번호
P3 = f"""
<h1 style="margin-top:48px;font-size:88px">기초는 다섯 단계예요.</h1>
{step(1, "변수·제어문·함수", "체력·점수를 담고 턴을 돌려요. 규칙의 뼈대")}
{step(2, "포인터·참조·메모리", "캐릭터 하나를 여러 시스템이 복사 없이 가리켜요")}
{step(3, "클래스·상속·가상함수", "몬스터 공통 클래스. 언리얼 액터·컴포넌트 구조", True)}
{step(4, "STL 컨테이너·알고리즘", "vector·map으로 인벤토리·적 목록. 코딩 테스트 범위")}
{step(5, "스마트 포인터·RAII", "자원을 객체 수명에 묶어 누수를 막아요")}
<p class="small" style="margin-top:auto;padding-bottom:40px">단계마다 책 한 권을 다 읽을 필요는 없어요. 그 단계 문법으로 작은 프로그램 하나가 돌아가면 다음으로.</p>
"""

# 4 확인 과제 세 개 — 순서
P4 = f"""
<h1 style="margin-top:48px;font-size:88px">끝났는지는<br>과제 세 개로 확인해요.</h1>
{step(1, "콘솔 텍스트 게임", "턴제 전투나 텍스트 던전. 클래스로 캐릭터·몬스터,<br>vector로 인벤토리면 1~4단계 확인")}
{step(2, "SFML·SDL 2D 게임", "창을 띄우고 키 입력으로 스프라이트를 움직이는<br>벽돌 깨기·슈팅. 게임 루프를 직접 짜요")}
{step(3, "언리얼 C++ 클래스 한 개", "공식 퀵스타트대로 Actor를 상속해<br>Tick에서 떠서 도는 큐브 하나", True)}
<p class="body" style="margin-top:36px">세 번째까지 되면 신입 공고가 요구하는<br>"C++로 만든 결과물"이 생겨요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 언리얼 5.8 C++ Quick Start·SFML 3.0 튜토리얼 (2026.11.05 확인)</p>
"""

# 5 공고가 보는 것 — 핵심 한 줄 오렌지 선
P5 = f"""
<h1 style="margin-top:48px;font-size:88px">공고는 완독을<br>안 봐요.</h1>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">코딩 테스트는 있기도 없기도,<br>포트폴리오는 전부 요구했어요.</div>
</div>
<p class="body" style="margin-top:48px">하이퍼센트는 1차 면접에서 간단한 코딩 테스트,<br>넥슨 넥토리얼 2026은 코딩 테스트를 없앴고,<br>엔씨 2026 신입 공채는 프로그래밍 지원자에게<br>온라인 코딩 테스트를 추가했어요.</p>
<p class="body" style="margin-top:36px">준비는 두 갈래예요. STL로 정렬·탐색 문제 풀기,<br>과제 세 개를 깃허브 코드와 플레이 영상으로 정리하기.<br>면접에선 내가 쓴 코드를 설명할 수 있어야 해요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 하이퍼센트 공고(2026.09), 넥슨 넥토리얼 2026 안내·데일리안(2026.08.26), 토요경제(2025.10.02) (2026.11.05 확인)<br>회사마다 달라요. 지원 전에 공고 원문을 확인하세요.</p>
"""

# 6 상담
P6 = f"""
<h1 style="margin-top:60px;font-size:92px">책은 읽었는데<br>게임이 안 만들어진다면?</h1>
<p class="lead" style="margin-top:44px">지금 어느 단계인지 보고<br>다음 과제 하나를 같이 정해요.</p>
<p class="body" style="margin-top:40px">대전점 게임프로그래밍 과정은 유니티·언리얼을 다뤄요.<br>국비 등록 과정은 유니티 기준이라<br>C++·언리얼 비중은 상담에서 과정 구성으로 확인해요.<br>순서는 상담 → 과정 확인 → 카드 신청.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ---------- 14 TV에 나온 게임 기획자 (2026-11-09, MBC 전지적 집착 시점 선공개 fOkis7RA8cw 자막 + posts/2026-10-06_게임기획자-되는-법) ----------
# 영상 장면·캡처 사용 금지(MBC 무단 전재 금지). 자막에서 확인된 말만 글자로 인용한다.
T_CHIP, T_SERIES = "취업", "TV에 나온 게임 기획자"

# 1 표지 — 거대한 '9년'
T1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">전지적 집착 시점에 나온 배그 개발팀 기획자</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-6px;margin-left:-6px">9년</span>
</div>
<h1 style="margin-top:90px;font-size:84px">게임 회사에서 9년,<br>기획자는 <span class="mark">무슨 일</span>을 할까요?</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">MBC 선공개 영상(11/7)에서 나온 말만 모았어요.<br>장면은 안 쓰고 글로만 정리했어요.</p>
"""

# 2 영상에서 확인된 사실 — 순서 아님
T2 = f"""
<h1 style="margin-top:48px;font-size:88px">배그 초창기 멤버,<br>기획과 분석을 맡고 있어요.</h1>
{submit("소속", "크래프톤 PUBG 스튜디오<br>배틀그라운드 개발팀 9년 차, 내년 10주년")}
{submit("맡은 일", "내부에서 기획과 분석 파트를<br>꾸준히 담당하고 있대요", True)}
{submit("상사의 소개", "배그가 커질 때<br>손을 안 거친 게 없는 초창기 멤버")}
<p class="body" style="margin-top:44px">한 게임을 9년 동안 기획하고 분석한 사람이<br>TV에 나온 거예요. 기획자가 무슨 일을 하는지<br>보여 주는 드문 장면이에요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: MBC 「전지적 집착 시점」 선공개 영상 자막 (유튜브 MBCentertainment, 2026.11.07 게시, 11.09 확인)<br>출연자·방송사·크래프톤은 저희 학원과 관계가 없어요.</p>
"""

# 3 기획과 분석 — 일반 직무 구분
T3 = f"""
<h1 style="margin-top:48px;font-size:88px">기획과 분석은<br>이렇게 나뉘어요.</h1>
{step(1, "시스템·콘텐츠 기획", "전투·성장·보상 규칙과 퀘스트를 정하고<br>개발팀이 바로 만들 수 있게 문서로 써요")}
{step(2, "밸런스", "능력치·확률·재화를 엑셀로 맞춰요")}
{step(3, "분석", "플레이 데이터로 어디서 그만두는지,<br>무엇을 고칠지 찾아 기획에 되돌려요", True)}
{step(4, "라이브 운영", "업데이트 뒤 반응을 보고 다시 기획해요")}
<p class="small" style="margin-top:auto;padding-bottom:40px">일반적인 기획 직무 기준(게임기획자 되는 법 글, 현직자 Q&amp;A). 회사마다 이름과 범위가 달라요.</p>
"""

# 4 플레이 2,314시간 — 핵심 한 줄 오렌지 선
T4 = f"""
<h1 style="margin-top:48px;font-size:88px">플레이 2,314시간,<br>그런데 상태창은 꺼요.</h1>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">표시가 다 켜져 있으면 쉬워지고<br>반복하면 질린대요.</div>
</div>
<p class="body" style="margin-top:48px">기획자는 자기 게임을 '처음 하는 사람'처럼<br>다시 봐야 해요. 그래서 일부러 난이도를 올려요.<br>많이 하는 게 아니라 다르게 보는 게 일이에요.</p>
<p class="body" style="margin-top:36px">주말에도 회사에 있는 장면은<br>방송의 재미 포인트예요.<br>직무의 조건이 아니니 따라 할 필요는 없어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 같은 영상 자막(플레이 타임 2,314시간, 상태창·데미지 표시 끄기). 해석은 저희 설명이에요.</p>
"""

# 5 신입 준비물 — 순서 아님
T5 = f"""
<h1 style="margin-top:48px;font-size:88px">신입은 플레이 시간 말고<br>문서 네 개로 보여 줘요.</h1>
{submit("역기획서", "하는 게임의 시스템 하나를<br>거꾸로 분석해 문서로")}
{submit("시스템 기획서", "새 규칙 하나를<br>예외 상황까지 설계")}
{submit("밸런스 시트", "엑셀로 성장·보상 수치와 근거")}
{submit("분석 1건", "내 플레이 기록이나 공개 지표로<br>'왜 그만두나' 한 장", True)}
<p class="body" style="margin-top:44px">3,000시간을 했다는 말보다<br>그 3,000시간에서 무엇을 봤는지가 포트폴리오예요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">기준: 게임기획자 되는 법 글(현직자 Q&amp;A·채용 콘텐츠, 2026.10). 공고마다 요구 문서가 달라요.</p>
"""

# 6 상담
T6 = f"""
<h1 style="margin-top:60px;font-size:92px">게임은 3,000시간,<br>기획서는 0장이라면?</h1>
<p class="lead" style="margin-top:44px">플레이 기록을 분석 노트로 바꾸는 것부터<br>같이 정해요.</p>
<p class="body" style="margin-top:40px">대전점에 게임기획 과정이 있어요.<br>과정 구성은 상담에서 확인해요.<br>국비 등록 과정은 게임그래픽·게임프로그래밍(유니티)·웹툰이라<br>기획은 상담으로 먼저 확인하는 게 맞아요.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ---------- 15 배경 원화, 투시부터 (2026-11-11, posts/2026-11-10_게임-배경-원화가-되는-법) ----------
B_CHIP, B_SERIES = "취업", "배경 원화, 투시부터"

# 1 표지 — 거대한 '투시'
B1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">캐릭터는 되는데 배경만 넣으면 무너진다면</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-6px;margin-left:-6px">투시</span>
</div>
<h1 style="margin-top:90px;font-size:84px">배경 원화의 기초는<br>인체가 아니라 <span class="mark">투시</span>예요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">게임잡 배경 원화 공고 세 건 기준,<br>하는 일과 연습 여섯 단계를 정리했어요.</p>
"""

# 2 하는 일 — 순서 아님
B2 = f"""
<h1 style="margin-top:48px;font-size:88px">배경 원화가는<br>공간을 설계해요.</h1>
{submit("무드 컨셉", "씬 전체 분위기 설정.<br>레벨 제작에 쓰여요")}
{submit("프랍 컨셉", "소품 디자인과 제작용 원화.<br>3D 배경 제작에 쓰여요", True)}
{submit("일러스트", "그래픽 컨셉을 보여 주는 그림")}
<p class="body" style="margin-top:44px">그림 한 장이 결과물이 아니에요.<br>3D 배경 모델러가 보고 만들 수 있게<br>넘기는 그림이에요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 NC 「AION2」 배경 컨셉 아티스트 공고 담당 업무(2026.09.28 등록, 11.10 확인)</p>
"""

# 3 캐릭터 원화와 차이 — 순서 아님
B3 = f"""
<h1 style="margin-top:48px;font-size:88px">캐릭터 원화와<br>기초가 달라요.</h1>
{submit("그리는 것", "인물·의상이 아니라<br>공간·건물·소품")}
{submit("기초", "인체·실루엣이 아니라<br>투시·조명·스케일", True)}
{submit("넘기는 곳", "3D 배경 모델러와<br>레벨 제작")}
<p class="body" style="margin-top:44px">배경은 여러 사람이 나눠 그려도<br>한 세계처럼 보여야 해요.<br>그래서 내 화풍보다 프로젝트 화풍이 먼저예요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 시프트업·NC 배경 원화 공고 자격 요건(2026.11.10 확인)</p>
"""

# 4 연습 여섯 단계 — 실제 순서이므로 번호
B4 = f"""
<h1 style="margin-top:48px;font-size:88px">연습은 여섯 단계예요.</h1>
{step(1, "투시", "1·2·3점 투시로 상자와 건물. 눈높이 선부터")}
{step(2, "명암·조명", "광원 하나, 흑백 서너 단계로 덩어리 나누기")}
{step(3, "소품", "문·가로등을 앞·옆에서. 사람 실루엣으로 크기 표시")}
{step(4, "썸네일 여러 장", "한 공간을 흑백 스케치 여섯 장 이상으로", True)}
{step(5, "키 아트 한 장", "고른 안을 분위기와 조명이 보이는 큰 그림으로")}
{step(6, "설정 시트", "소품과 건물 조각의 형태·재질·크기 정리")}
"""

# 5 공고가 본 것 — 핵심 한 줄 오렌지 선
B5 = f"""
<h1 style="margin-top:48px;font-size:88px">공고 세 건,<br>전부 포트폴리오 필수.</h1>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">3D 이해는 세 건 모두 우대,<br>화풍은 회사마다 반대였어요.</div>
</div>
<p class="body" style="margin-top:48px">빅게임스튜디오는 2D 애니풍,<br>NC는 실사풍 컨셉을 찾았어요.<br>지원할 프로젝트 화풍부터 정해요.</p>
<p class="body" style="margin-top:36px">포트폴리오는 키 아트 한 장에<br>썸네일 과정, 프랍 시트, 스케일 표시를 붙여요.<br>완성작보다 설계 과정이 보여야 해요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 시프트업(2026.09.10)·빅게임스튜디오(06.22)·NC(09.28) 공고 (11.10 확인)<br>포트폴리오 구성은 공고 문구에서 끌어낸 제안이에요. 지원 전에 공고 원문을 확인하세요.</p>
"""

# 6 상담
B6 = f"""
<h1 style="margin-top:60px;font-size:92px">배경만 넣으면<br>그림이 무너진다면?</h1>
<p class="lead" style="margin-top:44px">지금 그린 그림을 같이 보고<br>투시부터 다시 잡을지 정해요.</p>
<p class="body" style="margin-top:40px">대전점 게임그래픽 과정에서 배울 수 있어요.<br>과정 구성은 상담에서 확인해요.<br>국비는 상담 → 과정 확인 → 카드 신청 순서예요.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ---------- 16 첫 게임, 한 판만 끝내요 (2026-11-12, posts/2026-11-09_게임-만들기-처음-시작) ----------
F_CHIP, F_SERIES = "진로", "첫 게임, 한 판만 끝내요"

# 1 표지 — 거대한 '한 판'
F1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">엔진 깔고 석 달째 캐릭터만 움직인다면</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-6px;margin-left:-6px">한 판</span>
</div>
<h1 style="margin-top:90px;font-size:84px">첫 게임은<br>한 판만 <span class="mark">끝내요</span>.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">크기, 도구, 순서, 올리는 곳을<br>공식 안내 기준으로 정리했어요.</p>
"""

# 2 크기 — 순서 아님
F2 = f"""
<h1 style="margin-top:48px;font-size:88px">첫 게임 크기는<br>이만큼이에요.</h1>
{submit("한 화면", "스크롤 없는 맵 하나")}
{submit("한 조작", "이동 하나나 버튼 하나", True)}
{submit("한 목표", "점수나 생존 시간")}
<p class="body" style="margin-top:44px">기간은 2~4주를 넘기지 않아요.<br>RPG가 하고 싶다면<br>턴제 전투 한 판만 떼어 와요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">글로벌 게임 잼도 48시간 안에 게임 하나를 끝내요.</p>
"""

# 3 도구 — 순서 아님
F3 = f"""
<h1 style="margin-top:48px;font-size:88px">코딩을 못해도<br>도구는 있어요.</h1>
{submit("GDevelop", "이벤트 블록으로 만들어요.<br>무료 플랜이 있어요")}
{submit("블루프린트", "언리얼에 들어 있어요.<br>노드를 이어서 만들어요", True)}
{submit("비주얼<br>스크립팅", "유니티에 들어 있어요.<br>퍼스널은 무료예요")}
<p class="body" style="margin-top:44px">도구는 기능보다<br>내 장르 튜토리얼이 공식 문서에 있는지<br>보고 골라요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: GDevelop·언리얼 엔진·유니티 공식 안내(2026.11.09 확인)</p>
"""

# 4 완성 여섯 단계 — 실제 순서이므로 번호 (6단계라 하단 문구 없음)
F4 = f"""
<h1 style="margin-top:48px;font-size:88px">완성은 여섯 단계예요.</h1>
{step(1, "핵심 동작 하나", "움직이고 부딪히면 끝. 그래픽은 네모여도 돼요")}
{step(2, "한 판 끝내기", "30초~1분 뒤 이기거나 지게. 여기까지가 게임", True)}
{step(3, "시작·끝 화면과 점수", "제목, 시작 버튼, 결과와 다시 하기")}
{step(4, "소리·효과", "효과음 두세 개와 배경음 하나. 라이선스 확인")}
{step(5, "세 명에게 시켜 보기", "막히는 곳만 고쳐요. 새 기능은 안 넣어요")}
{step(6, "빌드", "다른 컴퓨터에서 켜지는지 확인")}
"""

# 5 올리는 곳 — 핵심 한 줄 오렌지 선
F5 = f"""
<h1 style="margin-top:48px;font-size:88px">올리는 곳은<br>itch.io부터.</h1>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">itch.io는 무료,<br>가격도 내가 정해요.</div>
</div>
<p class="body" style="margin-top:48px">구글 플레이는 등록비 25달러 1회,<br>애플은 연 99달러,<br>스팀은 게임당 100달러예요.</p>
<p class="body" style="margin-top:36px">구글 플레이 개인 계정은<br>테스터 12명이 14일 연속 참여해야<br>정식 출시를 신청할 수 있어요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: itch.io 제작자 문서·구글 플레이 콘솔 고객센터·<br>애플 개발자 프로그램·스팀웍스 문서(2026.11.09 확인)</p>
"""

# 6 상담
F6 = f"""
<h1 style="margin-top:60px;font-size:92px">캐릭터만 움직이고<br>멈춰 있다면?</h1>
<p class="lead" style="margin-top:44px">지금 만든 걸 같이 보고<br>한 판으로 줄일 범위를 정해요.</p>
<p class="body" style="margin-top:40px">끝낸 게임 하나가 입시·취업 포트폴리오의 시작이에요.<br>대전점 게임프로그래밍(유니티·언리얼) 과정에서 배울 수 있어요.<br>국비는 상담 → 과정 확인 → 카드 신청 순서예요.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

# ---------- 17 게임 자격증, 따야 할까요? (2026-11-13, posts/2026-11-11_게임-자격증) ----------
L_CHIP, L_SERIES = "취업", "게임 자격증, 따야 할까요?"

# 1 표지 — 거대한 '자격증'
L1 = f"""
<div style="margin-top:40px;font-size:40px;font-weight:600;color:{MIST};letter-spacing:-.5px">게임회사 가려면 자격증부터?</div>
<div style="margin-top:8px;color:{NAVY};white-space:nowrap">
  <span style="display:block;font-size:200px;line-height:.95;font-weight:800;letter-spacing:-6px;margin-left:-6px">자격증</span>
</div>
<h1 style="margin-top:90px;font-size:84px">공고는 <span class="mark">포트폴리오</span>를<br>먼저 봤어요.</h1>
<p class="lead" style="margin-top:34px;color:{MIST}">종목, 일정, 합격률, 쓸모를<br>공식 누리집 기준으로 정리했어요.</p>
"""

# 2 종목 셋 — 순서 아님
L2 = f"""
<h1 style="margin-top:48px;font-size:88px">게임 자격증은<br>세 종목이에요.</h1>
{submit("기획", "게임기획전문가")}
{submit("그래픽", "게임그래픽전문가", True)}
{submit("프로그래밍", "게임프로그래밍전문가")}
<p class="body" style="margin-top:52px">한국콘텐츠진흥원이 시행하는<br>국가기술자격이에요.</p>
<p class="body" style="margin-top:36px">필기는 누구나 볼 수 있고<br>실기는 필기 합격 뒤 2년 안에 봐요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임국가기술자격검정 누리집(2026.11.11 확인)</p>
"""

# 3 일정 — 한 해에 한 번
L3 = f"""
<h1 style="margin-top:48px;font-size:88px">시험은 한 해에<br>한 번이에요.</h1>
{submit("필기", "2026년 5월 16일<br>접수는 4월 8~17일", True)}
{submit("실기", "2026년 9월 12일<br>접수는 8월 5~14일")}
<p class="body" style="margin-top:52px">2027년 일정은 아직 공고 전이에요.<br>필기를 놓치면 1년을 기다려야 해요.<br>3월 말부터 공지사항을 확인하세요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">2026년 시험 지역은 서울·대전·광주·부산·제주였어요.<br>2027년 공고 여부는 2026.11.13 확인</p>
"""

# 4 합격률 — 2025년
L4 = f"""
<h1 style="margin-top:48px;font-size:88px">2025년<br>합격률이에요.</h1>
{submit("기획", "필기 86.15%<br>실기 66.05%")}
{submit("그래픽", "필기 92.30%<br>실기 44.13%", True)}
{submit("프로그래밍", "필기 82.25%<br>실기 100%")}
<p class="body" style="margin-top:48px">프로그래밍 실기는 응시자가 35명이었어요.<br>응시자가 적어서 합격률이<br>해마다 크게 흔들려요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임국가기술자격검정 누리집 종목별 검정 현황(2025년)</p>
"""

# 5 쓸모 — 핵심 한 줄 오렌지 선
L5 = f"""
<h1 style="margin-top:48px;font-size:88px">채용 공고는<br>뭘 봤을까요?</h1>
<div style="margin-top:52px;padding-left:28px;border-left:14px solid {ORANGE}">
<div style="font-size:60px;font-weight:800;letter-spacing:-2px;line-height:1.15">공고 세 건에<br>자격증 이름은 없었어요.</div>
</div>
<p class="body" style="margin-top:48px">2026년 6~10월 게임잡 공고<br>세 건을 열어 봤어요.<br>두 건은 포트폴리오를 받았어요.</p>
<p class="body" style="margin-top:36px">자격증의 공식 우대는<br>학점은행제 20학점,<br>병역특례업체 지원 가산점 10점이에요.</p>
<p class="small" style="margin-top:auto;padding-bottom:40px">출처: 게임잡 채용 공고 3건(2026년 6~10월 등록),<br>게임국가기술자격검정 누리집 자격정보</p>
"""

# 6 상담
L6 = f"""
<h1 style="margin-top:60px;font-size:92px">자격증부터 딸지<br>작품부터 만들지?</h1>
<p class="lead" style="margin-top:44px">목표 직군과 지금까지 만든 걸<br>같이 보고 순서를 정해요.</p>
<p class="body" style="margin-top:40px">대전점에는 게임기획·게임그래픽·게임프로그래밍 과정이 있어요.<br>국비는 상담 → 과정 확인 → 카드 신청 순서예요.</p>
<div class="body" style="margin-top:56px;line-height:1.8">
<p>프로필 링크에서 <b style="color:{ORANGE}">상담 신청</b> &nbsp;<span class="small">1~2분</span></p>
<p>전화 042-716-7439 &nbsp;<span class="small">09:00~22:00</span></p>
<p>대전광역시 서구 대덕대로 179, 5층<br><span class="small">둔산동, 엠제이굿모닝어학원빌딩 501호</span></p>
</div>
"""

SETS = {
    "02": ("입시", "성적 0%, 포트폴리오 100%", [S1, S2, S3, S4, S5, S6]),
    "03": (K_CHIP, K_SERIES, [K1, K2, K3, K4, K5, K6, K7]),
    "04": (G_CHIP, G_SERIES, [G1, G2, G3, G4, G5, G6]),
    "05": (C_CHIP, C_SERIES, [C1, C2, C3, C4, C5, C6]),
    "06": (J_CHIP, J_SERIES, [J1, J2, J3, J4, J5, J6]),
    "07": (A_CHIP, A_SERIES, [A1, A2, A3, A4, A5, A6]),
    "08": (M_CHIP, M_SERIES, [M1, M2, M3, M4, M5, M6]),
    "09": (U_CHIP, U_SERIES, [U1, U2, U3, U4, U5, U6]),
    "10": (E_CHIP, E_SERIES, [E1, E2, E3, E4, E5, E6]),
    "11": (R_CHIP, R_SERIES, [R1, R2, R3, R4, R5, R6]),
    "12": (Q_CHIP, Q_SERIES, [Q1, Q2, Q3, Q4, Q5, Q6]),
    "13": (P_CHIP, P_SERIES, [P1, P2, P3, P4, P5, P6]),
    "14": (T_CHIP, T_SERIES, [T1, T2, T3, T4, T5, T6]),
    "15": (B_CHIP, B_SERIES, [B1, B2, B3, B4, B5, B6]),
    "16": (F_CHIP, F_SERIES, [F1, F2, F3, F4, F5, F6]),
    "17": (L_CHIP, L_SERIES, [L1, L2, L3, L4, L5, L6]),
}

if __name__ == "__main__":
    n = 0
    for key, (chip, series, slides) in SETS.items():
        for i, body in enumerate(slides, start=1):
            (SRC / f"v2_{key}_{i:02d}.html").write_text(frame(i, body, chip, series, len(slides)), encoding="utf-8")
            n += 1
    print("written", n)
