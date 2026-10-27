// Builds the Blind Ant site into dist/.
// Every Markdown file in site/content becomes an HTML page and a Markdown mirror.
// To add a page, add a Markdown file. Nothing else needs to change.
//
// Frontmatter keys:
//   title, description          every page
//   kind: piece | object        a Piece is listed on the front page; an Object is listed on its Piece
//   order: 1, 2, ...            the order Objects appear in on their Piece
//   label_title, label_meta, label   an optional wall label at the top of the page
//
// In a page body, <!-- pieces --> becomes the list of Pieces, <!-- latest:N --> the N newest Pieces (highest order first),
// <!-- pieces-a-z --> every Piece in alphabetical order under a heading per letter, and <!-- objects --> the list of this Piece's Objects.
// When a Piece has exactly one Object, "## Objects" and its marker are replaced by the Object itself.

import { readFile, writeFile, mkdir, readdir, copyFile, rm } from 'node:fs/promises';
import { join, dirname, relative, sep, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';

// A list item that is a single paragraph is written without the <p>, so screen readers don't announce its marker twice.
const tight = (h) => h.replace(/<li><p>((?:(?!<\/?p[ >])[\s\S])*?)<\/p>\s*<\/li>/g, '<li>$1</li>');


// Headings get GitHub-style ids, so in-page links (such as the A to Z's letter links) work.
let seen = new Map();
const slug = (t) => t.toLowerCase().replace(/<[^>]+>/g, '').replace(/&[a-z#0-9]+;/g, '').replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s/g, '-');
marked.use({ renderer: { heading({ tokens, depth, text }) {
  const base = slug(text); const n = seen.get(base) || 0; seen.set(base, n + 1);
  const id = n ? `${base}-${n}` : base;
  return `<h${depth} id="${id}">${this.parser.parseInline(tokens)}</h${depth}>\n`;
} } });

const SITE = 'https://blind-ant.com';
const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const contentDir = join(here, 'content');
const publicDir = join(here, 'public');
const dist = process.argv[2] ? resolve(process.argv[2]) : join(root, 'dist');

// Minimal frontmatter: key: value, and key: | for indented blocks.
function parse(src) {
  src = src.replace(/\r\n?/g, '\n'); // files saved on Windows have CRLF line endings
  const m = src.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { data: {}, body: src };
  const data = {};
  const lines = m[1].split('\n');
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^(\w+):\s?(.*)$/);
    if (!kv) continue;
    if (kv[2] === '|') {
      const block = [];
      while (i + 1 < lines.length && (lines[i + 1].startsWith('  ') || lines[i + 1] === '')) {
        block.push(lines[++i].replace(/^  /, ''));
      }
      data[kv[1]] = block.join('\n').trim();
    } else data[kv[1]] = kv[2].trim();
  }
  return { data, body: m[2] };
}

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Every page has exactly one H1: the wall label's title if there is a label, otherwise the page title.
const heading = (d) => d.label_title || d.title;

function wallLabel(d, jump) {
  if (!d.label) return `\n  <h1 class="page-title">${esc(d.title)}</h1>`;
  const paras = d.label.split(/\n\s*\n/).map((p) => `<p>${esc(p.trim())}</p>`).join('\n      ');
  return `
  <figure class="wall-label${d.label.length > 280 ? ' long' : ''}" aria-labelledby="label-title">
    <figcaption>
      <h1 class="label-title" id="label-title">${esc(heading(d))}</h1>
      <p class="label-meta">${esc(d.label_meta)}</p>${jump ? `\n      <p class="jump"><a href="#the-work">${jump}</a></p>` : ''}
    </figcaption>
    <div class="label-body" id="label-body">
      ${paras}
    </div>
  </figure>`;
}

function trail(p) {
  if (!p.parent) return '';
  return `\n  <p class="trail"><a href="${p.parent.path}">${esc(p.parent.title)}</a>, a Piece</p>`;
}

// Pictures whose alt text points back to the wall label get aria-describedby, so someone moving from picture
// to picture still hears the full description. A long label gets a link straight to the work it describes.
function wire(d, html) {
  if (!d.label) return { html, jump: '' };
  html = html.replace(/<img(?![^>]*aria-describedby)([^>]*\balt="[^"]*\babove\b[^"]*")/gi, '<img aria-describedby="label-body"$1');
  let jump = '';
  if (d.label.length > 280) {
    const m = html.match(/<(img|video)\b/);
    if (m) {
      jump = m[1] === 'video' ? 'Go straight to the film' : 'Go straight to the picture';
      html = html.replace(/<(img|video)\b/, '<$1 id="the-work"');
    }
  }
  return { html, jump };
}

function page(p, rawHtml) {
  const d = p;
  const { html, jump } = wire(d, rawHtml);
  const url = SITE + p.path;
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(d.title)}${p.path === '/' ? '' : ' — Blind Ant'}</title>
<meta name="description" content="${esc(d.description)}">
<meta name="color-scheme" content="light dark">
<meta name="dcterms.license" content="https://creativecommons.org/licenses/by-sa/4.0/">
<link rel="canonical" href="${url}">
<link rel="alternate" type="text/markdown" href="${p.mdPath}" title="This page as Markdown">
<link rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
<link rel="stylesheet" href="/styles.css">
<meta property="og:title" content="${esc(d.title)}">
<meta property="og:description" content="${esc(d.description)}">
<meta property="og:url" content="${url}">
<meta property="og:site_name" content="Blind Ant">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="site-header">
  <a class="site-name" href="/">Blind Ant</a>
  <nav aria-label="Site"><a href="/pieces/"${p.path === '/pieces/' ? ' aria-current="page"' : ''}>All Pieces</a></nav>
</header>
<main id="main">${trail(p)}
${wallLabel(d, jump)}
  <div class="prose">
${html}
  </div>
</main>
<footer class="site-footer">
  <p>Blind Ant is run by Charlotte Joanne, and is part of <a href="https://charli.info/">the CharliVerse</a>. To get in touch, write to <a href="mailto:charlotte.joanne@blind-ant.com">charlotte.joanne@blind-ant.com</a>.</p>
  <p>Everything here is licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. People and machines are welcome to read it, quote it and learn from it. For agents: <a href="/llms.txt">llms.txt</a>, and <a href="${p.mdPath}">this page as Markdown</a>.</p>
</footer>
</body>
</html>
`;
}

// Markdown mirror: the same page for readers that prefer plain text. Relative links are made absolute.
function markdownMirror(p, body) {
  let out = `# ${heading(p)}\n\n> ${p.description}\n\n`;
  if (p.parent) out += `Part of [${p.parent.title}](${SITE}${p.parent.mdPath}), a Piece.\n\n`;
  if (p.label) out += `${p.label_meta}\n\n${p.label}\n\n`;
  body = body.replace(/<!--[\s\S]*?-->\n?/g, '').replace(/\]\(\//g, `](${SITE}/`);
  return out + body.trim() + '\n';
}

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
// Anything in site/content that isn't a page (a picture, a PDF) is published at the same path, beside its page.
const extras = [];

const listItem = (p, md) =>
  md ? `- [${p.title}](${SITE}${p.mdPath}): ${p.description}` : `- [${p.title}](${p.path}): ${p.description}`;

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

// First pass: read every page.
const pages = [];
for (const file of await walk(contentDir)) {
  const rel = relative(contentDir, file).split(sep).join('/').replace(/\.md$/, ''); // forward slashes on Windows too
  const { data, body } = parse(await readFile(file, 'utf8'));
  if (/^# /m.test(body)) throw new Error(`${rel}.md: start headings at ## — the page's H1 comes from its title or wall label`);
  const isIndex = rel === 'index' || rel.endsWith('/index');
  const path = rel === '404' ? '/404' : isIndex ? '/' + rel.replace(/index$/, '') : `/${rel}/`;
  pages.push({ ...data, rel, path, mdPath: rel === '404' ? '/index.md' : `${path}index.md`, body });
}
for (const p of pages) {
  if (p.kind !== 'object') continue;
  const parentPath = p.path.replace(/[^/]+\/$/, '');
  p.parent = pages.find((q) => q.path === parentPath);
}
const byOrder = (a, b) => (Number(a.order) || 99) - (Number(b.order) || 99) || a.title.localeCompare(b.title);
const pieces = pages.filter((p) => p.kind === 'piece').sort(byOrder);

// Second pass: write them.
for (const p of pages) {
  const objects = pages.filter((q) => q.parent === p).sort(byOrder);
  const fill = (md) =>
    p.body
      .replace('<!-- pieces -->', pieces.map((q) => listItem(q, md)).join('\n'))
      .replace(/<!-- latest:(\d+) -->/, (_, n) => [...pieces].reverse().slice(0, Number(n)).map((q) => listItem(q, md)).join('\n'))
      .replace('<!-- pieces-a-z -->', () => {
        // Alphabetical, ignoring a leading "The" and letter case, under a level 3 heading per letter.
        const key = (q) => q.title.replace(/^the\s+/i, '').toLowerCase();
        const groups = new Map();
        for (const q of [...pieces].sort((a, b) => key(a).localeCompare(key(b)))) {
          const L = /[a-z]/.test(key(q)[0]) ? key(q)[0].toUpperCase() : '#';
          if (!groups.has(L)) groups.set(L, []);
          groups.get(L).push(q);
        }
        const id = (L) => (L === '#' ? 'numbers' : L.toLowerCase());
        const jump = [...groups.keys()].map((L) => `[${L}](#${id(L)})`).join(' · ');
        return `Jump to a letter: ${jump}\n\n` + [...groups].map(([L, qs]) => `### ${L === '#' ? 'Numbers' : L}\n\n${qs.map((q) => listItem(q, md)).join('\n')}`).join('\n\n');
      })
      .replace(/## Objects\s*\n\s*<!-- objects -->/, (all) => {
        // A Piece with a single Object shows that Object on the Piece page itself, so readers skip a click.
        // The Object keeps its own page too, so links to it still work.
        if (objects.length !== 1) return all;
        const q = objects[0];
        const same = (x) => x && (x.trim() === (p.label || '').trim() || x.trim() === (p.description || '').trim());
        const label = q.label && !same(q.label) ? `${q.label_meta ? `*${q.label_meta}*\n\n` : ''}${q.label.trim()}\n\n` : (q.label_meta ? `*${q.label_meta}*\n\n` : '');
        const body = q.body.replace(/^(#{2,5}) /gm, '#$1 ');
        return `## ${q.title === p.title ? "In full" : q.title}\n\n${label}${body.trim()}`;
      })
      .replace('<!-- objects -->', objects.map((q) => listItem(q, md)).join('\n'));
  seen = new Map();
  const html = page(p, tight(marked.parse(fill(false))));
  if (p.rel === '404') {
    await writeFile(join(dist, '404.html'), html);
    continue;
  }
  const htmlOut = join(dist, p.path, 'index.html');
  await mkdir(dirname(htmlOut), { recursive: true });
  await writeFile(htmlOut, html);
  await writeFile(join(dist, p.mdPath), markdownMirror(p, fill(true)));
}
const listed = pages.filter((p) => p.rel !== '404').sort((a, b) => a.path.localeCompare(b.path));

// Static files, and files that sit beside pages
for (const f of await readdir(publicDir)) await copyFile(join(publicDir, f), join(dist, f));
for (const f of extras) {
  const to = join(dist, relative(contentDir, f));
  await mkdir(dirname(to), { recursive: true });
  await copyFile(f, to);
}

// llms.txt
const home = pages.find((p) => p.path === '/');
// The agent surface, to ZIC v1.7 §3.6: three separate declarations, and a map that links each page as well as its Markdown mirror.
const DECLARE = 'Sent agents: served. Any agent a person sends is welcome, named or not. Search indexing: permitted. Model training: permitted. These are three separate declarations; none is inferred from another. They are also stated in /robots.txt, with Content-Signal: search=yes, ai-input=yes, ai-train=yes. This site is written to Zero Information Casualty (ZIC) v1.7: https://carrados.com/papers/zic-design-standard/';
let llms = `# Blind Ant\n\n> ${home.description}\n\nBlind Ant is the design fiction practice of Charlotte Joanne, its author and operator. It is part of the CharliVerse (https://charli.info/). Contact: charlotte.joanne@blind-ant.com.\n\n${DECLARE}\n\nAll content is CC BY-SA 4.0. Every page is also available as Markdown at its address plus index.md, or by asking for text/markdown.\n\n## Pages\n\n`;
for (const p of listed) llms += `- [${p.title}](${SITE}${p.path}): ${p.description} Markdown: ${SITE}${p.mdPath}\n`;
await writeFile(join(dist, 'llms.txt'), llms);

// sitemap
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${listed.map((p) => `  <url><loc>${SITE}${p.path}</loc></url>`).join('\n')}\n</urlset>\n`;
await writeFile(join(dist, 'sitemap.xml'), sitemap);

console.log(`Built ${listed.length} page(s) into ${dist}/`);
