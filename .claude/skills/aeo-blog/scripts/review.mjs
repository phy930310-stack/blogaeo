// 발행 후 점검: node .claude/skills/aeo-blog/scripts/review.mjs <티스토리URL> <네이버URL> <출력폴더>
// - PC(1280px)·모바일(iPhone 13) 화면을 구간별 PNG로 저장 (<출력폴더>/t-desk-0.png …)
// - 자동 점검 결과를 콘솔과 <출력폴더>/review.json 으로 저장
// URL 하나만 점검하려면 다른 쪽에 "-" 를 넣습니다.
import { createRequire } from "module";
import { mkdirSync, writeFileSync } from "fs";
import { join } from "path";

const require = createRequire(import.meta.url);
const { chromium, devices } = require("playwright");
const [tUrl, nUrl, out = "review-out"] = process.argv.slice(2);
mkdirSync(out, { recursive: true });

function naverUrls(u) {
  const m = u.match(/blog\.naver\.com\/([^/?#]+)\/(\d+)/) || [];
  const id = m[1] || new URL(u).searchParams.get("blogId");
  const no = m[2] || new URL(u).searchParams.get("logNo");
  return { desk: `https://blog.naver.com/PostView.naver?blogId=${id}&logNo=${no}`, mob: `https://m.blog.naver.com/${id}/${no}` };
}
function tistoryUrls(u) {
  const x = new URL(u);
  return { desk: u, mob: `${x.origin}/m${x.pathname.replace(/^\/m/, "")}` };
}

const browser = await chromium.launch(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {});

async function open(url, mobile) {
  const ctx = await browser.newContext({ ...(mobile ? devices["iPhone 13"] : { viewport: { width: 1280, height: 900 } }), ignoreHTTPSErrors: true, locale: "ko-KR" });
  const p = await ctx.newPage();
  try { await p.goto(url, { waitUntil: "networkidle", timeout: 30000 }); } catch {}
  // 리다이렉트 등으로 컨텍스트가 바뀌면 한 번 더 시도
  for (let i = 0; i < 3; i++) {
    try {
      await p.waitForLoadState("domcontentloaded");
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 200)); } window.scrollTo(0, 0); });
      break;
    } catch { await p.waitForTimeout(2000); }
  }
  await p.waitForTimeout(2000);
  return { ctx, p };
}
async function shots(p, name, width) {
  const H = await p.evaluate(() => document.body.scrollHeight);
  const step = width > 600 ? 1500 : 1800;
  for (let y = 0, k = 0; y < H; y += step, k++)
    await p.screenshot({ path: join(out, `${name}-${k}.png`), fullPage: true, clip: { x: 0, y, width, height: Math.min(step, H - y) } });
}

const report = {};

if (tUrl && tUrl !== "-") {
  const u = tistoryUrls(tUrl);
  const { ctx, p } = await open(u.desk, false);
  report.tistory = await p.evaluate(() => {
    const body = document.querySelector(".article-view, .tt_article_useless_p_margin, .entry-content, article") || document.body;
    const text = body.innerText;
    const lds = [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent);
    const imgs = [...body.querySelectorAll("img")].filter((i) => i.naturalWidth > 200 || i.width > 200);
    const tables = [...body.querySelectorAll("table")];
    return {
      faqPage: lds.some((t) => t.includes('"FAQPage"')),
      faqParses: lds.filter((t) => t.includes("FAQPage")).every((t) => { try { JSON.parse(t); return true; } catch { return false; } }),
      images: imgs.length,
      imagesMissingAlt: imgs.filter((i) => !i.alt || i.alt.length < 5).length,
      imagesBroken: imgs.filter((i) => i.complete && i.naturalWidth === 0).length,
      leftoverMarkers: ["[이미지 업로드", "대체텍스트:", '"@context"', "본문 시작"].filter((m) => text.includes(m)),
      category: (document.querySelector(".category, .tit_category, [class*=category]") || {}).innerText?.trim().slice(0, 30) || null,
      tags: [...document.querySelectorAll('a[rel="tag"], .tag_label a, .area_tag a')].map((a) => a.innerText.trim()).filter(Boolean),
      tablesTotal: tables.length,
      tablesWithoutScrollWrapper: tables.filter((t) => !/overflow-x/.test(t.parentElement?.getAttribute("style") || "")).length,
      blockquoteCentered: [...body.querySelectorAll("blockquote")].some((b) => getComputedStyle(b).textAlign === "center"),
      hasDisclaimerIfCase: !/상담에서 자주/.test(text) || /가상 사례/.test(text),
      hasSources: /참고 자료/.test(text),
    };
  });
  await shots(p, "t-desk", 1280); await ctx.close();
  const m = await open(u.mob, true);
  report.tistory.mobileVerticalBreakCells = await m.p.evaluate(() =>
    [...document.querySelectorAll("td,th")].filter((c) => {
      // 짧은 셀(3~6자)의 글자가 3줄 이상으로 쪼개졌는지 실제 줄 수로 판정
      const t = c.innerText.trim(); if (t.length < 3 || t.length > 6) return false;
      const r = document.createRange(); r.selectNodeContents(c);
      const tops = new Set([...r.getClientRects()].map((x) => Math.round(x.top)));
      return tops.size >= 3;
    }).map((c) => c.innerText.trim()).slice(0, 10));
  await shots(m.p, "t-mob", 390); await m.ctx.close();
}

if (nUrl && nUrl !== "-") {
  const u = naverUrls(nUrl);
  const { ctx, p } = await open(u.desk, false);
  report.naver = await p.evaluate(() => {
    const body = document.querySelector(".se-main-container") || document.body;
    const text = body.innerText;
    const sizes = {};
    body.querySelectorAll(".se-text-paragraph span[class*=se-fs-]").forEach((s) => { const c = [...s.classList].find((x) => x.startsWith("se-fs-")); sizes[c] = (sizes[c] || 0) + 1; });
    return {
      sectionTitles: body.querySelectorAll(".se-sectionTitle").length,
      rawSquareHeadings: (text.match(/^■/gm) || []).length,
      quotations: body.querySelectorAll(".se-quotation").length,
      images: body.querySelectorAll(".se-image").length,
      captions: [...body.querySelectorAll(".se-caption")].filter((c) => c.innerText.trim()).length,
      map: body.querySelectorAll(".se-placesMap, .se-map").length > 0,
      leftoverMarkers: ["[제목]", "[태그]", "[이미지:", "사진 설명:", "[네이버 지도"].filter((m) => text.includes(m)),
      hasDisclaimerIfCase: !/상담에서 자주/.test(text) || /가상 사례/.test(text),
      hasSources: /참고 자료/.test(text),
      fontSizeClasses: sizes,
    };
  });
  await shots(p, "n-desk", 1280); await ctx.close();
  const m = await open(u.mob, true);
  report.naver.tags = await m.p.evaluate(() => [...document.querySelectorAll('[class*="tag"] a, a[href*="tag"]')].map((a) => a.innerText.trim()).filter((t) => t.startsWith("#")).slice(0, 20));
  await shots(m.p, "n-mob", 390); await m.ctx.close();
}

await browser.close();
writeFileSync(join(out, "review.json"), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
