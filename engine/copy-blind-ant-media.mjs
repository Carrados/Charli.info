// Copy only the seven public media files listed by the Blind Ant publisher.
import { readFile, mkdir, copyFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const source = resolve(root, 'blind-ant');
const output = resolve(root, 'dist/blind-ant');
const { files } = JSON.parse(await readFile(resolve(source, 'site/media.json'), 'utf8'));
for (const [url, [from]] of Object.entries(files)) {
  const target = resolve(output, url.replace(/^\//, ''));
  await mkdir(dirname(target), { recursive: true });
  await copyFile(resolve(source, from), target);
}
console.log(`Copied ${Object.keys(files).length} public Blind Ant media files.`);
