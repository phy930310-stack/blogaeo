# blogaeo — AEO 블로그 자동 작성

키워드 하나로 AEO(답변 엔진 최적화) 기준 블로그 원고를 생성합니다.

## 사용법
1. `brand/profile.md` 빈칸 입력 (최초 1회)
2. Claude Code에서 `/aeo-blog 키워드` 또는 "OOO 키워드로 블로그 써줘"
3. 작업이 끝나면 대화창에 zip 파일이 올라옵니다 → 다운로드 후 원하는 폴더에 압축 해제
4. 같은 내용은 GitHub `posts/날짜_슬러그/` 에도 보관됩니다: `네이버_본문.txt`, `티스토리_본문.html`, `images/*.png`, `작업보고서.md` 확인
5. 발행 후 "이 주소 점검해줘 + 티스토리/네이버 URL" → PC·모바일 화면과 누락 항목을 자동 점검
6. 이미지 수정 시: `images/src/*.html` 수정 후 `node .claude/skills/aeo-blog/scripts/render.mjs posts/<폴더>/images`

## 문서
- `docs/01_AEO_리서치_요약.md` — AEO 개념·원칙 (PDF + 외부 조사)
- `docs/02_자동화_파이프라인_개요.md` — 키워드 → 원고 7단계 설계
- `.claude/skills/aeo-blog/` — 자동 작성 스킬과 템플릿
