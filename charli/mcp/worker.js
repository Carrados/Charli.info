// The CharliPedia MCP server, at https://mcp.charli.info/ (and /mcp).
// A read-only Model Context Protocol server (Streamable HTTP, stateless JSON-RPC) that lets any agent look things up
// in CharliPedia. It can only read: it fetches the published entries (charlipedia/entries.json, written by the
// charli.info build) and has no tool that writes, edits or deletes anything. CharliPedia changes only when
// Charli-Jo publishes. semantic_search queries the Vectorize index `charliverse`, which charli/mcp/indexer.js keeps;
// this Worker only ever queries it. Redeploy this Worker to Cloudflare only if this file changes.
const DATA = 'https://raw.githubusercontent.com/CharliJoTyrer/Charli.info/charli-site/charlipedia/entries.json';
const PROTOCOLS = ['2025-06-18', '2025-03-26', '2024-11-05'];
const COURT = ['charlotte-joanne', 'alex', 'char', 'big-charli', 'cass-flux', 'cathryn-bigelow-vision', 'lottie', 'lily', 'jo'];

const INSTRUCTIONS = `CharliPedia is the memory of the CharliVerse, Charli-Jo Tyrer's world of fictional people, companies, places and ideas, at https://charli.info/charlipedia/.
Entries are written from inside the world; each ends with "Behind the scenes", written from outside, which says what is real.
Each entry has a status: canon (how things are), idea (not yet canon), stub (true but short), author (a real author described from outside) or real (something real).
This server is read-only. It is a source of continuity, not an authority: anything you invent is an idea, not canon, until Charli-Jo publishes it.
Respect the boundaries the entries record: for example, Big Charli is she/her; the Museum Court's private lives are never written; Charli-Jo Tyrer (they/them) and Charlotte Joanne (she/her) are distinct identities.
semantic_search also reaches Blind Ant (design fiction), Carrados (real-world research), ZIC (the web design standard) and charli.info, and every passage says which site it comes from: keep fiction and fact apart.\nSearch results are a sample, not the whole record: before saying something is not recorded, try other phrasings, search for the people involved and read their full entries. Many connections in the CharliVerse are implied across stories rather than stated; when you join them, say that you are inferring.\nCite entries by their URL. Everything is CC BY-SA 4.0.`;

const RO = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const TOOLS = [
  { name: 'search', title: 'Search CharliPedia', description: 'Search CharliPedia entries by words in their title, description or text. Returns the best matches with a short snippet and URL.', inputSchema: { type: 'object', properties: { query: { type: 'string', description: 'Words to search for' }, limit: { type: 'integer', minimum: 1, maximum: 25, description: 'Most results to return (default 8)' } }, required: ['query'] }, annotations: RO },
  { name: 'get_entry', title: 'Get a CharliPedia entry', description: 'Get one CharliPedia entry in full, as Markdown, by its slug (for example "big-charli") or its exact title.', inputSchema: { type: 'object', properties: { entry: { type: 'string', description: 'Slug or title of the entry' } }, required: ['entry'] }, annotations: RO },
  { name: 'list_entries', title: 'List CharliPedia entries', description: 'List CharliPedia entries with their one-sentence descriptions, optionally only those starting with a letter or with a given status.', inputSchema: { type: 'object', properties: { letter: { type: 'string', description: 'First letter of the title, ignoring a leading "The"' }, status: { type: 'string', enum: ['canon', 'idea', 'stub', 'author', 'real'] } } }, annotations: RO },
  { name: 'semantic_search', title: 'Search the CharliVerse by meaning', description: 'Search by meaning and by words together, across CharliPedia, Blind Ant, Carrados, ZIC, charli.info and Charli-Jo\'s Training courses. Each result says which site it comes from and what kind of writing that is. Use this for themes, ideas and questions ("who has been let down by a beautiful interface?"); use search for names. Set site to training for practical how-to questions, or to one site to keep to it.', inputSchema: { type: 'object', properties: { query: { type: 'string', description: 'A question, theme or idea, in plain words' }, site: { type: 'string', enum: ['charlipedia', 'blind-ant', 'carrados', 'charli.info', 'training', 'zic'], description: 'Search only one site (optional)' }, limit: { type: 'integer', minimum: 1, maximum: 15, description: 'Most passages to return (default 6)' } }, required: ['query'] }, annotations: RO },
  { name: 'get_court', title: 'Get the CharliVerse Court', description: 'Get the CharliVerse Court entry and the full entries of its nine members, for a deliberation or a crossover.', inputSchema: { type: 'object', properties: {} }, annotations: RO },
];

