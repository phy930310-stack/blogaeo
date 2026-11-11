"""humanize-korean 입출력 보조 (2026-11-11)

티스토리 본문 문단의 인라인 스타일 `!important`(문단 간격용)가 humanize 사전 점수에서
느낌표로 세어져 route_hint가 heavy로 잘못 나온다. 그래서 스타일을 뗀 사본으로 윤문하고,
끝난 뒤 원고의 여는 태그는 그대로 두고 바뀐 문장만 되붙인다.

사용법 (저장소 루트에서):
  python -X utf8 .claude/skills/aeo-blog/scripts/hz_io.py strip posts/<폴더>/티스토리_본문.html _workspace/<run>/01_input.txt
  … prepare_monolith_input.py → humanize-monolith → restore_modality / strip_injected_commas / verify_gates …
  python -X utf8 .claude/skills/aeo-blog/scripts/hz_io.py apply posts/<폴더>/티스토리_본문.html _workspace/<run>/01_input.txt _workspace/<run>/final.md
"""
import io
import re
import sys

SUMMARY = re.compile(r"\n*<!-- HUMANIZE-SUMMARY.*?-->\s*$", re.S)
OPEN = re.compile(r"^(\s*<(?:p|li|h2|h3|td|th|div)\b[^>]*>)(.*)$", re.S)


def read(p):
    return io.open(p, encoding="utf-8").read().replace("\r\n", "\n")


def strip_styles(s):
    """여는 태그 안의 `!important`와 문단 간격 스타일만 뗀다(줄 수·태그 수는 그대로)."""
    s = s.replace(' style="margin:0 0 20px !important;"', "")
    return s.replace(" !important", "")


def tags(s):
    return [re.sub(r"\s+style=\"[^\"]*\"", "", t) for t in re.findall(r"<[^>]+>", s)]


def main():
    if len(sys.argv) < 4 or sys.argv[1] not in ("strip", "apply"):
        sys.exit(__doc__)
    cmd, post = sys.argv[1], sys.argv[2]
    src = read(post)
    if cmd == "strip":
        out = strip_styles(src)
        io.open(sys.argv[3], "w", encoding="utf-8", newline="").write(out)
        print(f"strip: 문단 간격 스타일 {src.count('margin:0 0 20px !important')}개, !important {src.count('!important')}개 제거 → {sys.argv[3]}")
        return
    before = read(sys.argv[3])
    after = SUMMARY.sub("", read(sys.argv[4])).rstrip("\n") + "\n"
    if strip_styles(src) != before:
        sys.exit("apply: 원고가 strip 이후 바뀌었습니다. strip부터 다시 하십시오.")
    a, b, o = before.split("\n"), after.split("\n"), src.split("\n")
    if len(a) != len(b):
        sys.exit(f"apply: 줄 수가 다릅니다({len(a)} → {len(b)}). 윤문이 줄 구조를 바꿨습니다.")
    if tags(before) != tags(after):
        sys.exit("apply: 태그 구조가 바뀌었습니다. 윤문 결과를 채택하지 않습니다.")
    changed = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x == y:
            continue
        mo, my = OPEN.match(o[i]), OPEN.match(y)
        if not (mo and my):
            sys.exit(f"apply: {i + 1}번째 줄을 되붙일 수 없습니다: {y[:60]}")
        o[i] = mo.group(1) + my.group(2)
        changed += 1
    out = "\n".join(o)
    if strip_styles(out) != after:
        sys.exit("apply: 되붙인 결과가 윤문본과 다릅니다. 저장하지 않습니다.")
    io.open(post, "w", encoding="utf-8", newline="").write(out)
    print(f"apply: {changed}줄 반영, 문단 간격 스타일 {out.count('margin:0 0 20px !important')}개 유지 → {post}")


if __name__ == "__main__":
    main()
