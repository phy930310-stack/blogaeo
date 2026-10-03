"""네이버 검색광고 키워드도구 엑셀(전체 다운로드)을 합쳐 우리 학원 관련 키워드만 질문군별로 정리한다.
사용: python3 .claude/skills/aeo-blog/scripts/keywords.py   (keywords/raw/*.xlsx → keywords/backlog.csv, keywords/backlog.md)
- 같은 키워드는 가장 최근 파일 값을 사용
- '< 10' 은 5로 계산
- 이미 쓴 키워드는 keywords/used.csv(키워드,작성일,글폴더)에 적으면 '완료'로 표시
"""
import csv, glob, math, os, re, sys
try:
    import openpyxl
except ImportError:
    sys.exit("pip install openpyxl 후 다시 실행하세요")

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "../../../.."))
KW = os.path.join(REPO, "keywords")

# 질문군(카테고리): (이름, 우선도 가중치, 포함 패턴)
GROUPS = [
    ("A. 게임학과·입시", 1.0, r"게임.*(학과|대학|고등학교|입시|전공)|(학과|입시|실기|포트폴리오).*게임|청강|게임고|게임포트폴리오|게임실기|게임입시"),
    ("B. 게임원화·그림", 1.0, r"원화|컨셉아트|게임일러스트|게임캐릭터|캐릭터(디자인|일러스트|드로잉|원화)|인체드로잉|디지털드로잉학원|일러스트(학원|레이터학원)"),
    ("C. 3D·모델링", 0.9, r"블렌더|BLENDER|지브러쉬|ZBRUSH|3D|3DS?MAX|맥스|마야|MAYA|모델링|리깅|서브스턴스|노마드스컬프"),
    ("D. 게임기획·개발", 0.9, r"게임(기획|개발|프로그래|만들기|엔진|디자이너|그래픽)|UNITY|유니티|언리얼|UNREAL|C\+\+|C#"),
    ("E. 게임업계 취업", 0.8, r"게임(회사|업계|QA|취업)|(넥슨|넷마블|엔씨|NC소프트|크래프톤|펄어비스|스마일게이트|카카오게임즈|네오플|컴투스|위메이드|데브시스터즈|시프트업).*(채용|연봉|취업|신입)"),
    ("F. 대전·학원", 1.0, r"대전.*(게임|미술|그림|일러스트|웹툰|컴퓨터|코딩|국비|디자인|애니|3D)|둔산.*(학원|미술)|게임학원|게임아카데미"),
]
EXCLUDE = r"^(서울|부산|대구|인천|강남|분당|일산|부평|서면|성남|광주|수원|울산|홍대|신촌|노원|안양|부천|경기|창원|평택)|인테리어|인디자인|컴활|컴퓨터활용|성인미술|웹디자인|프린터|캐드|CAD|클로3D|3D클로|3D영상|챗|GPT|롤$|롤게임|DART|엑셀|국민취업|국취|프로게이머|E스포츠|이스포츠|대회|발로란트|오버워치|배틀그라운드|먹방|공모전$"

def num(v):
    if v in (None, ""):
        return 0.0
    s = str(v).replace(",", "").strip()
    if s.startswith("<"):
        return 5.0
    try:
        return float(s)
    except ValueError:
        return 0.0

def load():
    rows = {}
    for f in sorted(glob.glob(os.path.join(KW, "raw", "*.xlsx"))):  # 파일명 날짜순 → 최신 값이 덮어씀
        ws = openpyxl.load_workbook(f, read_only=True).worksheets[0]
        for r in list(ws.iter_rows(values_only=True))[2:]:
            if not r or not r[0]:
                continue
            k = str(r[0]).strip()
            rows[k] = dict(keyword=k, pc=num(r[1]), mobile=num(r[2]), total=num(r[1]) + num(r[2]),
                           competition=r[7] or "", ads=num(r[8]), source=os.path.basename(f))
    return rows

