# 인스타그램 공식 API 설정 (자동 업로드용, 처음 한 번)

이 설정을 마치면 클라우드 세션이 `instagram/publish.py`로 @sbs_game_daejeon에 카드뉴스를 직접 올린다. 회사 PC가 꺼져 있어도 된다.

- 방식: **Instagram API with Instagram Login** (Business Login for Instagram). 페이스북 페이지 연결은 필요 없다.
- 필요 권한: `instagram_business_basic`, `instagram_business_content_publish`
- 한도: 24시간 동안 API로 100건까지 올릴 수 있다. 카드뉴스 1개는 1건으로 센다(공식 문서).
- 못 하는 것: 게시물 고정, 하이라이트, 프로필 링크 편집 → 휴대폰 앱에서 한다.
- Meta 화면의 메뉴 이름은 자주 바뀐다. 아래와 다르면 화면을 캡처해서 보여 주면 Claude가 다시 안내한다.

---

## 0. 준비물
- PC 브라우저 (휴대폰보다 PC가 편하다)
- **페이스북 계정**(개인 계정이어도 된다). Meta 개발자 등록에 필요하다. 이 계정이 앱 관리자가 된다.
- 인스타그램 @sbs_game_daejeon 로그인 정보
- @sbs_game_daejeon이 **비즈니스(프로페셔널) 계정**일 것 → 2026-10-24에 전환 완료

## 1. Meta 개발자 등록 (약 5분, 처음 한 번)
개발자 사이트에서 휴대폰 인증 문자가 안 오는 일이 잦다(2026-10-27 실제로 막힘). **페이스북 본계정에 번호를 먼저 등록**하면 개발자 등록 때 인증을 건너뛰는 경우가 많다.
1. facebook.com 로그인 → 프로필 사진 → **설정 및 개인정보** → **설정** → **계정 센터** → **개인정보** → **연락처 정보** → **휴대폰 번호 추가**
   - 국가 `대한민국(+82)`, 번호는 0 포함·하이픈 없이(`010…`)
   - 문자가 안 오면: 스팸 문자함 확인 → 2분 뒤 재전송 1회 → 그래도 안 오면 **이메일 인증**으로 바꿔 진행(이메일만으로도 등록된다) → 다른 번호 → 다음 날 재시도
2. https://developers.facebook.com → **시작하기** → 약관 동의 → (인증을 다시 물으면 등록한 번호 선택) → 직업은 아무거나
3. 상단 **내 앱**(My Apps)이 보이면 등록 완료

## 2. 앱 만들기 (약 3분)
1. **내 앱** → **앱 만들기**(Create App)
2. 앱 이름: `sbs-daejeon-insta` (아무 이름이나 된다. 단 'Instagram', 'IG' 같은 단어는 넣을 수 없다)
3. 앱 연락처 이메일: 대표님 이메일
4. **사용 사례**(Use case): **Instagram에서 메시지 및 콘텐츠 관리**(Manage messaging & content on Instagram)를 고른다.
5. 비즈니스 포트폴리오 연결을 물으면 **나중에** 또는 **연결 안 함**을 고른다.
6. **앱 만들기** → 비밀번호를 다시 확인하면 앱 대시보드가 열린다.

## 3. 학원 인스타 계정을 앱에 연결 (약 5분)
> 왼쪽 메뉴에 **Instagram** 항목이 바로 보이면 그 안의 'API 설정(Instagram 로그인 포함)' 화면에 **테스터 추가 / 계정 추가** 버튼이 있다. 그 버튼으로 바로 추가해도 된다(아래 1번 대신).
> 초대 수락·계정 추가 때는 반드시 **@sbs_game_daejeon으로 로그인된 상태**여야 한다. 개인 계정과 연결돼 있어 개인 계정이 먼저 뜰 수 있다.
앱은 지금 **개발 모드**다. 개발 모드에서는 앱에 '역할'이 있는 계정에만 글을 올릴 수 있다. 우리는 학원 계정 하나에만 올리면 되므로 이 상태로 충분하고, 앱 심사도 필요 없다.

1. 왼쪽 메뉴 **앱 역할**(App roles) → **역할**(Roles) → **사람 추가**(Add People) → **Instagram 테스터**(Instagram Tester) → `sbs_game_daejeon` 입력 → 추가
2. 인스타그램에서 초대를 수락한다.
   - PC: https://www.instagram.com/accounts/manage_access/ → **테스터 초대**(Tester Invites) 탭 → **수락**
   - 메뉴가 안 보이면 인스타그램 앱 → 설정 → 웹사이트 권한 → 앱 및 웹사이트 → 테스터 초대
   - 이 메뉴가 아예 없으면 3번은 건너뛰고 4번으로 간다. 4번의 '계정 추가'에서 바로 연결될 수 있다.

