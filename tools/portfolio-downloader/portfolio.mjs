// 학원 홈페이지 '학생 포트폴리오' 이미지 일괄 다운로드 (사용자 PC에서 실행)
//   node portfolio.mjs [목록URL] [최대페이지]
// - 목록 페이지(curPage=1,2,…)의 작품을 하나씩 열어 큰 이미지만 저장합니다.
// - 결과: 학생작품\<번호>_<제목>\01.jpg … / 학생작품\목록.csv / 학생작품\보기.html(한눈에 보기)
// - 작품을 하나도 못 찾으면 학생작품\_구조확인.html 을 남깁니다 → 이 파일을 Claude에게 보내 주세요.
// - 이미 받은 이미지는 건너뜁니다(다시 실행해도 안전).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const START = process.argv[2] || "http://sbsdaejeon-game.co.kr/2025/portfolio/portfolio.asp?curPage=1&seq=&hidDbType=&category=1&ptype=student";
const MAXPAGES = Number(process.argv[3] || 60);
const OUT = path.join(HERE, "학생작품");
const MIN_W = 400; // 이보다 작은 이미지(썸네일·아이콘)는 제외
const SKIP = /logo|btn|icon|bg_|banner|top_|footer|header|blank|spacer|sns|quick/i;

const log = (...a) => console.log(...a);
const safe = (s) => (s || "").replace(/[\\/:*?"<>|\r\n\t]+/g, " ").replace(/\s+/g, " ").trim().slice(0, 40) || "작품";
const pageUrl = (n) => { const u = new URL(START); u.searchParams.set("curPage", String(n)); return u.toString(); };

async function launch() {
  const { chromium } = await import("playwright");
  const opts = { headless: true };
  try { return await chromium.launch({ ...opts, channel: "chrome" }); }
  catch { try { return await chromium.launch({ ...opts, channel: "msedge" }); }
  catch { try { return await chromium.launch(opts); }
  catch (e) { console.error("Chrome 또는 Edge를 실행할 수 없습니다:", e.message); process.exit(1); } } }
}

// 목록에서 '작품 항목' 찾기: 이미지를 품은 링크/클릭 요소 (머리말·꼬리말 제외)
async function listItems(page) {
  return page.evaluate((SKIPSRC) => {
    const skip = new RegExp(SKIPSRC, "i");
    const out = [];
    const seen = new Set();
    for (const img of document.querySelectorAll("img")) {
      if (img.closest("header, footer, nav, #header, #footer, .header, .footer, #gnb, .gnb")) continue;
      if (skip.test(img.src) || (img.width && img.width < 80)) continue;
      const el = img.closest("a, [onclick]");
      if (!el) continue;
      const href = el.getAttribute("href") || "";
      const onclick = el.getAttribute("onclick") || "";
      const key = href + "|" + onclick + "|" + img.src;
      if (seen.has(key)) continue;
      seen.add(key);
      const box = el.closest("li, tr, td, .item, .list, div") || el;
      out.push({ key, href: href && !href.startsWith("javascript") && href !== "#" ? new URL(href, location.href).toString() : "",
        thumb: img.src, title: (img.alt || box.innerText || "").trim().split("\n")[0] });
    }
    return out;
  }, SKIP.source);
}

// 열린 화면(상세 페이지 또는 팝업 레이어)에서 큰 이미지 주소 모으기
async function bigImages(page, exclude) {
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); } });
  await page.waitForTimeout(600);
  const srcs = await page.evaluate(({ MIN_W, SKIPSRC }) => {
    const skip = new RegExp(SKIPSRC, "i");
    return [...document.querySelectorAll("img")]
      .filter((i) => i.naturalWidth >= MIN_W && !skip.test(i.src) && getComputedStyle(i).display !== "none")
      .map((i) => i.currentSrc || i.src);
  }, { MIN_W, SKIPSRC: SKIP.source });
  return [...new Set(srcs)].filter((s) => !exclude.has(s));
}

async function save(ctx, src, file) {
  if (fs.existsSync(file)) return true;
  try {
    const r = await ctx.request.get(src, { timeout: 30000 });
    if (!r.ok()) return false;
    fs.writeFileSync(file, await r.body());
    return true;
  } catch { return false; }
}

fs.mkdirSync(OUT, { recursive: true });
const browser = await launch();
const ctx = await browser.newContext({ viewport: { width: 1400, height: 950 }, locale: "ko-KR" });
const page = await ctx.newPage();
const rows = [];
const done = new Set();
let prevSig = "";

