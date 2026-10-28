// 사용법: node .claude/skills/aeo-blog/scripts/render.mjs posts/<폴더>/images [파일명 접두어]
// <폴더>/images/src/*.html 을 같은 이름의 PNG로 <폴더>/images/ 에 저장합니다.
// 캔버스 크기는 각 HTML의 .canvas 요소 크기를 따릅니다.
import { createRequire } from "module";
import { readdirSync } from "fs";
import { join, resolve, basename } from "path";
import { pathToFileURL } from "url";

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); }
catch { ({ chromium } = require(join(process.env.npm_config_prefix || "/usr/local", "lib/node_modules/playwright"))); }

const dir = resolve(process.argv[2] || ".");
const srcDir = join(dir, "src");
// 세 번째 인자를 주면 그 글자로 시작하는 HTML만 렌더링한다. 예: ... instagram/assets v2_03_
const prefix = process.argv[3] || "";
const files = readdirSync(srcDir).filter((f) => f.endsWith(".html") && f.startsWith(prefix));
// 번들 크로미움이 없는 PC에서는 PLAYWRIGHT_CHANNEL=chrome 또는 msedge 로 설치된 브라우저를 쓴다
const browser = await chromium.launch(process.env.PLAYWRIGHT_CHANNEL ? { channel: process.env.PLAYWRIGHT_CHANNEL } : {});
const page = await browser.newPage({ deviceScaleFactor: 1 });
for (const f of files) {
  await page.goto(pathToFileURL(join(srcDir, f)).href);
  await page.evaluate(() => document.fonts.ready);
  const el = await page.$(".canvas");
  const out = join(dir, basename(f, ".html") + ".png");
  await el.screenshot({ path: out });
  console.log("rendered", out);
}
await browser.close();
