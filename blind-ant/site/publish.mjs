// Publishes the built site straight to Cloudflare: copies the media listed in site/media.json into dist/media/,
// then wrangler uploads dist as the static assets of the blind-ant Worker and deploys it (settings in wrangler.jsonc).
// With `aegis` as its argument it publishes aegisdynamics.blind-ant.com instead (wrangler.aegis.jsonc). Nothing goes to GitHub.
// It signs in to Cloudflare with wrangler's own login (run `npx wrangler login` once), or with an API token in the
// environment as CLOUDFLARE_API_TOKEN or in the file .cloudflare-token (listed in .gitignore, so it is never committed).
import { readFile, mkdir, copyFile } from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const aegis = process.argv[2] === 'aegis';
if (!aegis) {
  const dist = join(root, 'dist');
  const media = JSON.parse(await readFile(join(root, 'site/media.json'), 'utf8'));
  for (const [to, [from]] of Object.entries(media.files)) {
    await mkdir(dirname(join(dist, to)), { recursive: true });
    await copyFile(join(root, from), join(dist, to));
  }
}
const tokenFile = join(root, '.cloudflare-token');
const token = process.env.CLOUDFLARE_API_TOKEN || (existsSync(tokenFile) ? readFileSync(tokenFile, 'utf8').trim() : '');
let source = 'uncommitted-work';
try { source = execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(); } catch {}
const config = aegis ? 'wrangler.aegis.jsonc' : 'wrangler.jsonc';
execFileSync('npx', ['--yes', 'wrangler@4', 'deploy', '--config', config, '--message', `Publish-from-${source}`], {
  cwd: root, stdio: 'inherit', shell: process.platform === 'win32',
  env: token ? { ...process.env, CLOUDFLARE_API_TOKEN: token } : process.env, // no token: wrangler uses its own sign-in (npx wrangler login)
});
console.log(`Published ${aegis ? 'aegisdynamics.blind-ant.com' : 'blind-ant.com'} to Cloudflare (built from ${source})`);
