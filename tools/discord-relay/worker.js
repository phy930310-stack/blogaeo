// 구글 앱스 스크립트 → 디스코드 웹후크 중계 (Cloudflare Workers, 무료)
// 구글 서버에서 discord.com 으로 직접 보내면 429(error 1015)로 막히는 경우가 있어,
// 이 워커가 받은 요청을 같은 경로 그대로 discord.com 에 전달한다.
// 사용: DISCORD_WEBHOOK_URL 의 'https://discord.com' 을 'https://<워커 주소>' 로 바꾼다.
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method !== 'POST' || !url.pathname.startsWith('/api/webhooks/')) {
      return new Response('not found', { status: 404 });
    }
    const res = await fetch('https://discord.com' + url.pathname + url.search, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: await request.text(),
    });
    return new Response(await res.text(), { status: res.status });
  },
};
