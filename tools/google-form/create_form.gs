/**
 * SBS아카데미게임학원 대전점 — 입시·취업 상담 신청 구글 폼 생성 스크립트
 *
 * 사용법: README.md 참고. script.google.com 새 프로젝트에 이 파일 내용을 붙여 넣고
 * createConsultForm 을 한 번 실행하면 폼 + 응답 시트 + 메일 알림이 만들어진다.
 *
 * 구조(섹션 분기)
 *   1. 상담 목적 → [입시] 2-A로 / [취업] 2-B로 / [모르겠음] 3으로
 *   2-A. 입시 질문 → 끝나면 3으로
 *   2-B. 취업 질문 → 3으로
 *   3. 연락처·유입 경로·개인정보 동의 (공통)
 */

const FORM_TITLE = 'SBS아카데미게임학원 대전점 입시·취업 상담 신청';
const NOTIFY_EMAIL = 'phy930310@gmail.com';
const PHONE = '042-716-7439';

// 유입 경로 선택지 — brand/channels.md 의 목록과 동일하게 유지
const SOURCES = [
  '네이버 블로그',
  '네이버 검색·지도(플레이스)',
  '구글 검색·티스토리',
  '인스타그램',
  '유튜브',
  '카카오톡',
  '지인·선후배 추천',
  '학교·설명회',
];

