import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import carrados from '../carrados/worker.js';
import charli from '../charli/worker.js';
import zic from '../zic/worker.js';

const originalRevision = '1d6dcfce7dd8e80b6c1101877021fd8f2449dde2';
const base = 'https://zeroinformationcasualty.org';

test('the specification and published downloads are preserved without rewriting', async () => {
  const original = execFileSync('git', ['show', `${originalRevision}:carrados/content/papers/zic-design-standard.md`], { encoding: 'utf8' });
  assert.equal((await readFile('zic/content/index.md', 'utf8')).replace(/\r\n/g, '\n'), original.replace(/\r\n/g, '\n'));
  for (const version of ['1_5', '1_7']) {
    const name = `Zero_Information_Casualty_v${version}.docx`;
    assert.deepEqual(await readFile(`zic/content/documents/${name}`), execFileSync('git', ['show', `${originalRevision}:carrados/content/documents/${name}`]));
  }
  assert.deepEqual(await readFile('zic/public/styles.css'), await readFile('carrados/public/styles.css'));
});

test('old Carrados addresses redirect without fetching; queries and Markdown survive', async () => {
  for (const [path, expected, headers] of [
    ['/papers/zic-design-standard', '/', {}],
    ['/papers/zic-design-standard/', '/', {}],
    ['/papers/zic-design-standard/index.html', '/', {}],
    ['/papers/zic-design-standard/index.md', '/index.md', {}],
    ['/papers/zic-design-standard/', '/index.md', { accept: 'text/markdown' }],
    ['/documents/Zero_Information_Casualty_v1_5.docx', '/documents/Zero_Information_Casualty_v1_5.docx', {}],
    ['/documents/Zero_Information_Casualty_v1_7.docx', '/documents/Zero_Information_Casualty_v1_7.docx', {}],
    ['/images/zic-v1-5-cover.jpg', '/documents/zic-v1-5-cover.jpg', {}],
  ]) {
    for (const method of ['GET', 'HEAD']) {
      const response = await carrados.fetch(new Request('https://carrados.com' + path + '?source=citation', { method, headers }));
      assert.equal(response.status, 301);
      assert.equal(response.headers.get('location'), base + expected + '?source=citation');
    }
  }
});

test('legacy charli.info ZIC addresses go straight to ZIC', async () => {
  for (const [path, expected] of [
    ['/carrados/zic-design-standard/', '/'],
    ['/carrados/zic-design-standard/index.md', '/index.md'],
    ['/documents/Zero_Information_Casualty_v1_5.docx', '/documents/Zero_Information_Casualty_v1_5.docx'],
    ['/documents/Zero_Information_Casualty_v1_7.docx', '/documents/Zero_Information_Casualty_v1_7.docx'],
  ]) {
    const response = await charli.fetch(new Request('https://charli.info' + path));
    assert.equal(response.status, 301);
    assert.equal(response.headers.get('location'), base + expected);
  }
});

test('new Worker serves the published branch, Markdown, Word files and proper 404s', async () => {
  const saved = globalThis.fetch;
  globalThis.fetch = async (url) => {
    const source = 'https://raw.githubusercontent.com/Carrados/charli.info/zic-site';
    assert.ok(url.startsWith(source));
    try { return new Response(await readFile('dist/zic' + url.slice(source.length))); }
    catch { return new Response('missing', { status: 404 }); }
  };
  try {
    const html = await zic.fetch(new Request(base + '/'));
    assert.equal(html.status, 200);
    assert.match(await html.text(), /rel="canonical" href="https:\/\/zeroinformationcasualty.org\/"/);
    const md = await zic.fetch(new Request(base + '/', { headers: { accept: 'text/markdown' } }));
    assert.match(md.headers.get('content-type'), /text\/markdown/);
    assert.match(await md.text(), /^# Zero Information Casualty/);
    const doc = await zic.fetch(new Request(base + '/documents/Zero_Information_Casualty_v1_7.docx'));
    assert.equal(doc.status, 200);
    assert.match(doc.headers.get('content-type'), /wordprocessingml/);
    assert.equal((await zic.fetch(new Request(base + '/missing/'))).status, 404);
    assert.equal((await zic.fetch(new Request(base + '/', { method: 'POST' }))).status, 405);
    const www = await zic.fetch(new Request('https://www.zeroinformationcasualty.org/?from=www'));
    assert.equal(www.headers.get('location'), base + '/?from=www');
  } finally { globalThis.fetch = saved; }
});

test('generated surfaces identify the new home; Carrados no longer republishes the standard', async () => {
  for (const file of ['llms.txt', 'llms-full.txt', 'robots.txt', 'sitemap.xml', 'chunks.json']) {
    const text = await readFile('dist/zic/' + file, 'utf8');
    assert.ok(text.includes(base), file);
    assert.ok(!text.includes('https://carrados.com/papers/zic-design-standard/'), file);
  }
  const sitemap = await readFile('dist/carrados/sitemap.xml', 'utf8');
  assert.ok(!sitemap.includes('/papers/zic-design-standard/'));
  const home = await readFile('dist/carrados/index.html', 'utf8');
  assert.match(home, /href="https:\/\/zeroinformationcasualty.org\/"/);
});
