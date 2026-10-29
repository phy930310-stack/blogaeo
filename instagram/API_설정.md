# 인스타그램 공식 API 설정 (자동 업로드용)

> **2026-10-29 완료.** 아래는 실제로 성공한 경로를 기준으로 다시 쓴 것이다. 토큰은 회사 PC의 사용자 환경 변수 `INSTAGRAM_ACCESS_TOKEN`에 들어 있고, `python instagram/publish.py check`가 @sbs_game_daejeon(IG 사용자 ID 17841441907625937)을 정상 반환했다. 다시 발급할 일이 생기면 **4번**만 하면 된다.

이 설정이 되어 있으면 Claude 세션이 `instagram/publish.py`로 @sbs_game_daejeon에 카드뉴스를 직접 올린다.

- 방식: **Instagram API — Unified Login(통합 로그인)**, 토큰 종류는 **시스템 사용자 액세스 토큰(SUAT), 만료 없음**. 호스트는 `graph.facebook.com`.
  - 2026-10-29 기준 새로 만든 Meta 앱에는 "Instagram 로그인이 포함된 API 설정"(Instagram Login 방식)이 **없다**. 대시보드 공지: "최신 앱에서는 Instagram 로그인이 포함된 API 설정을 사용할 수 없습니다. 대신 앱이 통합된 로그인이 포함된 API 설정을 사용합니다." 그래서 `graph.instagram.com` 기준으로 쓴 예전 안내는 폐기했다.
  - Unified Login은 **앱이 비즈니스 포트폴리오 소유**여야 탭이 생긴다. 페이스북 페이지는 필요 없다.
- 권한(구성에 포함): `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_messages`, `ads_management`, `ads_read`
- 한도: 24시간 동안 API로 100건(카드뉴스 1개 = 1건). `check`가 `quota_usage`로 보여 준다.
- 못 하는 것: 게시물 고정, 하이라이트, 프로필 링크 편집 → 휴대폰 앱에서 한다.
- Meta 화면의 메뉴 이름은 자주 바뀐다. 아래와 다르면 화면을 캡처해서 보여 주면 Claude가 다시 안내한다.

## 만들어 둔 것 (2026-10-29)
| 항목 | 값 |
|---|---|
| Meta 앱 | `sbs-daejeon-sns` (앱 ID 28650853597918421). 이름에 insta/gram/FB/face/book 금지 → `sbs-daejeon-insta`는 거부됨 |
| 이용 사례 | Instagram에서 메시지 및 콘텐츠 관리 |
| 비즈니스 포트폴리오 | `SBS Game Academy Daejeon` (business_id 4428357544080766). 한글 이름은 거부됨 |
| Unified Login 구성 | `Instagram API (Unified Login)` 구성 ID 1921541615878493, 템플릿으로 생성 |
| Instagram 테스터 | sbs_game_daejeon, 2026-10-29 초대 수락(앱 표시명 sbs-daejeon-sns-IG) |
| 포트폴리오의 Instagram 계정 | @sbs_game_daejeon (IG 사용자 ID 17841441907625937) |
| 광고 계정 | 토큰 팝업에서 만들었다면 KRW · Asia/Seoul. 유료 광고는 하지 않으므로 사용하지 않음 |
| 앱 연락처 이메일 | 사용자 지메일 |

---

## 0. 준비물
- PC 브라우저(Chrome). Claude in Chrome이 대부분 대신 누를 수 있지만 **로그인·비밀번호 재입력·SMS 인증 코드는 사용자가 직접** 입력한다.
- **페이스북 계정**(개인 계정). Meta 개발자 등록과 앱 관리자용.
- @sbs_game_daejeon 로그인 정보. **비즈니스(프로페셔널) 계정**이어야 한다(2026-10-24 전환 완료).

## 1. Meta 개발자 등록 (처음 한 번) — 완료
- https://developers.facebook.com → 시작하기 → 약관 동의 → **SMS 인증 필수**(이메일 인증 없음, 번호 변경만 가능).
- 2026-10-27·28에는 문자가 오지 않아 두 번 실패했고, 2026-10-29에 문자가 와서 통과했다. 계정 센터에 번호가 등록돼 있어도 이 단계는 별도 SMS를 요구한다. 안 오면 하루 뒤 다른 시간대에 1회만 재전송한다(추정: 해외 발신 문자 차단 영향).

