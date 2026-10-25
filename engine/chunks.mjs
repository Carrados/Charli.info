// Writes chunks.json: every published page's Markdown copy, cut into passages of about 250 words,
// for the CharliVerse vector index (read by the charliverse-indexer Worker; see CLAUDE.md).
// Usage: node chunks.mjs <distDir> <baseUrl> <siteLabel> [<pathPrefix>=<label> ...]
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join, relative, sep } from 'node:path';
import { createHash } from 'node:crypto';

const [dist, base, label, ...rules] = process.argv.slice(2);
const prefixes = rules.map((r) => r.split('='));
const sha = (s) => createHash('sha1').update(s).digest('hex');
const WORDS = 250, LINE_MIN = 15, LINE_MAX = 70;

async function walk(dir) {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else if (e.name.endsWith('.md')) out.push(p);
  }
  return out;
}
const clean = (s) => s
  .replace(/<img[^>]*alt="([^"]*)"[^>]*>/g, ' [Picture: $1] ')
  .replace(/<audio[^>]*>.*?<\/audio>/gs, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/!\[([^\]]*)\]\([^)]*\)/g, ' [Picture: $1] ')
  .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
  .replace(/^> ?/gm, '')
  .replace(/[*_`]+/g, '')
  .replace(/[ \t]+/g, ' ');

const chunks = [];
for (const file of await walk(dist)) {
  const rel = relative(dist, file).split(sep).join('/');
  if (rel === '404.md' || rel.startsWith('404')) continue;
  const path = '/' + rel.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '/');
  const src = (await readFile(file, 'utf8')).replace(/\r\n?/g, '\n');
  const title = (src.match(/^# (.+)$/m) || [, path])[1].trim();
  let site = label;
  for (const [pre, lab] of prefixes) if (path.startsWith(pre)) site = lab;
  const body = src.replace(/^# .+$/m, '');
  const sections = body.split(/\n(?=#{2,4} )/);
  let n = 0;
  for (const sec of sections) {
    const hm = sec.match(/^#{2,4} (.+)$/m);
    const heading = hm && sec.trimStart().startsWith('#') ? hm[1].trim() : '';
    const paras = clean(sec.replace(/^#{2,4} .+$/m, '')).split(/\n\s*\n/).map((p) => p.replace(/\s+/g, ' ').trim()).filter(Boolean);
    let buf = [];
    const flush = () => {
      const text = buf.join('\n\n').trim();
      if (text.split(' ').length >= 8) {
        const k = n++;
        const id = sha(`${site}${path}#${k}`);
        chunks.push({ id, kind: 'passage', hash: sha(title + heading + text), site, title, url: base + path, heading, text });
        // Lines: the same text in short pieces (about 15 to 70 words), so a single line of dialogue or a
        // passing detail can be found on its own instead of being drowned by the rest of its passage.
        if (text.split(' ').length > LINE_MAX) {
          let line = [], j = 0;
          const push = () => {
            const t = line.join(' ').trim();
            if (t.split(' ').length >= 6) chunks.push({ id: sha(`${site}${path}#${k}L${j++}`), kind: 'line', passage: id, hash: sha(title + heading + t), site, title, url: base + path, heading, text: t });
            line = [];
          };
          for (const para of buf) {
            const w = para.split(' ');
            if (w.length > LINE_MAX) { push(); for (let i = 0; i < w.length; i += LINE_MAX - 20) { line = [w.slice(i, i + LINE_MAX).join(' ')]; push(); } continue; }
            if (line.join(' ').split(' ').length + w.length > LINE_MAX) push();
            line.push(para);
            if (line.join(' ').split(' ').length >= LINE_MIN) push();
          }
          push();
        }
      }
      buf = [];
    };
    for (const p of paras) {
      const words = p.split(' ');
      if (words.length > WORDS * 1.5) { flush(); for (let i = 0; i < words.length; i += WORDS) { buf = [words.slice(i, i + WORDS).join(' ')]; flush(); } continue; }
      if (buf.join(' ').split(' ').length + words.length > WORDS) flush();
      buf.push(p);
    }
    flush();
  }
}
await writeFile(join(dist, 'chunks.json'), JSON.stringify({ updated: new Date().toISOString(), count: chunks.length, chunks }));
console.log(`Wrote ${chunks.length} passages to ${join(dist, 'chunks.json')}`);