const SITES = {
  charlipedia: 'CharliPedia, the memory of the CharliVerse: written from inside the world; its people and companies are fictional, and each entry\'s Behind the scenes says what is real',
  'blind-ant': 'Blind Ant, design fiction by Charlotte Joanne: speculative works and how they were made',
  zic: 'Zero Information Casualty: the real-world web design standard by C J Tyrer and Claude (Anthropic)',
  carrados: 'Carrados, design non-fiction: real-world research and reports that make sourced claims about reality (its correspondents are characters)',
  'charli.info': 'charli.info, the front door of the CharliVerse and Charli-Jo Tyrer\'s real-world work, always labelled as real',
  training: 'Training, Charli-Jo Tyrer\'s real-world courses on AI for blind and partially sighted people, including Confident with AI with TAVIP: practical how-to material',
};
// Hybrid search: meaning (Vectorize) blended with words (BM25 over the same passages and lines), by reciprocal
// rank fusion. The passages and lines come from each site's published chunks.json, cached for five minutes.
const CHUNKS = [
  'https://raw.githubusercontent.com/CharliJoTyrer/Charli.info/charli-site/chunks.json',
  'https://raw.githubusercontent.com/CharliJoTyrer/Charli.info/carrados-site/chunks.json',
  'https://raw.githubusercontent.com/CharliJoTyrer/Charli.info/zic-site/chunks.json',
  'https://raw.githubusercontent.com/CharliJoTyrer/Blind-Ant/site/chunks.json',
];
const STOP = new Set('a an and are as at be been being but by can could did do does doing for from had has have he her hers him his how i if in into is it its me my no not of on or our she so some someone anyone than that the their them then there these they this those to was we were what when where which who whom whose why will with would you your say says said tell told about any'.split(' '));
const stem = (w) => {
  if (w.length > 5 && w.endsWith('ing')) w = w.slice(0, -3);
  else if (w.length > 4 && w.endsWith('ed')) w = w.slice(0, -2);
  if (w.length > 3 && w.endsWith('s') && !w.endsWith('ss')) w = w.slice(0, -1);
  return w;
};
const tokens = (t) => (String(t).toLowerCase().replace(/[\u2019']/g, "'").replace(/'s\b/g, '').match(/[a-z0-9]+/g) || []).filter((w) => !STOP.has(w)).map(stem);
let units = { at: 0, data: null };
async function loadUnits() {
  if (units.data && Date.now() - units.at < 300000) return units.data;
  const all = [];
  for (const u of CHUNKS) {
    const r = await fetch(u, { cf: { cacheEverything: true, cacheTtl: 300 } });
    if (r.ok) all.push(...(await r.json()).chunks);
  }
  const byId = new Map(all.map((c) => [c.id, c]));
  const df = new Map(); let total = 0;
  const tf = all.map((c) => {
    const m = new Map();
    for (const w of tokens(`${c.title} ${c.heading || ''} ${c.text}`)) { m.set(w, (m.get(w) || 0) + 1); total++; }
    for (const w of m.keys()) df.set(w, (df.get(w) || 0) + 1);
    let len = 0; for (const v of m.values()) len += v;
    return { m, len };
  });
  units = { at: Date.now(), data: { all, byId, df, tf, avg: total / Math.max(all.length, 1) } };
  return units.data;
}
function keyword(u, q, site, k) {
  const terms = [...new Set(tokens(q))].filter((w) => u.df.has(w));
  if (!terms.length) return [];
  const N = u.all.length, out = [];
  u.all.forEach((c, i) => {
    if (site && c.site !== site) return;
    const { m, len } = u.tf[i];
    let s = 0;
    for (const w of terms) {
      const f = m.get(w); if (!f) continue;
      const idf = Math.log(1 + (N - u.df.get(w) + 0.5) / (u.df.get(w) + 0.5));
      s += idf * (f * 2.2) / (f + 1.2 * (0.25 + 0.75 * len / u.avg));
    }
    if (s > 0) out.push([c.id, s]);
  });
  return out.sort((a, b) => b[1] - a[1]).slice(0, k).map((x) => x[0]);
}
async function meaning(env, args) {
  if (!env || !env.AI || !env.VEC) throw new Error('Search by meaning is not available right now; use search instead.');
  const q = String(args.query || '').trim();
  if (!q) throw new Error('Give a question or theme to search for.');
  const limit = Math.min(Number(args.limit) || 6, 15);
  const site = args.site && SITES[args.site] ? args.site : null;
  const [emb, u] = await Promise.all([env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [q] }), loadUnits()]);
  const opts = { topK: 50, returnMetadata: 'none' };
  if (site) opts.filter = { site };
  const vec = ((await env.VEC.query(emb.data[0], opts)).matches || []).map((m) => m.id);
  const words = keyword(u, q, site, 50);
  const score = new Map();
  vec.forEach((id, r) => score.set(id, (score.get(id) || 0) + 1 / (60 + r)));
  words.forEach((id, r) => score.set(id, (score.get(id) || 0) + 1 / (60 + r)));
  const seen = new Set(), hits = [];
  for (const [id] of [...score].sort((a, b) => b[1] - a[1])) {
    const c = u.byId.get(id);
    if (!c || seen.has(c.url)) continue; // the best match from each page
    seen.add(c.url); hits.push(c);
    if (hits.length >= limit) break;
  }
  if (!hits.length) return `Nothing found for "${q}". Try other words, or the names of people or places involved.`;
  const used = [...new Set(hits.map((c) => c.site))];
  const show = (c) => {
    const head = `- ${c.title}${c.heading ? ' (' + c.heading + ')' : ''}, from ${c.site}: ${c.url}`;
    if (c.kind === 'line') {
      const p = u.byId.get(c.passage);
      return `${head}\n  Matched: "${c.text}"${p ? `\n  In context: ${p.text}` : ''}`;
    }
    return `${head}\n  ${c.text}`;
  };
  return `${hits.length} result(s) for "${q}", best first, one per page.\n\nThese are the closest matches, not everything. If something seems missing, search again in other words or by the names involved, and read whole entries with get_entry, before concluding it is not recorded.\n\nWhere they come from:\n${used.map((x) => '- ' + x + ': ' + SITES[x]).join('\n')}\n\n${hits.map(show).join('\n\n')}`;
}

let cache = { at: 0, data: null };
async function load() {
  if (cache.data && Date.now() - cache.at < 300000) return cache.data;
  const r = await fetch(DATA, { cf: { cacheEverything: true, cacheTtl: 300 } });
  if (!r.ok) throw new Error(`CharliPedia could not be loaded (${r.status})`);
  cache = { at: Date.now(), data: await r.json() };
  return cache.data;
}
const key = (t) => t.replace(/^the\s+/i, '').toLowerCase();
const line = (e) => `- ${e.title} (${e.slug}, ${e.status || 'no status'}): ${e.description} ${e.url}`;
function find(entries, q) {
  const s = String(q || '').trim().toLowerCase();
  return entries.find((e) => e.slug === s || e.title.toLowerCase() === s || e.slug === s.replace(/\s+/g, '-'));
}
function search(entries, query, limit = 8) {
  const terms = String(query).toLowerCase().split(/\W+/).filter((t) => t.length > 1);
  if (!terms.length) return [];
  const scored = entries.map((e) => {
    const t = e.title.toLowerCase(), d = e.description.toLowerCase(), m = e.markdown.toLowerCase();
    let score = 0;
    for (const w of terms) score += (t.includes(w) ? 10 : 0) + (d.includes(w) ? 4 : 0) + Math.min((m.split(w).length - 1), 10);
    return { e, score };
  }).filter((x) => x.score > 0).sort((a, b) => b.score - a.score).slice(0, limit);
  return scored.map(({ e }) => {
    const body = e.markdown.replace(/\s+/g, ' ');
    const i = Math.max(0, body.toLowerCase().indexOf(terms[0]) - 80);
    return `${line(e)}\n  …${body.slice(i, i + 220).trim()}…`;
  });
}

async function callTool(name, args = {}, env) {
  if (name === 'semantic_search') return meaning(env, args);
  const { entries, updated } = await load();
  if (name === 'search') {
    const hits = search(entries, args.query, Math.min(Number(args.limit) || 8, 25));
    return hits.length ? `${hits.length} result(s) for "${args.query}":\n\n${hits.join('\n\n')}` : `Nothing in CharliPedia matches "${args.query}".`;
  }
  if (name === 'get_entry') {
    const e = find(entries, args.entry);
    if (!e) { const s = search(entries, args.entry, 5); throw new Error(`No entry called "${args.entry}".${s.length ? ' Closest:\n' + s.join('\n') : ''}`); }
    return `Source: ${e.url}\nStatus: ${e.status || 'none'}\n\n${e.markdown}`;
  }
  if (name === 'list_entries') {
    let list = entries;
    if (args.letter) list = list.filter((e) => key(e.title).startsWith(String(args.letter).toLowerCase()[0]));
    if (args.status) list = list.filter((e) => e.status === args.status);
    return `${list.length} of ${entries.length} entries (CharliPedia updated ${updated}):\n\n${list.map(line).join('\n')}`;
  }
  if (name === 'get_court') {
    const court = find(entries, 'the-charliverse-court');
    const members = COURT.map((s) => find(entries, s)).filter(Boolean);
    return [court, ...members].map((e) => `Source: ${e.url}\n\n${e.markdown}`).join('\n\n---\n\n');
  }
  throw new Error(`Unknown tool: ${name}`);
}

async function handle(msg, env) {
  const { id, method, params = {} } = msg;
  const ok = (result) => ({ jsonrpc: '2.0', id, result });
  const fail = (code, message) => ({ jsonrpc: '2.0', id, error: { code, message } });
  if (id === undefined || id === null) return null; // a notification: nothing to say back
  if (method === 'initialize') {
    const v = PROTOCOLS.includes(params.protocolVersion) ? params.protocolVersion : PROTOCOLS[0];
    return ok({ protocolVersion: v, capabilities: { tools: { listChanged: false } }, serverInfo: { name: 'charlipedia', title: 'CharliPedia', version: '1.3.0' }, instructions: INSTRUCTIONS });
  }
  if (method === 'ping') return ok({});
  if (method === 'tools/list') return ok({ tools: TOOLS });
  if (method === 'tools/call') {
    try { return ok({ content: [{ type: 'text', text: await callTool(params.name, params.arguments || {}, env) }], isError: false }); }
    catch (e) { return ok({ content: [{ type: 'text', text: String(e.message || e) }], isError: true }); }
  }
  if (method === 'resources/list') return ok({ resources: [] });
  if (method === 'prompts/list') return ok({ prompts: [] });
  return fail(-32601, `Method not found: ${method}`);
}

const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-methods': 'POST, GET, OPTIONS', 'access-control-allow-headers': 'content-type, accept, mcp-protocol-version, mcp-session-id', 'access-control-expose-headers': 'mcp-protocol-version' };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json', ...CORS } });

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    const url = new URL(request.url);
    // Clients such as ChatGPT look for sign-in details first. There is no sign-in: say so plainly with a 404.
    if (url.pathname.startsWith('/.well-known/')) return json({ error: 'not_found', message: 'No sign-in: this server is open and read-only.' }, 404);
    if (request.method === 'GET') {
      if (['/', '/mcp', '/mcp/'].includes(url.pathname) && !(request.headers.get('accept') || '').includes('text/event-stream')) {
        return new Response(`CharliPedia MCP server (read-only).\n\nAdd https://mcp.charli.info/mcp (or https://mcp.charli.info/) to your agent as a remote MCP server (Streamable HTTP, no sign-in).\nTools: search, semantic_search, get_entry, list_entries, get_court.\nCharliPedia itself: https://charli.info/charlipedia/\n`, { headers: { 'content-type': 'text/plain; charset=utf-8', ...CORS } });
      }
      return new Response('This server does not open event streams.', { status: 405, headers: { allow: 'POST, OPTIONS', ...CORS } });
    }
    if (request.method === 'DELETE') return new Response(null, { status: 405, headers: CORS });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: CORS });
    let body;
    try { body = await request.json(); } catch { return json({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } }, 400); }
    if (Array.isArray(body)) {
      const out = (await Promise.all(body.map((m) => handle(m, env)))).filter(Boolean);
      return out.length ? json(out) : new Response(null, { status: 202, headers: CORS });
    }
    const out = await handle(body, env);
    return out ? json(out) : new Response(null, { status: 202, headers: CORS });
  },
};