function createConsultForm() {
  const props = PropertiesService.getScriptProperties();
  if (props.getProperty('FORM_ID')) {
    throw new Error('이미 폼을 만들었습니다. 다시 만들려면 프로젝트 설정 > 스크립트 속성에서 FORM_ID 를 지운 뒤 실행하세요.');
  }

  const form = FormApp.create(FORM_TITLE);
  form.setDescription(
    '게임·웹툰·웹소설 분야 입시(게임학과·웹툰학과 진학)와 취업(국비 과정·취업 포트폴리오) 상담을 신청하는 곳입니다.\n' +
    '1~2분이면 작성할 수 있어요. 남겨 주신 방법으로 상담팀이 연락드립니다.\n' +
    '급한 문의: ' + PHONE
  );
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);
  form.setConfirmationMessage(
    '신청이 접수되었습니다. 확인 후 남겨 주신 방법으로 연락드릴게요.\n' +
    '급한 문의는 ' + PHONE + ' 로 전화 주세요.'
  );

  // ── 1. 공통 시작 ──────────────────────────────
  const purpose = form.addMultipleChoiceItem()
    .setTitle('어떤 상담을 원하세요?')
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('관심 있는 과정 (여러 개 선택 가능)')
    .setChoiceValues([
      '게임기획',
      '게임프로그래밍(유니티)',
      '게임원화·일러스트·애니메이션',
      '3D 그래픽',
      '웹툰',
      '웹소설',
      '아직 모르겠어요',
    ])
    .setRequired(true);

  // ── 2-A. 입시 ────────────────────────────────
  const ipsiPage = form.addPageBreakItem()
    .setTitle('입시 상담')
    .setHelpText('게임학과·웹툰학과 진학 상담을 위한 질문입니다.');

  form.addMultipleChoiceItem()
    .setTitle('신청하시는 분')
    .setChoiceValues(['학생 본인', '학부모', '기타'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('학생 학년')
    .setChoiceValues(['중3 이하', '고1', '고2', '고3', 'N수생'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('학교 유형')
    .setChoiceValues(['일반고', '특성화고', '기타'])
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('포트폴리오 준비 상황')
    .setChoiceValues(['아직 없어요', '독학으로 조금 해 봤어요', '학원·과외로 준비 중이에요'])
    .setRequired(false);

  // ── 2-B. 취업 ────────────────────────────────
  const jobPage = form.addPageBreakItem()
    .setTitle('취업 상담')
    .setHelpText('국비 과정·취업 포트폴리오 상담을 위한 질문입니다.');

  form.addMultipleChoiceItem()
    .setTitle('현재 상황')
    .setChoiceValues(['대학생(재학·휴학)', '졸업 후 구직 중', '직장인(이직·전직 준비)', '기타'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('국민내일배움카드가 있으신가요?')
    .setChoiceValues(['있어요', '없어요', '잘 모르겠어요'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('관련 경험')
    .setChoiceValues(['처음이에요', '독학해 본 적 있어요', '관련 전공·수강 경험이 있어요'])
    .setRequired(false);

  // ── 3. 공통 마무리 ────────────────────────────
  const commonPage = form.addPageBreakItem()
    .setTitle('연락처')
    .setHelpText('상담 연락을 위해 필요한 정보입니다.');

  form.addTextItem()
    .setTitle('이름')
    .setHelpText('입시 상담은 학생 이름을 적어 주세요.')
    .setRequired(true);

  const phoneRule = FormApp.createTextValidation()
    .requireTextMatchesPattern('^01[016789]-?[0-9]{3,4}-?[0-9]{4}$')
    .setHelpText('휴대폰 번호를 010-1234-5678 형식으로 적어 주세요.')
    .build();
  form.addTextItem()
    .setTitle('연락처 (휴대폰)')
    .setHelpText('예: 010-1234-5678')
    .setValidation(phoneRule)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('편한 연락 방법')
    .setChoiceValues(['전화', '문자·카카오톡'])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('연락 가능한 시간대 (여러 개 선택 가능)')
    .setChoiceValues(['평일 오전', '평일 오후', '평일 저녁(18시 이후)', '주말'])
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('저희 학원을 어떻게 알게 되셨나요?')
    .setChoiceValues(SOURCES)
    .showOtherOption(true)
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('궁금한 점이나 하고 싶은 이야기')
    .setRequired(false);

  form.addCheckboxItem()
    .setTitle('개인정보 수집·이용 동의')
    .setHelpText(
      '· 수집 항목: 이름, 연락처, 위 질문에 대한 답변\n' +
      '· 이용 목적: 상담 연락 및 상담 진행\n' +
      '· 보유 기간: 상담 종료 후 1년 또는 삭제 요청 시까지\n' +
      '· 동의하지 않을 수 있으며, 이 경우 상담 신청이 제한됩니다.\n' +
      '· 만 14세 미만은 보호자가 신청해 주세요.'
    )
    .setChoiceValues(['동의합니다'])
    .setRequired(true);

  // ── 섹션 분기 ────────────────────────────────
  purpose.setChoices([
    purpose.createChoice('입시 (게임학과·웹툰학과 진학)', ipsiPage),
    purpose.createChoice('취업 (국비 과정·취업 포트폴리오)', jobPage),
    purpose.createChoice('아직 모르겠어요 / 둘 다 궁금해요', commonPage),
  ]);
  // 입시 섹션을 마치면 취업 섹션을 건너뛰고 연락처로 이동
  jobPage.setGoToPage(commonPage);
  // 위 설정은 "취업 페이지 직전 섹션(=입시)이 끝난 뒤" 이동 위치다.
  // 취업 섹션은 바로 다음이 연락처라 별도 설정이 필요 없다.

  // ── 응답 시트 + 메일 알림 ──────────────────────
  const sheet = SpreadsheetApp.create(FORM_TITLE + ' (응답)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());
  ScriptApp.newTrigger('notifyOnSubmit').forForm(form).onFormSubmit().create();

  props.setProperty('FORM_ID', form.getId());

  Logger.log('응답용 주소(블로그·인스타에 사용): ' + form.getPublishedUrl());
  Logger.log('편집 주소(관리자용, 외부 공유 금지): ' + form.getEditUrl());
  Logger.log('응답 시트: ' + sheet.getUrl());
}

function notifyOnSubmit(e) {
  const answers = e.response.getItemResponses().map(function (r) {
    const v = r.getResponse();
    return '■ ' + r.getItem().getTitle() + '\n' + (Array.isArray(v) ? v.join(', ') : v);
  });
  const first = e.response.getItemResponses()[0];
  const kind = first ? String(first.getResponse()).split(' ')[0] : '';
  MailApp.sendEmail(
    NOTIFY_EMAIL,
    '[상담 신청] ' + kind + ' — ' + Utilities.formatDate(new Date(), 'Asia/Seoul', 'MM.dd HH:mm'),
    answers.join('\n\n')
  );
}