## 2. 앱 만들기 — 완료
1. **내 앱** → **앱 만들기**
2. 앱 이름: `sbs-daejeon-sns`. **insta / gram / FB / face / book 이 들어가면 거부**된다.
3. 앱 연락처 이메일: 사용자 지메일(칸에 전화번호가 미리 들어가 있으면 '다음'이 비활성이므로 지우고 입력)
4. **사용 사례**: **Instagram에서 메시지 및 콘텐츠 관리**
5. 비즈니스 포트폴리오: 이 단계에서는 건너뛰어도 되지만, 결국 **3번에서 연결해야** 한다.
6. **앱 만들기** → 비밀번호 재입력(사용자) → 대시보드.

## 3. 비즈니스 포트폴리오 만들고 앱·인스타 계정 연결 — 완료
Unified Login 탭("API setup with Unified login")은 앱이 비즈니스 포트폴리오에 속해야 나타난다.
1. https://business.facebook.com → 포트폴리오 만들기. 이름은 **영문**(`SBS Game Academy Daejeon`). 한글 이름은 거부됐다. 웹사이트를 물으면 `http://sbsdaejeon-game.co.kr/`.
2. Business Suite **설정 → 계정 → 앱 → 추가 → 앱 ID 연결**(28650853597918421). 운영자이므로 자동 승인.
3. **설정 → 계정 → Instagram 계정 → 추가 → Instagram 계정 추가** → 팝업에서 @sbs_game_daejeon 로그인(사용자) → 완료. "사람 리스트에 추가" 제안은 건너뛴다.
   - 이걸 안 하면 토큰 팝업에서 "Instagram Pro 계정이 필요합니다"가 뜨고 계정이 목록에 없다.
4. 기존 페이스북 페이지(학원과 무관한 것)는 포트폴리오에 넣지 않는다.

## 4. 액세스 토큰 발급 — 완료, 재발급 시 여기부터
앱 대시보드 → 왼쪽 **이용 사례** → Instagram의 **맞춤 설정** → 탭 **API setup with Unified login**.
1. **1. 앱 구성**: 구성이 없으면 **새로운 구성 만들기 → Create from template** → `Instagram API (Unified Login)`이 생긴다(SUAT, 만료 없음, 권한 6개). 구성이 선택돼 있어야 다음 단계가 된다("먼저 1단계에서 구성을 선택하세요" 오류의 원인).
   - 별도로 **권한 및 기능** 탭에 `instagram_business_basic`, `instagram_business_content_publish`를 추가해 두었다(테스트 준비 완료 상태). 실제 토큰에 들어간 권한은 구성 쪽 목록이다.
2. **앱 역할 → 역할 → 사람 추가 → Instagram 테스터 → `sbs_game_daejeon`** → 인스타그램 https://www.instagram.com/accounts/manage_access/ → **테스터 초대** 탭 → 수락(@sbs_game_daejeon으로 로그인된 상태).
3. **2. 액세스 토큰 생성** 표에서 `sbs_game_daejeon` 행의 **토큰 생성**.
   - **팝업 창이 따로 뜬다.** 비즈니스 포트폴리오 `SBS Game Academy Daejeon`, Instagram 계정 `@sbs_game_daejeon`, 광고 계정은 가능하면 선택 안 함(만들어야 하면 이름 `SBS Game Academy Daejeon`, 통화 KRW, 시간대 Asia/Seoul. 통화·시간대는 나중에 못 바꾼다) → 다음 → 허용.
   - **팝업이 닫히면 토큰 창은 원래 대시보드 탭에 뜬다.** 그 사이에 대시보드 탭을 다른 페이지로 옮기면 토큰 창이 사라진다(2026-10-29 한 번 놓쳤다). 탭을 그대로 둔다.
4. 토큰 창의 **복사** 버튼만 누른다. 화면에 띄우거나 대화·카톡·메일·파일에 붙여 넣지 않는다. 바로 5-B로 간다.

## 5. 클라우드 환경에 토큰 넣기 (클라우드 세션을 쓸 때만)
1. Claude 앱에서 세션 상단의 **환경 이름**(클라우드 환경 메뉴) → **Edit**
2. **Network secrets**(없으면 **환경 변수**)에 `INSTAGRAM_ACCESS_TOKEN` 추가 → 저장
3. **새 세션**에서 "인스타 API 확인해줘" → `python3 instagram/publish.py check`

