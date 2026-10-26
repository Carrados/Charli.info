// The CharliVerse indexer (Worker `charliverse-indexer`). Every 15 minutes it reads the passages each site's
// build publishes (chunks.json), embeds any that are new or changed with Workers AI, and keeps the Vectorize
// index `charliverse` in step: upserting changed passages and deleting ones that have gone.
// It has no web address of its own that changes anything: it runs only on its schedule.
// If any source can't be read, it stops without deleting anything. Deploy with `npm run deploy:indexer` (wrangler.indexer.jsonc).
// It reads each site's published chunks.json straight from the site Workers through service bindings, never from GitHub.
const SOURCES = [['CHARLI', 'https://charli.info/chunks.json'], ['CARRADOS', 'https://carrados.com/chunks.json'], ['BLINDANT', 'https://blind-ant.com/chunks.json']];
const MODEL = '@cf/baai/bge-base-en-v1.5';
export const embedText = (c) => `${c.title}${c.heading ? '. ' + c.heading : ''}. ${c.text}`;

export async function run(env) {
  const all = [];
  for (const [binding, src] of SOURCES) {
    const r = await env[binding].fetch(new Request(src));
    if (!r.ok) return `stopped: ${src} answered ${r.status}`;
    all.push(...(await r.json()).chunks);
  }
  const manifest = JSON.parse((await env.STATE.get('manifest')) || '{}');
  const changed = all.filter((c) => manifest[c.id] !== c.hash);
  const live = new Set(all.map((c) => c.id));
  const gone = Object.keys(manifest).filter((id) => !live.has(id));
  if (!changed.length && !gone.length) return `unchanged: ${all.length} passages`;
  let done = 0, saved = Date.now();
  for (let i = 0; i < changed.length; i += 50) {
    const batch = changed.slice(i, i + 50);
    const emb = await env.AI.run(MODEL, { text: batch.map(embedText) });
    await env.VEC.upsert(batch.map((c, j) => ({
      id: c.id, values: emb.data[j],
      metadata: { site: c.site, title: c.title, url: c.url, heading: c.heading || '', text: c.text },
    })));
    for (const c of batch) manifest[c.id] = c.hash;
    done += batch.length;
    // Save progress now and then (the key store refuses more than one write a second to the same key).
    if (Date.now() - saved > 5000) { try { await env.STATE.put('manifest', JSON.stringify(manifest)); saved = Date.now(); } catch {} }
  }
  for (let i = 0; i < gone.length; i += 100) {
    const ids = gone.slice(i, i + 100);
    await env.VEC.deleteByIds(ids);
    for (const id of ids) delete manifest[id];
  }
  await new Promise((r) => setTimeout(r, 1100));
  await env.STATE.put('manifest', JSON.stringify(manifest));
  await env.STATE.put('last', JSON.stringify({ at: new Date().toISOString(), passages: all.length, embedded: done, deleted: gone.length }));
  return `indexed ${done}, deleted ${gone.length}, of ${all.length} passages`;
}

export default {
  async scheduled(event, env, ctx) { ctx.waitUntil(run(env).then((m) => console.log(m))); },
  async fetch(request, env) {
    // Read-only status, nothing else.
    return new Response((await env.STATE.get('last')) || 'not yet run', { headers: { 'content-type': 'application/json' } });
  },
};
