"""티스토리 본문 부품 생성기 — templates/tistory-components.html 과 같은 인라인 스타일 HTML을 함수로 만든다.
사용 예 (원고 작성 시 파이썬에서):
    import sys; sys.path.insert(0, ".claude/skills/aeo-blog/scripts"); from tcomp import *
    html = "\\n".join([p("..."), summary(["..",".."]), table(["갈래","내용","직군"], [[..],[..]]), img("공통_x.png","대체텍스트"), ...])
"""
import html as _h

def esc(s):  # 본문 텍스트 안의 <b> 등 태그를 쓰려면 raw=True
    return _h.escape(s, quote=False)

def p(text, raw=True):
    return f"<p>{text if raw else esc(text)}</p>"

def note(text):
    return f'<p style="color:#5B6380;font-size:0.9em;">{text}</p>'

def h2(text):
    return f"<h2>{text}</h2>"

def ul(items):
    return "<ul>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ul>"

def ol(items):
    return "<ol>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ol>"

def summary(items, title="핵심 요약"):
    li = "\n".join(f'<li style="margin:4px 0;">{i}</li>' for i in items)
    return (f'<div style="background:#F4F6FB;border-left:4px solid #1E2A78;border-radius:8px;padding:16px 20px;margin:20px 0;text-align:left;word-break:keep-all;">\n'
            f'<p style="margin:0 0 8px;font-weight:bold;color:#1E2A78;">{title}</p>\n'
            f'<ul style="margin:0;padding-left:20px;text-align:left;">\n{li}\n</ul>\n</div>')

_TH = "background:#1E2A78;color:#fff;padding:10px 12px;border:1px solid #1E2A78;text-align:left;white-space:nowrap;"
_TD1 = "padding:10px 12px;border:1px solid #DCE1EE;white-space:nowrap;font-weight:bold;text-align:left;"
_TD = "padding:10px 12px;border:1px solid #DCE1EE;text-align:left;"

def table(head, rows):
    assert len(head) <= 3, "표는 3열 이하"
    mw = 520
    th = "\n".join(f'<th style="{_TH}">{x}</th>' for x in head)
    body = []
    for i, r in enumerate(rows):
        tds = "\n".join(f'<td style="{_TD1 if j == 0 else _TD}">{c}</td>' for j, c in enumerate(r))
        bg = ' style="background:#F9FAFD;"' if i % 2 else ""
        body.append(f"<tr{bg}>\n{tds}\n</tr>")
    return (f'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin:16px 0;">\n'
            f'<table style="width:100%;min-width:{mw}px;border-collapse:collapse;font-size:15px;line-height:1.5;word-break:keep-all;">\n'
            f'<thead>\n<tr>\n{th}\n</tr>\n</thead>\n<tbody>\n' + "\n".join(body) + "\n</tbody>\n</table>\n</div>")

def img(file, alt):
    return f"<p>[이미지 업로드: {file} / 대체텍스트: {alt}]</p>"

def photo(n, guide, alt):
    return f"<p>[실제 사진 {n}: (네이버용과 다른 각도로) {guide} / 대체텍스트: {alt}]</p>"

def case(title, situation, worry, checked, plan):
    rows = "\n".join(f'<p style="margin:6px 0;"><b>{k}</b> — {v}</p>' for k, v in
                     [("상황", situation), ("고민", worry), ("확인한 것", checked), ("세운 계획", plan)])
    return (f"<h2>{title} (가상 사례)</h2>\n"
            f'<div style="border:1px solid #DCE1EE;border-radius:8px;padding:16px 20px;margin:16px 0;text-align:left;word-break:keep-all;">\n'
            f'<p style="margin:0 0 10px;color:#5B6380;">아래는 상담에서 자주 나오는 고민을 재구성한 가상 사례입니다.</p>\n{rows}\n</div>')

def faq(pairs):
    if not pairs:
        return ""
    return "<h2>자주 묻는 질문</h2>\n" + "\n".join(f"<h3>Q. {q}</h3>\n<p>{a}</p>" for q, a in pairs)

def sources(date, items, tail="전형·채용 정보와 제도는 바뀔 수 있으니 반드시 공식 공고·모집요강을 확인하세요."):
    return (f'<hr>\n<p style="color:#5B6380;font-size:0.85em;"><b>참고 자료</b> ({date} 확인)<br>\n'
            + "<br>\n".join("· " + i for i in items) + f"<br>\n{tail}</p>")

def cta(kind, slug, head, sub):
    team = "입시상담팀" if kind == "입시" else "입시&취업상담팀"
    utm = f"?utm_source=tistory&amp;utm_medium=blog&amp;utm_campaign={slug}"
    btn = "display:inline-block;margin:4px 6px 4px 0;padding:12px 18px;border-radius:8px;font-weight:bold;text-decoration:none;font-size:15px;"
    return f'''<div style="margin:40px 0 24px;padding:24px 22px;border-radius:14px;background:#1E2A78;color:#fff;text-align:left;word-break:keep-all;">
<p style="margin:0 0 6px;font-size:13px;color:#FFB199;font-weight:bold;">SBS아카데미게임학원 대전점 {team}</p>
<p style="margin:0 0 8px;font-size:20px;font-weight:bold;line-height:1.45;color:#fff;">{head}</p>
<p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:#DCE1F5;">{sub}</p>
<p style="margin:0 0 14px;">
<a href="tel:042-716-7439" style="{btn}background:#FF5A36;color:#fff;">📞 전화 상담 042-716-7439</a>
<a href="http://sbsdaejeon-game.co.kr/{utm}" target="_blank" rel="noopener" style="{btn}background:#fff;color:#1E2A78;">게임학원 홈페이지 →</a>
<a href="http://webtoon-daejeon.com/{utm}" target="_blank" rel="noopener" style="{btn}background:#fff;color:#1E2A78;">웹툰학원 홈페이지 →</a>
</p>
<p style="margin:0;font-size:13px;line-height:1.6;color:#C9D0EE;">대전광역시 서구 대덕대로 179, 5층 (둔산동, 엠제이굿모닝어학원빌딩 501호) · 운영시간 09:00~22:00</p>
</div>'''

def naver_footer(kind, slug, line):
    team = "입시상담팀" if kind == "입시" else "입시&취업상담팀"
    utm = f"?utm_source=naver&utm_medium=blog&utm_campaign={slug}"
    return (f"─────────────\nSBS아카데미게임학원 대전점 {team}\n"
            "📍 대전광역시 서구 대덕대로 179, 5층 (둔산동, 엠제이굿모닝어학원빌딩 501호)\n📞 042-716-7439\n🕘 운영시간 09:00~22:00\n"
            f"{line}\n\n▶ 게임학원 홈페이지: http://sbsdaejeon-game.co.kr/{utm}\n▶ 웹툰학원 홈페이지: http://webtoon-daejeon.com/{utm}\n\n[지도]\n")