## 5-B. 로컬 PC(회사 PC 세션)에 토큰 넣기 — 2026-10-29 이 방식으로 저장 완료
Claude 세션이 있으면 **값을 보지 않고** 클립보드에서 바로 넣는다(토큰 창에서 복사 → "복사했어"):
```powershell
[Environment]::SetEnvironmentVariable('INSTAGRAM_ACCESS_TOKEN', (Get-Clipboard -Raw).Trim(), 'User'); Set-Clipboard -Value ' '
```
수동으로 할 때: 시작 메뉴 **환경 변수** 검색 → **계정의 환경 변수 편집** → 사용자 변수 **새로 만들기** → 이름 `INSTAGRAM_ACCESS_TOKEN`, 값 붙여넣기 → 확인.
- 새로 넣은 변수는 **Claude 앱을 완전히 종료했다가 다시 연 뒤의 새 세션**부터 보인다. 같은 세션에서 바로 쓰려면 PowerShell에서 `$env:INSTAGRAM_ACCESS_TOKEN = [Environment]::GetEnvironmentVariable('INSTAGRAM_ACCESS_TOKEN','User')` 뒤에 실행한다.
- 확인: `python instagram/publish.py check` → `username: sbs_game_daejeon`, `quota_total: 100`이 나오면 정상.
- 토큰 값은 대화·파일·커밋에 쓰지 않는다. 저장소는 공개다.

## 6. 이후 사용
- 올리기: "인스타에 02 올려줘" → Claude가 `publish.py jpg 02`(JPEG 변환) → 커밋·push → `publish.py post 02 --dry-run`으로 이미지·캡션 확인 → 사용자 확인 후 `post 02`.
  - 캡션 문구는 올리기 전에 텍스트로 먼저 합의한다(2026-10-28 사용자 규칙).
  - 이미지는 공개 저장소의 고정 커밋 주소로 넘기므로 push가 먼저다.
- 고정, 하이라이트, 링크 편집은 계속 휴대폰 앱에서 한다.

## 7. 토큰 만료 관리
- 지금 토큰은 **SUAT라 만료되지 않는다.** `publish.py refresh`는 안내만 출력한다.
- 권한 오류(#190, "Invalid OAuth access token")가 나면 4번 3·4 → 5-B로 다시 발급한다(약 3분). 앱 대시보드에서 토큰을 **해제**하거나 포트폴리오에서 앱·계정을 떼면 토큰이 죽는다.
- 앱은 **개발 모드**다. 역할이 있는 계정(@sbs_game_daejeon)에만 올릴 수 있고, 그게 전부이므로 앱 검수는 하지 않는다.

## 문제 해결
| 증상 | 해결 |
|---|---|
| "Instagram 로그인이 포함된 API 설정" 탭이 없음 | 정상(신규 앱). Unified Login 탭을 쓴다. 탭이 없으면 3번(포트폴리오 연결) |
| 토큰 팝업에 "Instagram Pro 계정이 필요합니다" | 3-3(포트폴리오에 Instagram 계정 추가)이 안 된 것 |
| "먼저 1단계에서 구성을 선택하세요" | 4-1 구성 생성·선택 |
| 팝업은 끝났는데 토큰 창이 없음 | 대시보드 탭이 이동됐음. 탭을 Unified Login 페이지에 둔 채 토큰 생성 재클릭 |
| `check`에서 "Cannot parse access token" | `graph.instagram.com`으로 보낸 것. publish.py는 `graph.facebook.com`을 써야 한다 |
| 게시할 때 권한 오류(#10, #200) | 구성 권한에 `instagram_content_publish`가 있는지 확인 → 토큰 재발급 |
| 이미지 오류 | Claude가 처리한다(JPEG, 공개 주소, push 여부) |

## 참고 (Meta 공식 문서)
- [Instagram Platform 개요 · Unified Login](https://developers.facebook.com/docs/instagram-platform/)
- [Create an App](https://developers.facebook.com/docs/instagram-platform/create-an-instagram-app/)
- [Publish Content (게시·카드뉴스·한도)](https://developers.facebook.com/docs/instagram-platform/content-publishing/)
