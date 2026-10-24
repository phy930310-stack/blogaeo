/**
 * SBS아카데미게임학원 대전점 — 입시·취업 상담 신청 구글 폼 생성 스크립트
 *
 * 사용법: README.md 참고. script.google.com 새 프로젝트에 이 파일 내용을 붙여 넣고
 * createConsultForm 을 한 번 실행하면 폼 + 응답 시트 + 알림(디스코드·메일)이 만들어진다.
 * 디스코드 웹후크 주소는 코드에 쓰지 않고 '스크립트 속성' DISCORD_WEBHOOK_URL 에 넣는다.
 *
 * 구조(섹션 분기)
 *   1. 상담 목적 → [입시] 2-A로 / [취업] 2-B로 / [모르겠음] 3으로
 *   2-A. 입시 질문 → 끝나면 3으로
 *   2-B. 취업 질문 → 3으로
 *   3. 연락처·유입 경로·개인정보 동의 (공통)
 */

const FORM_TITLE = 'SBS아카데미게임학원 대전점 입시·취업 상담 신청';
const NOTIFY_EMAIL = 'phy930310@gmail.com';
const SEND_EMAIL = true; // 디스코드가 끊겼을 때를 대비한 예비 알림. 메일이 필요 없으면 false
const PHONE = '042-716-7439';

// 관심 과정 선택지 (2026-10-24 사용자 확정: 언리얼·AI개발·애니메이션 추가)
const COURSES = [
  '게임기획',
  '게임프로그래밍(유니티&언리얼)',
  'AI개발',
  '게임원화·일러스트',
  '애니메이션(2D, 3D)',
  '3D 그래픽',
  '웹툰',
  '웹소설',
  '아직 모르겠어요',
];
const COURSE_TITLE = '관심 있는 과정 (여러 개 선택 가능)';

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
    .setTitle(COURSE_TITLE)
    .setChoiceValues(COURSES)
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
  const items = e.response.getItemResponses();
  const a = {};
  items.forEach(function (r) {
    const v = r.getResponse();
    a[r.getItem().getTitle()] = Array.isArray(v) ? v.join(', ') : String(v);
  });
  const purpose = a['어떤 상담을 원하세요?'] || '';
  const kind = purpose.indexOf('입시') === 0 ? '입시' : purpose.indexOf('취업') === 0 ? '취업' : '미정';
  const sheetUrl = 'https://docs.google.com/spreadsheets/d/' + e.source.getDestinationId();
  const time = Utilities.formatDate(new Date(), 'Asia/Seoul', 'MM.dd HH:mm');

  // 메일을 먼저 보낸다 — 메신저 전송이 실패해도 메일 알림은 남도록
  if (SEND_EMAIL) {
    MailApp.sendEmail(
      NOTIFY_EMAIL,
      '[상담 신청] ' + kind + ' — ' + time,
      Object.keys(a).map(function (k) { return '■ ' + k + '\n' + a[k]; }).join('\n\n')
    );
  }

  // 디스코드: 연락처 일부를 가린 요약만 보낸다(전체 정보는 응답 시트에서 확인)
  const who = kind === '입시'
    ? [a['학생 학년'], a['신청하시는 분']]
    : kind === '취업' ? [a['현재 상황'], '내일배움카드 ' + (a['국민내일배움카드가 있으신가요?'] || '-')] : [];
  sendDiscord_([
    '[상담 신청] ' + [kind].concat(who).filter(String).join(' · ') + '  (' + time + ')',
    '관심: ' + (a[COURSE_TITLE] || '-'),
    '유입: ' + (a['저희 학원을 어떻게 알게 되셨나요?'] || '-'),
    '연락: ' + (a['편한 연락 방법'] || '-') + ' / ' + maskPhone_(a['연락처 (휴대폰)']) +
      (a['연락 가능한 시간대 (여러 개 선택 가능)'] ? ' / ' + a['연락 가능한 시간대 (여러 개 선택 가능)'] : ''),
    '→ 응답 시트: ' + sheetUrl,
  ].join('\n'));
}

