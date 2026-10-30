"""카드뉴스 v2 — .claude/skills/frontend-design/적용규칙.md 를 적용한 버전 (2026-10-28).

사용: python3 instagram/build_carousels_v2.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets
파일: instagram/assets/v2_02_01.png ~ v2_02_06.png (6장, 2026-10-29 개정), v2_03_01.png ~ v2_03_07.png (7장), v2_04_01.png ~ v2_04_06.png (6장)
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

SETS = {
    "02": ("입시", "성적 0%, 포트폴리오 100%", [S1, S2, S3, S4, S5, S6]),
    "03": (K_CHIP, K_SERIES, [K1, K2, K3, K4, K5, K6, K7]),
    "04": (G_CHIP, G_SERIES, [G1, G2, G3, G4, G5, G6]),
}

if __name__ == "__main__":
    n = 0
    for key, (chip, series, slides) in SETS.items():
        for i, body in enumerate(slides, start=1):
            (SRC / f"v2_{key}_{i:02d}.html").write_text(frame(i, body, chip, series, len(slides)), encoding="utf-8")
            n += 1
    print("written", n)
