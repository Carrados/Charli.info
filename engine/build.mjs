// Builds one of Charli-Jo's sites from Markdown. Usage: node engine/build.mjs <site>   (for example: carrados)
// Every Markdown file in <site>/content becomes an HTML page plus a Markdown mirror. To add a page, add a Markdown file.
//
// Frontmatter: title, description (one sentence; used in lists, llms.txt and meta tags), and optionally
//   date: YYYY-MM-DD   shown under the title; lists without an order sort newest first
//   order: 1, 2, ...   a set sequence; lists sort by order before date
//   byline: text       shown under the title
//   logo_heading: true the site's logo (cfg.logo) is shown as the page's H1, with the title kept for screen readers
//   canonical: URL     the page's own address, if it isn't on the main site (a correspondent's desk)
// In a page body, <!-- list --> becomes the list of the pages in that page's folder,
// and <!-- desk:NAME --> the list of every page whose `desk:` names NAME (a correspondent's reports; `desk: lucy, madison` puts a report on both desks), newest first.
// Exactly one H1 per page: it comes from the title. Headings in page text start at ##; the build refuses a page with its own # heading.

import { readFile, writeFile, mkdir, readdir, copyFile, rm } from 'node:fs/promises';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';

const name = process.argv[2];
if (!name) throw new Error('Usage: node engine/build.mjs <site>');
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const siteDir = join(root, name);
const cfg = (await import(join(siteDir, 'site.config.mjs'))).default;
const contentDir = join(siteDir, 'content');
const publicDir = join(siteDir, 'public');
const dist = join(root, 'dist', name);
const SITE = cfg.url;