def main():
    rows = load()
    used = {}
    up = os.path.join(KW, "used.csv")
    if os.path.exists(up):
        for r in csv.DictReader(open(up, encoding="utf-8")):
            used[r["키워드"].replace(" ", "")] = r.get("작성일", "")
    out = []
    for k, r in rows.items():
        ku = k.upper()
        if re.search(EXCLUDE, ku):
            continue
        for name, w, pat in GROUPS:
            if re.search(pat, ku):
                r["group"] = name
                # 점수: 검색량(로그) × 질문군 가중치 × 모바일 비중 보정(모바일 위주 = 블로그 소비층)
                mob = r["mobile"] / r["total"] if r["total"] else 0
                r["score"] = round(math.log10(r["total"] + 1) * w * (0.8 + 0.4 * mob), 2)
                r["status"] = "완료(" + used[k.replace(" ", "")] + ")" if k.replace(" ", "") in used else ""
                out.append(r)
                break
    out.sort(key=lambda r: (r["group"], -r["total"]))
    with open(os.path.join(KW, "backlog.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["질문군", "키워드", "월검색(합)", "PC", "모바일", "광고경쟁", "점수", "상태"])
        for r in out:
            w.writerow([r["group"], r["keyword"], int(r["total"]), int(r["pc"]), int(r["mobile"]), r["competition"], r["score"], r["status"]])
    with open(os.path.join(KW, "backlog.md"), "w", encoding="utf-8") as f:
        f.write(f"# 키워드 백로그\n\n원본: keywords/raw/ ({len(rows)}개 중 관련 {len(out)}개)\n\n")
        for name, _, _ in GROUPS:
            g = [r for r in out if r["group"] == name]
            f.write(f"## {name} ({len(g)}개, 월 검색 합계 {int(sum(r['total'] for r in g)):,})\n\n| 키워드 | 월검색 | 모바일 | 광고경쟁 | 상태 |\n|---|---:|---:|---|---|\n")
            for r in g[:40]:
                f.write(f"| {r['keyword']} | {int(r['total']):,} | {int(r['mobile']):,} | {r['competition']} | {r['status']} |\n")
            f.write("\n")
    write_clusters(rows)
    print(f"전체 {len(rows)}개 → 관련 {len(out)}개 → keywords/backlog.csv, backlog.md, clusters.md")

def write_clusters(rows):
    """keywords/clusters.csv(주제 묶음 정의)의 합산 검색량을 계산해 clusters.md로 출력"""
    cp = os.path.join(KW, "clusters.csv")
    if not os.path.exists(cp):
        return
    vol = {k: r["total"] for k, r in rows.items()}
    cl = []
    for r in csv.DictReader(open(cp, encoding="utf-8")):
        ks = r["포함키워드"].split()
        cl.append(dict(r, 합산=int(sum(vol.get(k, 0) for k in ks)), ks=[k for k in ks if k in vol]))
    cl.sort(key=lambda c: (bool(c["상태"]), -c["합산"]))
    with open(os.path.join(KW, "clusters.md"), "w", encoding="utf-8") as f:
        f.write("# 주제 묶음(클러스터) 계획\n\n같은 질문에 속하는 키워드를 묶어 **글 1편(네이버+티스토리)**으로 공략합니다.\n"
                "합산 월검색 = 포함 키워드의 월간 검색수(PC+모바일) 합. 원본: keywords/raw/ (네이버 검색광고 키워드도구)\n"
                "주의: 도구·회사명 검색(블렌더3D, 넥슨채용 등)은 검색량이 커도 학원 상담 의도가 약합니다.\n\n"
                "| 순위 | 주제 | 대표 키워드 | 유형 | 합산 월검색 | 상태 |\n|---:|---|---|---|---:|---|\n")
        for i, c in enumerate(cl, 1):
            f.write(f"| {i} | {c['주제']} | {c['대표키워드']} | {c['유형']} | {c['합산']:,} | {c['상태']} |\n")
        f.write("\n## 묶음별 포함 키워드\n\n")
        for c in cl:
            f.write(f"### {c['주제']}\n" + ", ".join(f"{k}({int(vol[k])})" for k in c["ks"]) + "\n\n")

if __name__ == "__main__":
    main()
