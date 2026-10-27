const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 675 } });
await p.goto('file://' + __dirname + '/charlipedia-mcp.svg'); await p.screenshot({ path: __dirname + '/charlipedia-mcp.png' }); await b.close(); })();
