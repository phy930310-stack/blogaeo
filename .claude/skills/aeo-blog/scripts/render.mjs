// 사용법: node .claude/skills/aeo-blog/scripts/render.mjs posts/<폴더>/images
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
const files = readdirSync(srcDir).filter((f) => f.endsWith(".html"));
const browser = await chromium.launch();
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
