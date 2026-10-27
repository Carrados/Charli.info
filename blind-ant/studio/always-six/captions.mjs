// Writes out/captions.vtt: captions for the described film. The only sound in it is the spoken description,
// so the captions are the description's own lines and timings, marked as captions. Run: node captions.mjs
import { readFile, writeFile } from 'node:fs/promises';
const src = await readFile(new URL('./out/description.vtt', import.meta.url), 'utf8');
const out = src
  .replace(/^Kind: descriptions$/m, 'Kind: captions')
  .replace(/^NOTE .*$/m, 'NOTE Always Six: captions for the voiced description, the only sound in the film');
await writeFile(new URL('./out/captions.vtt', import.meta.url), out);
console.log('Wrote out/captions.vtt');