for (let n = 1; n <= MAXPAGES; n++) {
  await page.goto(pageUrl(n), { waitUntil: "networkidle", timeout: 45000 }).catch(() => {});
  const items = await listItems(page);
  const sig = items.map((i) => i.key).join("\n");
  if (!items.length) {
    if (n === 1) {
      fs.writeFileSync(path.join(OUT, "_구조확인.html"), await page.content());
      log("[중단] 작품 항목을 찾지 못했습니다. 학생작품\\_구조확인.html 을 Claude에게 보내 주세요.");
    }
    break;
  }
  if (sig === prevSig) break; // 마지막 페이지를 넘김
  prevSig = sig;
  // 목록 화면에 원래 있던 큰 이미지(배너 등)는 작품 이미지에서 제외
  const base = new Set(await bigImages(page, new Set()));
  log(`\n[${n}쪽] 작품 ${items.length}개`);

  for (let k = 0; k < items.length; k++) {
    const it = items[k];
    if (done.has(it.key)) continue;
    done.add(it.key);
    let srcs = [];
    let detailUrl = it.href;
    if (it.href) {
      const d = await ctx.newPage();
      await d.goto(it.href, { waitUntil: "networkidle", timeout: 45000 }).catch(() => {});
      srcs = await bigImages(d, base);
      await d.close();
    } else {
      // 자바스크립트로 여는 항목: 클릭해서 새 창·이동·팝업 레이어 중 무엇이든 처리
      const before = page.url();
      const popupP = ctx.waitForEvent("page", { timeout: 4000 }).catch(() => null);
      await page.evaluate((key) => {
        const [href, onclick, src] = key.split("|");
        const img = [...document.images].find((i) => i.src === src);
        (img?.closest("a, [onclick]") || img)?.click();
      }, it.key);
      const popup = await popupP;
      if (popup) {
        await popup.waitForLoadState("networkidle").catch(() => {});
        detailUrl = popup.url();
        srcs = await bigImages(popup, base);
        await popup.close();
      } else {
        await page.waitForLoadState("networkidle").catch(() => {});
        await page.waitForTimeout(800);
        if (page.url() !== before) detailUrl = page.url();
        srcs = await bigImages(page, base);
        await page.goto(pageUrl(n), { waitUntil: "networkidle", timeout: 45000 }).catch(() => {});
      }
    }
    const no = String(rows.length + 1).padStart(3, "0");
    const dir = path.join(OUT, `${no}_${safe(it.title)}`);
    let saved = 0;
    if (srcs.length) {
      fs.mkdirSync(dir, { recursive: true });
      for (let i = 0; i < srcs.length; i++) {
        const ext = (path.extname(new URL(srcs[i]).pathname) || ".jpg").toLowerCase().slice(0, 5);
        if (await save(ctx, srcs[i], path.join(dir, String(i + 1).padStart(2, "0") + ext))) saved++;
      }
    } else if (it.thumb) {
      // 상세 이미지가 없으면 목록 이미지라도 저장
      fs.mkdirSync(dir, { recursive: true });
      if (await save(ctx, it.thumb, path.join(dir, "00_목록이미지" + (path.extname(new URL(it.thumb).pathname) || ".jpg")))) saved++;
    }
    rows.push({ no, title: safe(it.title), dir: path.basename(dir), url: detailUrl || pageUrl(n), saved });
    log(`  ${no} ${safe(it.title)} — ${saved}장`);
  }
}
await browser.close();

// 목록.csv / 보기.html
const csv = "﻿번호,제목,폴더,원본주소,이미지수\n" + rows.map((r) => [r.no, r.title, r.dir, r.url, r.saved].map((v) => `"${String(v).replace(/"/g, '""')}"`).join(",")).join("\n");
fs.writeFileSync(path.join(OUT, "목록.csv"), csv);
const cards = rows.filter((r) => r.saved).map((r) => {
  const files = fs.readdirSync(path.join(OUT, r.dir)).filter((f) => /\.(jpe?g|png|gif|webp)$/i.test(f));
  return `<div class="c"><div class="t">${r.no} ${r.title} (${files.length}장)</div>${files.map((f) => `<a href="${encodeURI(r.dir + "/" + f)}" target="_blank"><img src="${encodeURI(r.dir + "/" + f)}" loading="lazy"></a>`).join("")}</div>`;
}).join("\n");
fs.writeFileSync(path.join(OUT, "보기.html"), `<!doctype html><meta charset="utf-8"><title>학생작품</title><style>body{font-family:sans-serif;background:#f4f6fb;margin:20px}.c{background:#fff;border-radius:10px;padding:12px;margin:0 0 14px}.t{font-weight:bold;margin-bottom:8px}img{height:160px;margin:0 6px 6px 0;border-radius:6px;object-fit:cover}</style><h2>학생작품 ${rows.length}개</h2>${cards}`);
const total = rows.reduce((a, r) => a + r.saved, 0);
log(`\n완료: 작품 ${rows.length}개, 이미지 ${total}장 → ${OUT}`);
log("학생작품\\보기.html 을 열면 한눈에 볼 수 있습니다.");
if (rows.length && total === 0) log("이미지를 하나도 받지 못했습니다. 학생작품\\목록.csv 와 화면 상황을 Claude에게 알려 주세요.");
