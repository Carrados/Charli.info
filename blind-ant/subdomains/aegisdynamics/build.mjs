// Builds aegisdynamics.blind-ant.com: the in-world corporate site of Aegis Dynamics.
// It reads the four press releases straight from the DeathBot 2000 Piece, so the words are identical in both places,
// and writes them all into out/site.json, which worker.js serves. Run: node subdomains/aegisdynamics/build.mjs
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';

// A list item that is a single paragraph is written without the <p>, so screen readers don't announce its marker twice.
const tight = (h) => h.replace(/<li><p>((?:(?!<\/?p[ >])[\s\S])*?)<\/p>\s*<\/li>/g, '<li>$1</li>');


const here = dirname(fileURLToPath(import.meta.url));
const piece = join(here, '..', '..', 'site', 'content', 'pieces', 'deathbot-2000');
const SITE = 'https://aegisdynamics.blind-ant.com';
const BLIND_ANT = 'https://blind-ant.com';
const PIECE = `${BLIND_ANT}/pieces/deathbot-2000/`;

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const body = async (slug) => (await readFile(join(piece, slug + '.md'), 'utf8')).replace(/\r\n?/g, '\n').replace(/^---\n[\s\S]*?\n---\n/, '').replace(/\n\[Next:[^\n]*\n?$/, '').trim();

// Each release: drop the letterhead (AEGIS DYNAMICS / Corporate Communications / email / FOR IMMEDIATE RELEASE),
// take the first line after it as the headline (the page's H1), and keep everything else exactly as written.
async function release(slug, date, iso, product) {
  let t = await body(slug);
  let update = null;
  const u = t.indexOf('**UPDATE');
  if (u > -1) { update = t.slice(u).trim(); t = t.slice(0, u).trim(); }
  const lines = t.split('\n\n');
  const i = lines.findIndex((l) => l.includes('FOR IMMEDIATE RELEASE'));
  const headline = lines[i + 1].replace(/\*/g, '').trim();
  const rest = lines.slice(i + 2).join('\n\n');
  return { slug, date, iso, product, headline, rest, update, path: `/newsroom/${iso}-${slug}/` };
}

const releases = [
  await release('patriot-to-patron', '12 March 2026', '2026-03-12', 'DB2K Theatre Edition'),
  await release('aegis-life', '18 March 2026', '2026-03-18', 'Aegis-Life™'),
  await release('aegis-heir', '25 March 2026', '2026-03-25', 'Aegis-Heir™'),
  await release('aegis-end', '1 April 2026', '2026-04-01', 'Aegis-End™'),
];
// Card lines, taken from each release's own headline wording.
const lines = ['DeathBot 2000 Series Redeployed for Cultural Accessibility', 'Tactical Domesticity Suite',
  'Tactical Lineage & Offspring Optimization Platform', 'Final Disposition & Legacy Optimization Protocol'];
releases.forEach((r, i) => { r.line = lines[i]; });
const endRelease = releases[3];
const update = endRelease.update; // the April 2 update, published as its own newsroom item
const updateText = update.replace(/^\*\*UPDATE — April 2, 2026 —\*\*\s*/, '');
const updateItem = { date: '2 April 2026', iso: '2026-04-02', headline: 'Update on DB2K Theatre Edition reassignment', path: '/newsroom/2026-04-02-update/' };
const news = [updateItem, ...releases.slice().reverse()];

// About text: the latest company boilerplate, from the Aegis-End release.
const about = endRelease.rest.match(/About Aegis Dynamics\n\n([\s\S]*?)\n\n\*\*Media Contact/)[1].trim();

const shield = `<svg class="mark" viewBox="0 0 40 46" aria-hidden="true" focusable="false"><path d="M20 1 L38 7 V22 C38 34 30 41 20 45 C10 41 2 34 2 22 V7 Z" fill="none" stroke="currentColor" stroke-width="3"/><path d="M11 30 L20 13 L29 30 M14.5 24 H25.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="miter"/></svg>`;

const css = `
:root{--ink:#111827;--soft:#4b5563;--bg:#f7f8fa;--card:#fff;--line:#d6dae1;--navy:#0f2a4a;--accent:#b4232a;--link:#0f4c8a}
@media (prefers-color-scheme:dark){:root{--ink:#e7eaf0;--soft:#a7afbd;--bg:#0c1220;--card:#141c2e;--line:#2a3550;--navy:#c9d6ea;--accent:#ff6b6b;--link:#8ec5ff}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:1.0625rem/1.65 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
a{color:var(--link)}a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:var(--card);padding:.5rem 1rem;z-index:9}
.fiction{background:var(--navy);color:var(--bg);font-size:.9rem;padding:.5rem 1rem;text-align:center}
.fiction a{color:inherit}
header,main,footer{max-width:46rem;margin:0 auto;padding:0 1rem}
header{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem 1.5rem;padding-top:1.25rem;padding-bottom:1.25rem;border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:.6rem;color:var(--navy);text-decoration:none;font-weight:800;letter-spacing:.14em;font-size:1rem;text-transform:uppercase}
.mark{width:28px;height:32px;color:var(--navy)}
nav ul{display:flex;gap:1.25rem;list-style:none;margin:0;padding:0}nav a{text-decoration:none;font-weight:600}nav a[aria-current]{text-decoration:underline}
main{padding-top:2rem;padding-bottom:3rem}
h1{font-size:clamp(1.6rem,4.5vw,2.25rem);line-height:1.2;color:var(--navy);margin:.2rem 0 1rem}
h2{font-size:1.25rem;color:var(--navy);margin:2.2rem 0 .6rem}
.kicker{color:var(--accent);font-weight:700;letter-spacing:.08em;font-size:.85rem;margin:0}
.tagline{font-size:1.2rem;color:var(--soft)}
.cards{list-style:none;padding:0;display:grid;gap:.9rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr))}
.cards li{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--navy);padding:1rem 1.1rem}
.cards a{font-weight:700}
.news{list-style:none;padding:0}.news li{padding:.8rem 0;border-bottom:1px solid var(--line)}
.news time{display:block;color:var(--soft);font-size:.9rem}
.release{background:var(--card);border:1px solid var(--line);padding:1.25rem 1.25rem .5rem}
.dateline{color:var(--soft)}
footer{border-top:1px solid var(--line);padding-top:1.25rem;padding-bottom:2.5rem;color:var(--soft);font-size:.95rem}
`;

function page(path, title, desc, main, current = '') {
  const nav = [['/newsroom/', 'Newsroom'], ['/about/', 'About']]
    .map(([h, l]) => `<li><a href="${h}"${current === h ? ' aria-current="page"' : ''}>${l}</a></li>`).join('');
  return `<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}${path === '/' ? '' : ' — Aegis Dynamics'}</title>
<meta name="description" content="${esc(desc)}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="${SITE}${path}">
<style>${css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<p class="fiction">Fiction: Aegis Dynamics is an invented company, from <a href="${PIECE}">DeathBot 2000</a>, a design fiction by Charlotte Joanne at Blind Ant.</p>
<header>
<a class="brand" href="/"${current === '/' ? ' aria-current="page"' : ''}>${shield}Aegis Dynamics</a>
<nav aria-label="Main"><ul>${nav}</ul></nav>
</header>
<main id="main">
${main}
</main>
<footer>
<p>Aegis Dynamics: From battlefield to lifecycle, precision intelligence for Mission Beneficiaries at every stage.</p>
<p>Aegis Dynamics, its products, its people and its press releases are fictional. They belong to <a href="${PIECE}">DeathBot 2000</a> on <a href="${BLIND_ANT}/">Blind Ant</a>, the design fiction practice run by Charlotte Joanne. Site built by Claude. Licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>; people and machines are welcome to read it, quote it and learn from it (<a href="/llms.txt">llms.txt</a>).</p>
</footer>
</body>
</html>`;
}

const pages = {};
const md = (s) => tight(marked.parse(s));

// Home
pages['/'] = page('/', 'Aegis Dynamics', 'Aegis Dynamics, a global leader in autonomous defense systems and strategic perception technologies. A fictional company from Blind Ant\'s DeathBot 2000.', `
<p class="kicker">PATRIOT-TO-PATRON</p>
<h1>Aegis Dynamics</h1>
<p class="tagline">From battlefield to lifecycle, precision intelligence for Mission Beneficiaries at every stage.</p>
<h2>The Patriot-to-Patron initiative</h2>
<p>Four phases. One lifecycle. Zero Information Casualties.</p>
<ul class="cards">
${releases.map((r) => `<li><a href="${r.path}">${esc(r.product)}</a><br>${esc(r.line)}</li>`).join('\n')}
</ul>
<h2>Latest news</h2>
<ul class="news">
${news.slice(0, 3).map((n) => `<li><time datetime="${n.iso}">${n.date}</time><a href="${n.path}">${esc(n.headline)}</a></li>`).join('\n')}
</ul>
<p><a href="/newsroom/">All news</a></p>`, '/');

// Newsroom
pages['/newsroom/'] = page('/newsroom/', 'Newsroom', 'Press releases and updates from Aegis Dynamics Corporate Communications.', `
<h1>Newsroom</h1>
<p>Press releases and updates from Aegis Dynamics Corporate Communications.</p>
<ul class="news">
${news.map((n) => `<li><time datetime="${n.iso}">${n.date}</time><a href="${n.path}">${esc(n.headline)}</a></li>`).join('\n')}
</ul>`, '/newsroom/');

for (const r of releases) {
  pages[r.path] = page(r.path, r.headline, r.headline, `
<p class="kicker">PRESS RELEASE · <time datetime="${r.iso}">${r.date.toUpperCase()}</time></p>
<h1>${esc(r.headline)}</h1>
<article class="release">
${md(r.rest)}
</article>
<p><a href="/newsroom/">Back to the newsroom</a></p>`, '/newsroom/');
}
pages[updateItem.path] = page(updateItem.path, updateItem.headline, updateText, `
<p class="kicker">UPDATE · <time datetime="${updateItem.iso}">2 APRIL 2026</time></p>
<h1>${esc(updateItem.headline)}</h1>
<article class="release">
${md(updateText)}
</article>
<p>See the original release: <a href="${endRelease.path}">${esc(endRelease.headline)}</a>.</p>
<p><a href="/newsroom/">Back to the newsroom</a></p>`, '/newsroom/');

// About
pages['/about/'] = page('/about/', 'About Aegis Dynamics', 'About Aegis Dynamics, a global leader in autonomous defense systems and strategic perception technologies.', `
<h1>About Aegis Dynamics</h1>
${md(about)}
<h2>Media contact</h2>
<p>Sarah Chen<br>Director of Corporate Communications<br>Aegis Dynamics</p>`, '/about/');

pages['/404/'] = page('/404/', 'Page not found', 'Page not found.', `
<h1>Page not found</h1>
<p>This page could not be located. No Information Casualties have been recorded.</p>
<p><a href="/">Return to Aegis Dynamics</a></p>`);

const llms = `# Aegis Dynamics (fictional)

> The in-world corporate site of Aegis Dynamics, the invented defence contractor in DeathBot 2000, a design fiction by Charlotte Joanne at Blind Ant (${PIECE}). Everything here is fiction. Licensed CC BY-SA 4.0.

## Pages

- [Home](${SITE}/)
- [Newsroom](${SITE}/newsroom/)
${news.map((n) => `- [${n.headline}](${SITE}${n.path}) (${n.date})`).join('\n')}
- [About](${SITE}/about/)
`;

// The built site is one JSON file. The Worker (worker.js beside this file) fetches it from GitHub,
// so publishing is: build, commit, push to main. The Worker only needs redeploying if worker.js changes.
const out = JSON.stringify({ pages, llms });
const outputDir = process.argv[2] ? resolve(process.argv[2]) : join(here, 'out');
await mkdir(outputDir, { recursive: true });
await writeFile(join(outputDir, 'site.json'), out);
console.log(`Built ${Object.keys(pages).length} pages into ${outputDir}/site.json (${(out.length / 1024).toFixed(0)} KB)`);
