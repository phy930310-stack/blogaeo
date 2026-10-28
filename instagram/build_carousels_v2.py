"""카드뉴스 v2 — .claude/skills/frontend-design/적용규칙.md 를 적용한 버전 (2026-10-28).

사용: python3 instagram/build_carousels_v2.py && node .claude/skills/aeo-blog/scripts/render.mjs instagram/assets
파일: instagram/assets/v2_02_01.png ~ v2_02_07.png (표지 포함 7장)

디자인 계획(02 성적이 낮아도 게임학과):
- 바탕 종이(#F4F6FB) + 네이비 잉크. 오렌지는 장마다 한 곳.
- 기억 요소 = 거대한 숫자 '5'와 등급 위치 눈금. 카드 상자 없음. 번호는 실제 순서(서류→면접)에만.
- 수치·사실은 posts/2026-10-01_게임학과-내신-5등급 (ZDNet 2026.09.09 등) 에서만.
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


def frame(n, body, chip="입시"):
    top = f'<div class="top"><span><b>{chip}</b>&nbsp; 성적이 낮아도 게임학과</span><span>{n}/7</span></div>' if n > 1 else ""
    foot = f'<div class="foot"><img src="logo/SBS아카데미게임학원_Color.png" alt="SBS아카데미게임학원"><span>{"대전점" if n < 7 else "@sbs_game_daejeon"}</span></div>'
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

if __name__ == "__main__":
    for i, s in enumerate([S1, S2, S3, S4, S5, S6, S7], start=1):
        (SRC / f"v2_02_{i:02d}.html").write_text(frame(i, s), encoding="utf-8")
    print("written 7")