// 디스코드 웹후크로 보낸다. 실패해도 예외를 던지지 않고 결과만 돌려준다(메일 알림·폼 처리를 막지 않도록).
// 구글 서버에서 discord.com 으로 직접 보내면 429(error 1015) 차단이 생길 수 있다 →
// 그때는 DISCORD_WEBHOOK_URL 의 'https://discord.com' 부분만 중계 주소로 바꾼다(README '429 오류가 날 때').
function sendDiscord_(text) {
  const url = PropertiesService.getScriptProperties().getProperty('DISCORD_WEBHOOK_URL');
  if (!url) return ''; // 아직 웹후크를 설정하지 않았으면 메일만 보낸다
  const result = post_(url, { username: '상담 신청 알림', content: text });
  Logger.log('디스코드: ' + result);
  return result;
}

// 성공하면 '성공', 실패하면 '실패(코드)'. 429(요청 제한)는 잠깐 쉬었다 두 번까지 다시 시도한다.
function post_(url, body) {
  let code = 0;
  for (let i = 0; i < 3; i++) {
    try {
      const res = UrlFetchApp.fetch(url, {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify(body),
        muteHttpExceptions: true,
      });
      code = res.getResponseCode();
      if (code >= 200 && code < 300) return '성공';
      if (code !== 429) break;
    } catch (err) {
      code = String(err);
    }
    Utilities.sleep(3000 * (i + 1));
  }
  return '실패(' + code + ')';
}

function maskPhone_(phone) {
  const d = String(phone || '').replace(/[^0-9]/g, '');
  return d.length >= 10 ? d.slice(0, 3) + '-****-' + d.slice(-4) : '-';
}

// 디스코드 연결 확인용: 웹후크 주소를 넣은 뒤 이 함수를 한 번 실행하면 테스트 메시지가 온다
// (처음 실행 시 '외부 서비스 연결' 권한을 허용해야 실제 신청 알림도 작동한다)
function testDiscord() {
  const result = sendDiscord_('✅ 상담 신청 알림 연결 테스트입니다. 이 메시지가 보이면 설정 완료입니다.');
  if (!result) throw new Error('스크립트 속성에 DISCORD_WEBHOOK_URL 을 먼저 넣어 주세요.');
  if (result !== '성공') throw new Error('디스코드 전송 ' + result + ' — README의 \'429 오류가 날 때\'를 확인하세요.');
}

// 섹션 이미지 넣기: 한 번만 실행 (다시 실행하면 같은 이미지가 또 들어간다)
// 이미지는 공개 저장소(GitHub)의 고정 커밋에서 받아 오므로 드라이브에 올릴 필요가 없다.
const IMAGE_BASE = 'https://raw.githubusercontent.com/phy930310-stack/blogaeo/67705fd9611f58fc799a5720d5334c33f23d05ae/tools/google-form/assets/';

function decorateForm() {
  const formId = PropertiesService.getScriptProperties().getProperty('FORM_ID');
  if (!formId) throw new Error('먼저 createConsultForm 으로 폼을 만들어 주세요.');
  const form = FormApp.openById(formId);
  const plan = [
    { section: '입시 상담', file: '폼_입시.png' },
    { section: '취업 상담', file: '폼_취업.png' },
    { section: '연락처', file: '폼_연락처.png' },
  ];
  plan.forEach(function (p) {
    const blob = UrlFetchApp.fetch(IMAGE_BASE + encodeURIComponent(p.file)).getBlob().setName(p.file);
    const breakItem = form.getItems(FormApp.ItemType.PAGE_BREAK).filter(function (it) {
      return it.getTitle() === p.section;
    })[0];
    if (!breakItem) throw new Error('폼에서 "' + p.section + '" 섹션을 찾지 못했습니다.');
    const img = form.addImageItem().setImage(blob).setTitle('')
      .setAlignment(FormApp.Alignment.CENTER).setWidth(640);
    form.moveItem(img.getIndex(), breakItem.getIndex() + 1);
    Logger.log(p.section + ' 섹션에 ' + p.file + ' 추가');
  });
}

// 이미 만든 폼의 '관심 있는 과정' 선택지를 COURSES 로 바꾼다 (기존 응답은 그대로 남는다)
function updateCourseChoices() {
  const formId = PropertiesService.getScriptProperties().getProperty('FORM_ID');
  if (!formId) throw new Error('FORM_ID 가 없습니다.');
  const item = FormApp.openById(formId).getItems(FormApp.ItemType.CHECKBOX).filter(function (it) {
    return it.getTitle() === COURSE_TITLE;
  })[0];
  if (!item) throw new Error('"' + COURSE_TITLE + '" 문항을 찾지 못했습니다.');
  item.asCheckboxItem().setChoiceValues(COURSES);
  Logger.log('관심 과정 선택지 변경: ' + COURSES.join(' / '));
}
