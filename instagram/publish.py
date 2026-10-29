"""인스타그램 공식 API로 게시물을 올린다.

2026-10-29부터: Meta 앱 sbs-daejeon-sns의 **Unified Login(통합 로그인) 시스템 사용자 액세스 토큰(SUAT)** 을 쓴다.
  - 호스트는 graph.facebook.com, 대상은 Instagram 사용자 ID(IG_USER_ID = 17841441907625937, @sbs_game_daejeon).
  - SUAT는 만료되지 않으므로 refresh가 필요 없다(만료 시에는 API_설정.md 4번대로 '토큰 생성'을 다시 누른다).
  - 토큰에 포함된 권한: instagram_basic, instagram_content_publish, instagram_manage_comments, instagram_manage_messages, ads_*
  - graph.instagram.com(Instagram Login 방식)에는 이 토큰이 통하지 않는다("Cannot parse access token").

필요: 환경 변수 INSTAGRAM_ACCESS_TOKEN — 대화창·파일·커밋에 쓰지 않고 사용자 환경 변수(API_설정.md 5-B)에만 넣는다.

사용:
  python instagram/publish.py check                 # 토큰·계정·남은 게시 한도 확인
  python instagram/publish.py jpg 02                # v2_02_*.png → assets/jpg/v2_02_*.jpg (API는 JPEG만 받는다)
  python instagram/publish.py post 02 --dry-run     # 올릴 이미지 주소·캡션만 출력
  python instagram/publish.py post 02               # 실제 게시
  python instagram/publish.py refresh               # (SUAT는 만료 없음 → 안내만 출력)
  python instagram/publish.py reel 01 --dry-run     # 릴스: instagram/reels/r01_*.mp4 + reels/README.md 캡션
  python instagram/publish.py reel 01               # 릴스 게시(REELS 컨테이너 → 처리 대기 → 발행)

이미지는 공개 저장소의 고정 커밋 주소(raw.githubusercontent.com)로 넘긴다. 그래서 게시 전에
instagram/assets/jpg/ 의 파일이 커밋·push되어 있어야 한다(커밋 해시를 --ref 로 지정, 기본 = 현재 HEAD).
2026-10-28부터 디자인 기준은 v2(frontend-design)다: assets/jpg/v2_NN_*.jpg 가 있으면 그것을, 없으면 예전 이름(게시물_NN/캐러셀_NN)을 쓴다.
로컬 PC에서는 토큰을 사용자 환경 변수 INSTAGRAM_ACCESS_TOKEN 에 넣는다(API_설정.md 5-B).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://graph.facebook.com/v23.0"
IG_USER_ID = os.environ.get("INSTAGRAM_USER_ID", "17841441907625937")  # @sbs_game_daejeon
ROOT = Path(__file__).resolve().parent
REPO_RAW = "https://raw.githubusercontent.com/phy930310-stack/blogaeo"


def token():
    t = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    if not t:
        sys.exit("INSTAGRAM_ACCESS_TOKEN 이 없습니다. API_설정.md 5번(클라우드) 또는 5-B(로컬 PC)대로 넣고 새 세션에서 실행하세요.")
    return t


def call(method, path, **params):
    params["access_token"] = token()
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{API}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{API}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        body = re.sub(r"access_token=[^&\"]+", "access_token=***", body)
        sys.exit(f"API 오류 {e.code}: {body}")


def captions(readme=None):
    """README.md 의 '**NN 제목**' (릴스는 '**rNN 제목**') 다음 코드블록을 캡션으로 읽는다."""
    text = (readme or ROOT / "README.md").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"\*\*(r?\d{2}) [^*]+\*\*\n```\n(.*?)\n```", text, re.S):
        out[m.group(1)] = m.group(2)
    return out


def images(key, ref):
    jpg = ROOT / "assets" / "jpg"
    files = sorted(jpg.glob(f"v2_{key}_*.jpg"))
    if not files:
        files = sorted(jpg.glob(f"게시물_{key}_*.jpg")) + sorted(jpg.glob(f"캐러셀_{key}_*.jpg"))
    if not files:
        sys.exit(f"{key} 이미지가 없습니다: instagram/assets/jpg/")
    base = f"{REPO_RAW}/{ref}/instagram/assets/jpg/"
    return [base + urllib.parse.quote(f.name) for f in files]


def to_jpg(key):
    """v2_NN_MM.png → assets/jpg/v2_NN_MM.jpg (품질 92, sRGB). 바뀐 파일은 커밋·push해야 API가 받을 수 있다."""
    from PIL import Image  # Pillow
    src = sorted((ROOT / "assets").glob(f"v2_{key}_*.png"))
    if not src:
        sys.exit(f"instagram/assets/v2_{key}_*.png 이 없습니다. build_carousels_v2.py 와 render.mjs 를 먼저 실행하세요.")
    out = ROOT / "assets" / "jpg"
    out.mkdir(exist_ok=True)
    for p in src:
        Image.open(p).convert("RGB").save(out / (p.stem + ".jpg"), "JPEG", quality=92, optimize=True)
        print("jpg", out / (p.stem + ".jpg"))


def wait_ready(cid):
    for _ in range(30):
        st = call("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"컨테이너 {cid} 상태: {st}")
        time.sleep(3)
    sys.exit(f"컨테이너 {cid} 준비 시간 초과")


def post(key, ref, dry):
    urls = images(key, ref)
    cap = captions().get(key)
    if not cap:
        sys.exit(f"README.md 에 {key} 캡션이 없습니다.")
    print(f"이미지 {len(urls)}장\n" + "\n".join(urls) + f"\n\n캡션:\n{cap}")
    if dry:
        return
    for u in urls:  # 게시 전에 주소가 열리는지 확인
        with urllib.request.urlopen(u, timeout=30) as r:
            if r.status != 200:
                sys.exit(f"이미지 주소 오류 {r.status}: {u}")
    me = call("GET", IG_USER_ID, fields="id,username")
    uid = me["id"]
    if len(urls) == 1:
        cid = call("POST", f"{uid}/media", image_url=urls[0], caption=cap)["id"]
    else:
        kids = [call("POST", f"{uid}/media", image_url=u, is_carousel_item="true")["id"] for u in urls]
        for k in kids:
            wait_ready(k)
        cid = call("POST", f"{uid}/media", media_type="CAROUSEL", children=",".join(kids), caption=cap)["id"]
    wait_ready(cid)
    mid = call("POST", f"{uid}/media_publish", creation_id=cid)["id"]
    link = call("GET", mid, fields="permalink").get("permalink")
    print(f"\n게시 완료 @{me['username']}: {link}")


def wait_ready_long(cid, minutes=10):
    """릴스는 영상 처리에 몇 분 걸린다. IN_PROGRESS 동안 기다린다."""
    for _ in range(minutes * 6):
        st = call("GET", cid, fields="status_code,status").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"릴스 컨테이너 {cid} 상태: {st}")
        time.sleep(10)
    sys.exit(f"릴스 컨테이너 {cid} 처리 시간 초과({minutes}분)")


def reel(key, ref, dry):
    """instagram/reels/rNN_*.mp4 를 공개 raw 주소로 넘겨 릴스로 올린다 (media_type=REELS)."""
    files = sorted((ROOT / "reels").glob(f"r{key}_*.mp4"))
    if len(files) != 1:
        sys.exit(f"instagram/reels/r{key}_*.mp4 가 {len(files)}개입니다(1개여야 함).")
    cap = captions(ROOT / "reels" / "README.md").get(f"r{key}")
    if not cap:
        sys.exit(f"instagram/reels/README.md 에 r{key} 캡션이 없습니다.")
    url = f"{REPO_RAW}/{ref}/instagram/reels/" + urllib.parse.quote(files[0].name)
    print(f"영상: {url}\n\n캡션:\n{cap}")
    if dry:
        return
    with urllib.request.urlopen(url, timeout=60) as r:  # 게시 전에 주소가 열리는지 확인
        if r.status != 200:
            sys.exit(f"영상 주소 오류 {r.status}: {url}")
    me = call("GET", IG_USER_ID, fields="id,username")
    cid = call("POST", f"{me['id']}/media", media_type="REELS", video_url=url, caption=cap, share_to_feed="true")["id"]
    print(f"컨테이너 {cid} 생성, 영상 처리 대기 …")
    wait_ready_long(cid)
    mid = call("POST", f"{me['id']}/media_publish", creation_id=cid)["id"]
    link = call("GET", mid, fields="permalink").get("permalink")
    print(f"\n릴스 게시 완료 @{me['username']}: {link}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "jpg", "post", "refresh", "reel"])
    ap.add_argument("key", nargs="?")
    ap.add_argument("--ref", default=None, help="이미지를 가져올 커밋 해시(기본: 현재 HEAD)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd == "check":
        me = call("GET", IG_USER_ID, fields="id,username,media_count,followers_count")
        lim = call("GET", f"{me['id']}/content_publishing_limit", fields="quota_usage,config")
        print(json.dumps({"account": me, "publishing_limit": lim}, ensure_ascii=False, indent=2))
    elif a.cmd == "jpg":
        if not a.key:
            sys.exit("게시물 번호를 지정하세요. 예: jpg 02")
        to_jpg(a.key)
    elif a.cmd == "post":
        if not a.key:
            sys.exit("게시물 번호를 지정하세요. 예: post 03")
        ref = a.ref or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        post(a.key, ref, a.dry_run)
    elif a.cmd == "reel":
        if not a.key:
            sys.exit("릴스 번호를 지정하세요. 예: reel 01")
        ref = a.ref or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        reel(a.key, ref, a.dry_run)
    else:
        print("현재 토큰은 시스템 사용자 액세스 토큰(SUAT)으로 만료되지 않습니다. 갱신이 필요 없습니다. "
              "권한 오류(#190)가 나면 API_설정.md 4번대로 Meta 앱 대시보드에서 '토큰 생성'을 다시 눌러 환경 변수를 교체하세요.")


if __name__ == "__main__":
    main()