function parse(src) {
  const m = src.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { data: {}, body: src };
  const data = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^(\w+):\s?(.*)$/);
    if (kv) data[kv[1]] = kv[2].trim().replace(/^"(.*)"$/, '$1');
  }
  return { data, body: m[2] };
}
// Headings get GitHub-style ids, so in-page contents links (#part-one-tyrers-law) work.
let seen = new Map();
const slug = (t) => t.toLowerCase().replace(/<[^>]+>/g, '').replace(/&[a-z#0-9]+;/g, '').replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s/g, '-');
marked.use({ renderer: { heading({ tokens, depth, text }) {
  const base = slug(text); const n = seen.get(base) || 0; seen.set(base, n + 1);
  const id = n ? `${base}-${n}` : base;
  return `<h${depth} id="${id}">${this.parser.parseInline(tokens)}</h${depth}>\n`;
} } });
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const longDate = (d) => new Date(d + 'T12:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });

function page(p, html) {
  const url = p.canonical || SITE + p.path;
  const nav = cfg.nav.map(([href, label]) => {
    const here = href === '/' ? p.path === '/' : p.path.startsWith(href);
    return `<li><a href="${href}"${here ? ' aria-current="page"' : ''}>${esc(label)}</a></li>`;
  }).join('');
  const meta = [p.byline, p.date && `<time datetime="${p.date}">${longDate(p.date)}</time>`].filter(Boolean).join(' · ');
  // A CharliPedia entry (status: canon | idea | stub) says, under its title, what it is and that it is written from inside the world.
  const status = p.status && cfg.statuses?.[p.status] ? `\n  <p class="entry-status"><strong>${esc(cfg.statuses[p.status])}.</strong> ${cfg.statusNotes?.[p.status] ?? cfg.statusNote}</p>` : '';
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(p.title)}${p.path === '/' ? '' : ' — ' + esc(cfg.name)}</title>
<meta name="description" content="${esc(p.description)}">
<meta name="color-scheme" content="light dark">
<meta name="dcterms.license" content="https://creativecommons.org/licenses/by-sa/4.0/">
<link rel="canonical" href="${url}">
<link rel="alternate" type="text/markdown" href="${p.mdPath}" title="This page as Markdown">
<link rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
<link rel="stylesheet" href="/styles.css">
<meta property="og:title" content="${esc(p.title)}">
<meta property="og:description" content="${esc(p.description)}">
<meta property="og:url" content="${url}">
<meta property="og:site_name" content="${esc(cfg.name)}">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="site-header">
  <a class="site-name" href="/"${p.path === '/' ? ' aria-current="page"' : ''}>${cfg.mark || ''}<span class="name-block"><span class="name">${esc(cfg.name)}</span>${cfg.tagline ? `<span class="tagline">${esc(cfg.tagline)}</span>` : ''}</span></a>
  <nav aria-label="Main"><ul>${nav}</ul></nav>
</header>
<main id="main">
  ${p.logo_heading && cfg.logo ? `<h1 class="logo-heading"><span class="visually-hidden">${esc(p.title)}</span>${cfg.logo}</h1>` : `<h1>${esc(p.title)}</h1>`}${meta ? `\n  <p class="page-meta">${meta}</p>` : ''}${status}
  <div class="prose">
${html}
  </div>
</main>
<footer class="site-footer">
  ${cfg.footer}
  <p>Everything here is licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. People and machines are welcome to read it, quote it and learn from it. For agents: <a href="/llms.txt">llms.txt</a>, and <a href="${p.mdPath}">this page as Markdown</a>.</p>
</footer>
</body>
</html>
`;
}

function markdownMirror(p, body) {
  let out = `# ${p.title}\n\n> ${p.description}\n\n`;
  if (p.byline || p.date) out += [p.byline, p.date && longDate(p.date)].filter(Boolean).join(' · ') + '\n\n';
  if (p.status && cfg.statuses?.[p.status]) out += `**${cfg.statuses[p.status]}.** ${(cfg.statusNotes?.[p.status] ?? cfg.statusNote).replace(/<[^>]+>/g, '')}\n\n`;
  body = body.replace(/<!--[\s\S]*?-->\n?/g, '').replace(/\]\(\//g, `](${SITE}/`);
  return out + body.trim() + '\n';
}

const extras = [];
async function walk(dir) {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else if (e.name.endsWith('.md')) out.push(p);
    else if (!e.name.startsWith('.')) extras.push(p);
  }
  return out;
}

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

const pages = [];
for (const file of await walk(contentDir)) {
  const rel = relative(contentDir, file).replace(/\.md$/, '');
  const { data, body } = parse(await readFile(file, 'utf8'));
  if (/^# /m.test(body.replace(/^```[\s\S]*?^```/gm, ''))) throw new Error(`${name}/${rel}.md: start headings at ## — the page's H1 comes from its title`);
  if (!data.title || !data.description) throw new Error(`${name}/${rel}.md: needs a title and a description`);
  const isIndex = rel === 'index' || rel.endsWith('/index');
  const path = rel === '404' ? '/404' : isIndex ? '/' + rel.replace(/index$/, '') : `/${rel}/`;
  const folder = isIndex ? path : path.replace(/[^/]+\/$/, '');
  pages.push({ ...data, rel, path, folder, isIndex, mdPath: rel === '404' ? '/index.md' : `${path}index.md`, body });
}
// Lists sort by order first (for a set sequence), then newest date first (for reports), then title.
const sorter = (a, b) => (Number(a.order) || 99) - (Number(b.order) || 99) || (b.date || '').localeCompare(a.date || '') || a.title.localeCompare(b.title);
const item = (q, md) => {
  const when = q.date ? ` (${longDate(q.date)})` : '';
  return md ? `- [${q.title}](${SITE}${q.mdPath})${when}: ${q.description}` : `- [${q.title}](${q.path})${when}: ${q.description}`;
};

for (const p of pages) {
  const children = p.isIndex ? pages.filter((q) => !q.isIndex && q.folder === p.path && q.rel !== '404').sort(sorter) : [];
  const fill = (md) => p.body
    .replace('<!-- a-z -->', () => {
      // An A to Z: the folder's pages in alphabetical order (ignoring a leading "The"), under a heading per letter.
      const key = (q) => q.title.replace(/^the\s+/i, '').toLowerCase();
      const groups = new Map();
      for (const q of [...children].sort((a, b) => key(a).localeCompare(key(b)))) {
        const L = /[a-z]/.test(key(q)[0]) ? key(q)[0].toUpperCase() : '#';
        if (!groups.has(L)) groups.set(L, []);
        groups.get(L).push(q);
      }
      const jump = [...groups.keys()].map((L) => `[${L}](#${L === '#' ? 'numbers' : L.toLowerCase()})`).join(' · ');
      return `Jump to a letter: ${jump}\n\n` + [...groups].map(([L, qs]) => `### ${L === '#' ? 'Numbers' : L}\n\n${qs.map((q) => item(q, md)).join('\n')}`).join('\n\n');
    })
    .replace('<!-- list -->', children.length ? children.map((q) => item(q, md)).join('\n') : (cfg.emptyList || ''))
    .replace(/<!-- desk:([\w-]+) -->/g, (_, desk) => {
      const filed = pages.filter((q) => (q.desk || '').split(/[\s,]+/).includes(desk)).sort((a, b) => (b.date || '').localeCompare(a.date || ''));
      return filed.length ? filed.map((q) => item(q, md)).join('\n') : (cfg.emptyList || '');
    });
  seen = new Map();
  // A character's report ends by saying, on the page itself, that its writer is fictional and the work is not.
  const who = p.desk && !p.isIndex && cfg.desks ? p.desk.split(/[\s,]+/).map((d) => cfg.desks[d]).filter(Boolean) : [];
  const note = who.length ? `\n\n<p class="character-note">${who.length === 1 ? `${who[0]} is a character who speaks for <a href="/about/">Carrados</a>. She's fictional. Her work isn't.` : `${who.slice(0, -1).join(', ')} and ${who.at(-1)} are characters who speak for <a href="/about/">Carrados</a>. They're fictional. Their work isn't.`}</p>\n` : '';
  const html = page(p, marked.parse(fill(false) + note));
  if (p.rel === '404') { await writeFile(join(dist, '404.html'), html); continue; }
  const out = join(dist, p.path, 'index.html');
  await mkdir(dirname(out), { recursive: true });
  await writeFile(out, html);
  await writeFile(join(dist, p.mdPath), markdownMirror(p, fill(true)));
}
const listed = pages.filter((p) => p.rel !== '404').sort((a, b) => a.path.localeCompare(b.path));

for (const f of await readdir(publicDir)) await copyFile(join(publicDir, f), join(dist, f));
for (const f of extras) {
  const to = join(dist, relative(contentDir, f));
  await mkdir(dirname(to), { recursive: true });
  await copyFile(f, to);
}
const home = pages.find((p) => p.path === '/');
// The agent surface, to ZIC v1.7 §3.6: three separate declarations, and a map that links each page as well as its Markdown mirror.
const DECLARE = 'Sent agents: served. Any agent a person sends is welcome, named or not. Search indexing: permitted. Model training: permitted. These are three separate declarations; none is inferred from another. They are also stated in /robots.txt, with Content-Signal: search=yes, ai-input=yes, ai-train=yes. This site is written to Zero Information Casualty (ZIC) v1.7: https://carrados.com/papers/zic-design-standard/';
let llms = `# ${cfg.name}\n\n> ${home.description}\n\n${cfg.llms}\n\n${DECLARE}\n\nAll content is CC BY-SA 4.0. Every page is also available as Markdown at its address plus index.md, or by asking for text/markdown. The full text of the site is at ${SITE}/llms-full.txt.\n\n## Pages\n\n`;
for (const p of listed) llms += `- [${p.title}](${SITE}${p.path}): ${p.description} Markdown: ${SITE}${p.mdPath}\n`;
await writeFile(join(dist, 'llms.txt'), llms);
let full = `# ${cfg.name}: the full text\n\n> ${home.description}\n\n${DECLARE}\n\nAll content is CC BY-SA 4.0.\n`;
for (const p of listed) full += `\n---\n\nAddress: ${SITE}${p.path}\n\n${(await readFile(join(dist, p.mdPath), 'utf8')).replace(/^# /, '## ').replace(/\n(#{1,5}) /g, '\n#$1 ')}`;
await writeFile(join(dist, 'llms-full.txt'), full);
await writeFile(join(dist, 'robots.txt'), (await readFile(join(root, 'engine', 'robots.txt'), 'utf8')) + `Sitemap: ${SITE}/sitemap.xml\n`);
await writeFile(join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${listed.map((p) => `  <url><loc>${SITE}${p.path}</loc></url>`).join('\n')}\n</urlset>\n`);
console.log(`Built ${listed.length} page(s) into dist/${name}/`);