## 4. 액세스 토큰 발급 (약 3분)
1. 왼쪽 메뉴 **사용 사례**(Use cases) → Instagram 사용 사례의 **맞춤 설정**(Customize)
2. **Instagram 로그인을 통한 API 설정**(API setup with Instagram login)
3. **권한**(Permissions) 항목에서 `instagram_business_basic`, `instagram_business_content_publish`가 있는지 확인한다. 없으면 **추가**한다.
4. **액세스 토큰 생성**(Generate access tokens) → **계정 추가**(Add account) → @sbs_game_daejeon으로 로그인 → 권한 허용
5. 계정 옆 **토큰 생성**(Generate token) → 나온 긴 문자열을 **복사**한다.
   - 이것이 **장기 토큰**이다. 약 60일 동안 유효하다.
   - **절대 대화창, 카톡, 메일에 붙여 넣지 마십시오.** 바로 아래 5번 위치에만 넣는다.

## 5. 클라우드 환경에 토큰 넣기 (약 2분)
1. Claude 앱에서 이 세션 상단 제목 표시줄의 **환경 이름**(클라우드 환경 메뉴) → **Edit**
2. **Network secrets**(앱 버전에 따라 'API credentials')가 있으면 그곳에, 없으면 **환경 변수**(Environment variables)에 추가한다.
   - 이름: `INSTAGRAM_ACCESS_TOKEN`
   - 값: 4-5에서 복사한 토큰
3. **저장**한다.
4. **새 세션**을 열고 "인스타 API 확인해줘"라고 말하면 Claude가 `python3 instagram/publish.py check`로 연결을 확인한다. 토큰은 새 세션부터 적용된다.

## 5-B. 로컬 PC(회사 PC 세션)에 토큰 넣기 (약 2분) — 2026-10-28부터 이쪽이 기본
1. 시작 메뉴에서 **환경 변수**를 검색 → **계정의 환경 변수 편집** → **사용자 변수** → **새로 만들기**
   - 변수 이름: `INSTAGRAM_ACCESS_TOKEN`
   - 변수 값: 4-5에서 복사한 토큰
2. **확인**으로 닫는다. Claude 앱을 완전히 종료했다가 다시 연다(새로 연 세션부터 변수가 보인다).
3. 새 세션에서 "인스타 API 확인해줘" → `python instagram/publish.py check`
   - 토큰 값은 대화·파일·커밋에 쓰지 않는다. 저장소는 공개다.

## 6. 이후 사용
- 올리기: "인스타에 02 올려줘" → Claude가 `publish.py jpg 02`(JPEG 변환) → 커밋·push → `publish.py post 02 --dry-run`으로 이미지·캡션 확인 → 사용자 확인 후 `post 02`.
  - 캡션 문구는 올리기 전에 텍스트로 먼저 합의한다(2026-10-28 사용자 규칙).
  - 먼저 `--dry-run`으로 이미지와 캡션을 보여 드린 뒤 실제로 올린다.
- 고정, 하이라이트, 링크 편집은 계속 휴대폰 앱에서 한다.

## 7. 토큰 만료 관리 (60일)
- 만료되기 전에 "인스타 토큰 갱신해줘"라고 하면 `publish.py refresh`로 연장한다.
- 갱신 결과 새 토큰 값이 나오면 5번 위치의 값을 교체해야 할 수 있다. 이 부분은 확인하지 못했다(추정).
- 이미 만료됐다면 4번부터 다시 하면 된다(약 5분).
- 첫 발급일을 `brand/channels.md`에 기록해 두고, 50일쯤 지나면 갱신한다.

## 문제 해결
| 증상 | 해결 |
|---|---|
| 4번에 '계정 추가'가 안 보임 | 2-4의 사용 사례가 Instagram인지 확인. 다르면 앱을 새로 만든다 |
| 계정 추가 시 "비즈니스 계정이 아님" | 인스타그램 앱 → 설정 → 계정 유형 → 프로페셔널(비즈니스)인지 확인 |
| 게시할 때 권한 오류(#10, #200) | 4-3 권한에 `instagram_business_content_publish`가 있는지 확인 → 토큰을 다시 발급 |
| 이미지 오류 | Claude가 처리한다(이미지는 JPEG, 공개 주소로 넘김) |

## 참고 (Meta 공식 문서)
- [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/)
- [Create an App](https://developers.facebook.com/docs/instagram-platform/create-an-instagram-app/)
- [Publish Content (게시·카드뉴스·한도)](https://developers.facebook.com/docs/instagram-platform/content-publishing/)
- [Access Token](https://developers.facebook.com/docs/instagram-platform/reference/access_token/)
