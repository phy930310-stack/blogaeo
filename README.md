# blogaeo — AEO 블로그 자동 작성

키워드 하나로 AEO(답변 엔진 최적화) 기준 블로그 원고를 생성합니다.

## 사용법
1. `brand/profile.md` 빈칸 입력 (최초 1회)
2. Claude Code에서 `/aeo-blog 키워드` 또는 "OOO 키워드로 블로그 써줘"
3. `posts/날짜_슬러그/` 의 `naver.md`, `tistory.html`, `images/*.png`, `report.md` 확인
4. 이미지 수정 시: `images/src/*.html` 수정 후 `node .claude/skills/aeo-blog/scripts/render.mjs posts/<폴더>/images`

## 문서
- `docs/01_AEO_리서치_요약.md` — AEO 개념·원칙 (PDF + 외부 조사)
- `docs/02_자동화_파이프라인_개요.md` — 키워드 → 원고 7단계 설계
- `.claude/skills/aeo-blog/` — 자동 작성 스킬과 템플릿
