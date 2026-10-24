// Publishes a built site: pushes dist/<site>/ as the `<site>-site` branch, which that site's Worker serves.
// Run with: npm run publish:<site>
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const name = process.argv[2];
if (!name) throw new Error('Usage: node engine/publish.mjs <site>');
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist', name);
const branch = `${name}-site`;
const git = (args, opts = {}) => execFileSync('git', args, { cwd: root, encoding: 'utf8', ...opts }).trim();
const source = git(['rev-parse', '--short', 'HEAD']);
const env = { ...process.env, GIT_INDEX_FILE: join(root, '.git', `${name}-index`) };
git(['--work-tree', dist, 'add', '-A', '.'], { env });
const tree = git(['write-tree'], { env });
let parent = [];
try {
  git(['fetch', '-q', 'origin', `+refs/heads/${branch}:refs/remotes/origin/${branch}`], { stdio: 'pipe' });
  parent = ['-p', git(['rev-parse', `origin/${branch}`])];
} catch {} // first publish: no branch yet
const commit = git(['commit-tree', tree, ...parent, '-m', `Publish ${name}, built from ${source}`]);
git(['push', 'origin', `${commit}:refs/heads/${branch}`]);
console.log(`Published ${commit.slice(0, 7)} (built from ${source}) to the ${branch} branch`);
