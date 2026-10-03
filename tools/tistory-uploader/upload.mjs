// 티스토리 비공개 업로더 v0.1.3 — aeo-blog 원고 폴더(posts/<날짜_슬러그>)를 티스토리에 '비공개 저장'한다.
//
//   node upload.mjs login              티스토리 로그인 창 열기(최초 1회·세션 만료 시). 로그인 후 창을 닫으면 끝
//   node upload.mjs check              로그인 상태 확인
//   node upload.mjs preview [폴더]     업로드 없이 최종 HTML 미리보기(preview.html) 생성
//   node upload.mjs upload  [폴더]     이미지 업로드 → 본문·FAQ 코드·카테고리·태그 입력 → 비공개 저장
//
// 원칙
// - 로그인은 사람이 직접 한다. 비밀번호를 저장하지 않는다(로그인 세션은 이 PC의 브라우저 프로필에만 저장).
// - 항상 '비공개 저장'만 한다. 비공개 선택·버튼 이름을 확인하지 못하면 저장하지 않고 멈춘다.
// - 공개 전환은 사람이 티스토리에서 검수 후 직접 한다.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import readline from "node:readline/promises";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const PROFILE = path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), ".local"), "blogaeo-uploader", "profile");
const POSTS = path.join(ROOT, "posts");
const cfgPath = path.join(ROOT, "config.json");

function fail(msg) { console.error(`\n[중단] ${msg}\n`); process.exit(1); }
function loadConfig() {
  if (!fs.existsSync(cfgPath)) fail("config.json 이 없습니다. config.example.json 을 복사해 config.json 으로 만들고 블로그 주소를 넣어 주세요.");
  const c = JSON.parse(fs.readFileSync(cfgPath, "utf-8"));
  if (!/^https:\/\/[^/]+\.tistory\.com\/?$|^https:\/\/[^/]+\/?$/.test(c.blogUrl || "")) fail("config.json 의 blogUrl 형식이 올바르지 않습니다. 예: https://youknow-that.tistory.com");
  return { blogUrl: c.blogUrl.replace(/\/$/, "") };
}

async function pickPost(arg) {
  if (arg) {
    const p = fs.existsSync(arg) ? arg : path.join(POSTS, arg);
    if (!fs.existsSync(path.join(p, "티스토리_본문.html"))) fail(`원고 폴더가 아닙니다: ${p}`);
    return path.resolve(p);
  }
  const list = fs.existsSync(POSTS) ? fs.readdirSync(POSTS).filter((d) => fs.existsSync(path.join(POSTS, d, "티스토리_본문.html"))).sort().reverse() : [];
  if (!list.length) fail(`posts 폴더에 원고가 없습니다. 받은 압축 파일을 ${POSTS} 안에 풀어 주세요.`);
  console.log("\n업로드할 원고를 고르세요:");
  list.forEach((d, i) => console.log(`  ${i + 1}) ${d}${fs.existsSync(path.join(POSTS, d, "uploaded.json")) ? "   (이미 업로드함)" : ""}`));
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const n = Number((await rl.question("번호 입력 (Enter = 1): ")).trim() || 1); rl.close();
  if (!list[n - 1]) fail("잘못된 번호입니다.");
  return path.join(POSTS, list[n - 1]);
}

// ---------- 원고 읽기 ----------
const IMG_RE = /<p>\[이미지 업로드: (\S+) \/ 대체텍스트: ([^\]]+)\]<\/p>/g;
const REAL_RE = /<p>\[실제 사진 (\d+): [^\]]*? \/ 대체텍스트: ([^\]]+)\]<\/p>/g;

