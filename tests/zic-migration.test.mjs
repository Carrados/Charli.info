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
  // v1.7 moved to its own page (zic/content/1.7.md) when v1.8 took the home page. Every section heading of the original
  // v1.7 must still be on that page, so section links keep working, and every one except its changelog must be in v1.8,
  // which preserves section numbering.
  const v17 = (await readFile('zic/content/1.7.md', 'utf8')).replace(/\r\n/g, '\n');
  const now = (await readFile('zic/content/index.md', 'utf8')).replace(/\r\n/g, '\n');
  for (const text of [v17, now]) { assert.ok(!text.includes('C J Tyrer')); assert.ok(!text.includes('example.org/zic')); }
  for (const heading of original.replace(/\r\n/g, '\n').split('\n').filter((line) => /^#{2,3} /.test(line))) {
    assert.ok(v17.includes('\n' + heading + '\n'), heading);
    if (heading !== '## Changes in v1.7') assert.ok(now.includes('\n' + heading + '\n'), heading);
  }
  // Part Eight: every identifier is unique and well formed.
  const ids = [...now.matchAll(/^#### (ZIC-[0-9.]+-\d\d): /gm)].map((m) => m[1]);
  assert.ok(ids.length >= 63);
  assert.equal(new Set(ids).size, ids.length);
  // The Word renderings were corrected on 15 November 2026 (author's name, British English, titles, the v1.7 Preamble heading),
  // so they no longer match the files that moved from Carrados byte for byte. They must still be Word files that open.
  for (const version of ['1_5', '1_6', '1_7', '1_8']) {
    const file = await readFile(`zic/content/documents/Zero_Information_Casualty_v${version}.docx`);
    assert.equal(file.subarray(0, 2).toString(), 'PK');
    assert.ok(file.length > 40000);
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

test('new Worker serves its own static assets, Markdown, Word files and proper 404s', async () => {
  const env = { ASSETS: { async fetch(request) {
    try { return new Response(await readFile('dist/zic' + decodeURIComponent(new URL(request.url).pathname))); }
    catch { return new Response('missing', { status: 404 }); }
  } } };
  {
    const html = await zic.fetch(new Request(base + '/'), env);
    assert.equal(html.status, 200);
    assert.match(await html.text(), /rel="canonical" href="https:\/\/zeroinformationcasualty.org\/"/);
    const md = await zic.fetch(new Request(base + '/', { headers: { accept: 'text/markdown' } }), env);
    assert.match(md.headers.get('content-type'), /text\/markdown/);
    assert.match(await md.text(), /^# Zero Information Casualty/);
    const doc = await zic.fetch(new Request(base + '/documents/Zero_Information_Casualty_v1_7.docx'), env);
    assert.equal(doc.status, 200);
    assert.match(doc.headers.get('content-type'), /wordprocessingml/);
    // Every version keeps its own address. v1.7 is a page of its own; /1.8/ serves the current specification, as a page and as Markdown.
    const versioned = await zic.fetch(new Request(base + '/1.7/'), env);
    assert.equal(versioned.status, 200);
    assert.match(await versioned.text(), /<h1>Zero Information Casualty \(ZIC\) v1\.7<\/h1>/);
    assert.match(await (await zic.fetch(new Request(base + '/1.8/'), env)).text(), /<h1>Zero Information Casualty \(ZIC\) v1\.8<\/h1>/);
    assert.match(await (await zic.fetch(new Request(base + '/1.8/index.md'), env)).text(), /^# Zero Information Casualty \(ZIC\) v1\.8/);
    assert.match(await (await zic.fetch(new Request(base + '/1.7/index.md'), env)).text(), /^# Zero Information Casualty/);
    assert.equal((await zic.fetch(new Request(base + '/1.7?x=1'), env)).headers.get('location'), base + '/1.7/?x=1');
    // Earlier versions are pages at their own addresses, marked as superseded, and kept out of the one-file full text.
    for (const v of ['1.5', '1.6', '1.7']) {
      const page = await (await zic.fetch(new Request(`${base}/${v}/`), env)).text();
      assert.match(page, new RegExp(`<h1>Zero Information Casualty \\(ZIC\\) v${v.replace('.', '\\.')}</h1>`));
      assert.match(page, /It has been superseded/);
      assert.equal((await zic.fetch(new Request(`${base}/${v}`), env)).headers.get('location'), `${base}/${v}/`);
    }
    assert.ok(!(await readFile('dist/zic/llms-full.txt', 'utf8')).includes('Changes in v1.6\n'));
    assert.equal((await zic.fetch(new Request(base + '/missing/'), env)).status, 404);
    assert.equal((await zic.fetch(new Request(base + '/', { method: 'POST' }), env)).status, 405);
    const www = await zic.fetch(new Request('https://www.zeroinformationcasualty.org/?from=www'), env);
    assert.equal(www.headers.get('location'), base + '/?from=www');
  }
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

test('the ZIC skill download is packed from its folder and served as a zip', async () => {
  // The site serves the committed zip, so it must match zic/skill/zic-1-7/ (python3 zic/skill/pack.py rebuilds it).
  execFileSync('python3', ['zic/skill/pack.py', '--check']);
  const env = { ASSETS: { async fetch(request) {
    try { return new Response(await readFile('dist/zic' + decodeURIComponent(new URL(request.url).pathname))); }
    catch { return new Response('missing', { status: 404 }); }
  } } };
  const zip = await zic.fetch(new Request(base + '/documents/zic-1-7-skill.zip'), env);
  assert.equal(zip.status, 200);
  assert.equal(zip.headers.get('content-type'), 'application/zip');
  assert.match(await (await zic.fetch(new Request(base + '/skill/'), env)).text(), /<h1>The ZIC skill for agents<\/h1>/);
});
