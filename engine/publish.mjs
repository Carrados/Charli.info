// Publishes a built site straight to Cloudflare: wrangler uploads dist/<site>/ as the static assets of that site's
// Worker and deploys the Worker (settings in wrangler.<site>.jsonc). Nothing goes to GitHub.
// Run with: npm run publish:<site>. It signs in to Cloudflare with wrangler's own login (run `npx wrangler login` once), or with an API token
// in the environment as CLOUDFLARE_API_TOKEN or in the file .cloudflare-token (listed in .gitignore, so it is never committed).
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const name = process.argv[2];
if (!name) throw new Error('Usage: node engine/publish.mjs <site>');
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const tokenFile = join(root, '.cloudflare-token');
const token = process.env.CLOUDFLARE_API_TOKEN || (existsSync(tokenFile) ? readFileSync(tokenFile, 'utf8').trim() : '');
let source = 'uncommitted-work';
try { source = execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(); } catch {}
execFileSync('npx', ['--yes', 'wrangler@4', 'deploy', '--config', `wrangler.${name}.jsonc`, '--message', `Publish-${name}-from-${source}`], {
  cwd: root, stdio: 'inherit', shell: process.platform === 'win32',
  env: token ? { ...process.env, CLOUDFLARE_API_TOKEN: token } : process.env, // no token: wrangler uses its own sign-in (npx wrangler login)
});
console.log(`Published ${name} to Cloudflare (built from ${source})`);