function readPost(dir) {
  const meta = JSON.parse(fs.readFileSync(path.join(dir, "meta.json"), "utf-8"));
  const html = fs.readFileSync(path.join(dir, "티스토리_본문.html"), "utf-8");
  const faqPath = path.join(dir, "티스토리_FAQ코드.html");
  const faq = fs.existsSync(faqPath) ? fs.readFileSync(faqPath, "utf-8").trim() : "";
  const slots = [];
  for (const m of html.matchAll(IMG_RE)) slots.push({ marker: m[0], file: path.join(dir, "images", m[1]), alt: m[2].trim(), kind: "생성 이미지" });
  for (const m of html.matchAll(REAL_RE)) {
    const base = path.join(dir, "실제사진", `실제사진${m[1]}`);
    const file = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"].map((e) => base + e).find((f) => fs.existsSync(f));
    slots.push({ marker: m[0], file, alt: m[2].trim(), kind: `실제 사진 ${m[1]}` });
  }
  return { meta, html, faq, slots };
}

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
function figure(src, alt) {
  return `<figure data-ke-type="image" data-ke-style="alignCenter" style="margin:24px auto;text-align:center;"><img src="${esc(src)}" alt="${esc(alt)}" style="display:block;max-width:100%;height:auto;margin:0 auto;"></figure>`;
}
function compose(post, urls) {
  let out = post.html;
  const missing = [];
  for (const s of post.slots) {
    const url = urls.get(s.marker);
    if (url) out = out.replace(s.marker, figure(url, s.alt));
    else missing.push(s.kind); // 사진이 없으면 안내 줄을 그대로 남겨 사람이 보고 채우게 한다
  }
  if (/<p>\[이미지 업로드:/.test(out)) throw new Error("생성 이미지 자리 중 채워지지 않은 곳이 있습니다.");
  return { html: out + (post.faq ? `\n${post.faq}\n` : ""), missing };
}

// ---------- 브라우저 ----------
async function browser(headless) {
  const { chromium } = await import("playwright");
  fs.mkdirSync(PROFILE, { recursive: true });
  const opts = { headless, viewport: { width: 1400, height: 950 } };
  try { return await chromium.launchPersistentContext(PROFILE, { ...opts, channel: "chrome" }); }
  catch { try { return await chromium.launchPersistentContext(PROFILE, { ...opts, channel: "msedge" }); }
  catch (e) { fail(`Chrome 또는 Edge를 실행할 수 없습니다: ${e.message}`); } }
}
async function isLoggedIn(ctx, blogUrl) {
  const r = await ctx.request.get(`${blogUrl}/manage`, { failOnStatusCode: false, timeout: 30000 });
  return r.status() < 400 && !/auth\/login|accounts\.kakao\.com/.test(r.url()) && /\/manage/.test(r.url());
}

async function login(cfg) {
  const ctx = await browser(false);
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto("https://www.tistory.com/auth/login");
  console.log("\n열린 창에서 카카오 계정으로 로그인하세요. 로그인이 확인되면 자동으로 창이 닫힙니다. (최대 10분)");
  const end = Date.now() + 10 * 60_000;
  while (Date.now() < end) {
    await page.waitForTimeout(3000).catch(() => {});
    if (ctx.pages().length === 0) break;
    if (await isLoggedIn(ctx, cfg.blogUrl).catch(() => false)) { console.log("로그인 완료 · 세션이 이 PC에 저장되었습니다."); break; }
  }
  await ctx.close();
}

async function uploadImage(page, file) {
  const before = await cdnImages(page);
  const attach = page.locator('[role="button"][aria-label="첨부"]:visible').first();
  if (!await attach.count()) throw new Error("편집기의 '첨부' 버튼을 찾지 못했습니다(티스토리 화면 변경 가능성)");
  await attach.click();
  const photo = page.locator("#attach-image:visible").first();
  if (!await photo.count()) throw new Error("'사진' 메뉴를 찾지 못했습니다(티스토리 화면 변경 가능성)");
  const chooser = page.waitForEvent("filechooser", { timeout: 15000 });
  await photo.click();
  await (await chooser).setFiles(file);
  const end = Date.now() + 40000;
  while (Date.now() < end) {
    for (const u of await cdnImages(page)) if (!before.has(u)) return u;
    await page.waitForTimeout(500);
  }
  throw new Error(`이미지 업로드 주소를 확인하지 못했습니다: ${path.basename(file)}`);
}
async function cdnImages(page) {
  const set = new Set();
  for (const f of page.frames()) {
    const srcs = await f.locator("img").evaluateAll((els) => els.map((e) => e.src)).catch(() => []);
    for (const s of srcs) if (/^https?:\/\/.*(kakaocdn\.net|daumcdn\.net)/.test(s)) set.add(s);
  }
  return set;
}

async function upload(cfg, dir) {
  const post = readPost(dir);
  for (const s of post.slots) if (s.kind === "생성 이미지" && !fs.existsSync(s.file)) fail(`이미지 파일이 없습니다: ${s.file}`);
  console.log(`\n[1/6] 크롬 실행 · 원고: ${path.basename(dir)}`);
  const ctx = await browser(false); // 진행 과정을 눈으로 볼 수 있게 창을 띄운다
  try {
    const page = ctx.pages()[0] || await ctx.newPage();
    // '작성 중인 글을 이어서 쓸까요?' 같은 확인창이 뜨면 '취소'(새 글)로 진행
    page.on("dialog", (d) => d.dismiss().catch(() => {}));
    const newpost = `${cfg.blogUrl}/manage/newpost`;
    const onLogin = () => /auth\/login|accounts\.kakao\.com|logins\.daum|\/login/i.test(page.url());
    console.log("[2/6] 로그인 확인 …");
    await page.goto(newpost, { waitUntil: "domcontentloaded", timeout: 60000 });
    if (onLogin()) {
      // 세션이 없거나 만료됨 → 같은 창에서 로그인하면 이어서 진행
      console.log("      로그인이 필요합니다. 열린 크롬 창에서 카카오 로그인을 해 주세요. (최대 10분 대기)");
      const end = Date.now() + 10 * 60_000;
      while (Date.now() < end) {
        await page.waitForTimeout(3000);
        if (await isLoggedIn(ctx, cfg.blogUrl).catch(() => false)) break;
      }
      if (!await isLoggedIn(ctx, cfg.blogUrl).catch(() => false)) throw new Error("10분 안에 로그인이 확인되지 않았습니다");
      console.log("      로그인 확인 — 계속 진행합니다");
      await page.goto(newpost, { waitUntil: "domcontentloaded", timeout: 60000 });
    }
    if (!/\/manage\/newpost/.test(page.url())) throw new Error(`글쓰기 화면으로 가지 못했습니다. 현재 주소: ${page.url()}`);
    await page.waitForTimeout(2500);
    console.log("[3/6] 제목·이미지 입력 …");

    // 1) 제목
    const title = page.locator('textarea[placeholder*="제목"], input[placeholder*="제목"], #post-title-inp').first();
    if (!await title.count()) throw new Error("제목 입력칸을 찾지 못했습니다");
    await title.fill(post.meta.tistory_title);

    // 2) 이미지 업로드(생성 이미지 + 있는 실제 사진)
    const urls = new Map();
    for (const s of post.slots) {
      if (!s.file) { console.log(`  - ${s.kind}: 실제사진 폴더에 파일이 없어 건너뜀(안내 줄 유지)`); continue; }
      process.stdout.write(`  - ${s.kind} 업로드: ${path.basename(s.file)} … `);
      urls.set(s.marker, await uploadImage(page, s.file));
      console.log("완료");
    }

    console.log("[4/6] 본문·FAQ 코드 입력 …");
    // 3) 본문 + FAQ 코드 입력 후 코드가 살아 있는지 확인 (TinyMCE가 완전히 초기화된 뒤 입력 — 초기화 전 입력 시 빈 글로 저장된 사례 있음)
    await page.waitForFunction(() => window.tinymce?.activeEditor?.initialized === true, null, { timeout: 30000 })
      .catch(() => { throw new Error("편집기 초기화를 확인하지 못했습니다"); });
    const { html, missing } = compose(post, urls);
    const expected = (html.match(/application\/ld\+json/g) || []).length;
    const res = await page.evaluate((content) => {
      const ed = window.tinymce?.activeEditor; if (!ed) return null;
      ed.setContent(content); ed.fire("change"); ed.save();
      const saved = String(ed.getContent() || "");
      return { len: saved.length, ld: (saved.match(/application\/ld\+json/g) || []).length };
    }, html);
    if (!res || !res.len) throw new Error("편집기에 본문을 넣지 못했습니다");
    if (res.ld < expected) throw new Error(`FAQ 코드가 편집기에서 제거되었습니다(${res.ld}/${expected}) — 저장하지 않고 중단`);

    console.log("[5/6] 카테고리·태그 입력 …");
    // 4) 카테고리 · 태그
    const warns = [];
    if (post.meta.tistory_category) {
      try {
        const btn = page.locator("#category-btn:visible").first(); await btn.click();
        const opt = page.locator('#category-list [role="option"]:visible').filter({ hasText: post.meta.tistory_category }).first();
        if (!await opt.count()) throw new Error();
        await opt.click(); await page.waitForTimeout(200);
        if (!(await btn.innerText()).includes(post.meta.tistory_category)) throw new Error();
      } catch { warns.push(`카테고리 '${post.meta.tistory_category}' 선택 실패 — 티스토리에 해당 카테고리가 있는지 확인`); await page.keyboard.press("Escape").catch(() => {}); }
    }
    const tagInput = page.locator('input[placeholder*="태그"]').first();
    if (await tagInput.count()) { for (const t of (post.meta.tistory_tags || []).slice(0, 10)) { await tagInput.fill(t); await page.keyboard.press("Enter"); } }
    else warns.push("태그 입력칸을 찾지 못함");

    console.log("[6/6] 비공개 저장 …");
    // 5) 비공개 저장 (확인 못 하면 저장하지 않음)
    await page.locator("#publish-layer-btn:visible").first().click();
    await page.waitForTimeout(600);
    const priv = page.locator("#open0:visible").first();
    if (!await priv.count()) throw new Error("'비공개' 선택 항목을 찾지 못했습니다 — 저장하지 않고 중단");
    if (!await priv.isChecked()) await priv.check();
    if (!await priv.isChecked()) throw new Error("'비공개'로 설정되었는지 확인하지 못했습니다 — 저장하지 않고 중단");
    const save = page.locator("#publish-btn:visible").first();
    const label = (await save.innerText()).trim();
    if (label !== "비공개 저장") throw new Error(`저장 버튼이 '${label}' 입니다. 공개 발행 방지를 위해 중단`);
    await save.click();
    await page.waitForTimeout(2500);

    // 6) 글 목록에서 비공개 저장 확인
    await page.goto(`${cfg.blogUrl}/manage/posts/`, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(1500);
    const link = page.locator("a.link_cont").filter({ hasText: post.meta.tistory_title }).first();
    const row = (await link.count()) ? await link.locator("xpath=ancestor::li[1]").innerText() : "";
    const href = (await link.count()) ? await link.getAttribute("href") : null;
    if (!/비공개/.test(row)) throw new Error("글 목록에서 비공개 저장을 확인하지 못했습니다. 티스토리 '글 관리'에서 직접 확인해 주세요.");

    fs.writeFileSync(path.join(dir, "uploaded.json"), JSON.stringify({ at: new Date().toISOString(), url: href, private: true, missingPhotos: missing, warnings: warns }, null, 2));
    console.log(`\n[완료] 비공개 저장됨: ${href}`);
    if (missing.length) console.log(`  · 사진 미첨부: ${missing.join(", ")} → 티스토리 편집 화면에서 안내 줄 자리에 직접 넣어 주세요.`);
    for (const w of warns) console.log(`  · ${w}`);
    console.log("  · 티스토리에서 내용을 검수한 뒤 '공개'로 전환하세요. 공개 후 Claude에게 주소를 주면 검색 수집 준비까지 점검합니다.\n");
  } catch (e) {
    console.error(`\n[실패] ${e.message}\n원고와 이미지는 그대로 있습니다. 문제를 해결한 뒤 다시 실행하면 됩니다.`);
    console.error("크롬 창과 이 창을 캡처해 Claude에게 보내 주세요.");
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    await rl.question("Enter 를 누르면 크롬 창을 닫습니다 … "); rl.close();
    process.exitCode = 1;
  } finally { await ctx.close(); }
}

function preview(dir) {
  const post = readPost(dir);
  const urls = new Map(post.slots.filter((s) => s.file).map((s) => [s.marker, "file:///" + s.file.replace(/\\/g, "/")]));
  const { html, missing } = compose(post, urls);
  const out = path.join(dir, "preview.html");
  fs.writeFileSync(out, `<!doctype html><meta charset="utf-8"><title>${esc(post.meta.tistory_title)}</title><body style="max-width:760px;margin:24px auto;padding:0 16px;font-family:sans-serif;line-height:1.7"><h1>${esc(post.meta.tistory_title)}</h1>${html}<hr><p>태그: ${esc((post.meta.tistory_tags || []).join(", "))} / 카테고리: ${esc(post.meta.tistory_category || "")}</p>`);
  console.log(`미리보기 생성: ${out}`);
  console.log(`이미지 ${post.slots.length - missing.length}/${post.slots.length}개 연결, FAQ 코드 ${post.faq ? "있음" : "없음"}${missing.length ? `, 사진 미첨부: ${missing.join(", ")}` : ""}`);
}

const [cmd, arg] = process.argv.slice(2);
const cfg = cmd === "preview" ? null : loadConfig();
if (cmd === "login") await login(cfg);
else if (cmd === "check") { const ctx = await browser(true); console.log((await isLoggedIn(ctx, cfg.blogUrl)) ? "로그인 상태: 정상" : "로그인 필요: login.cmd 실행"); await ctx.close(); }
else if (cmd === "preview") preview(await pickPost(arg));
else if (cmd === "upload") await upload(cfg, await pickPost(arg));
else console.log("사용법: node upload.mjs login | check | preview [폴더] | upload [폴더]");
