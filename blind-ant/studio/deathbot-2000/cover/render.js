const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [, , svgPath, pngPath, w, h] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2 });
  const svg = fs.readFileSync(svgPath, 'utf8');
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${w}" height="${h}" `)}</body></html>`);
  await p.screenshot({ path: pngPath, omitBackground: true });
  await b.close();
})();
