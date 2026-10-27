// The Aegis Dynamics Worker (aegisdynamics.blind-ant.com). It serves the pages built by build.mjs, from out/site.json
// in its own Cloudflare static assets, uploaded by `npm run publish:aegis` with wrangler (wrangler.aegis.jsonc).
const HTML = { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, max-age=60', 'x-content-type-options': 'nosniff' };
const TEXT = { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'public, max-age=60' };
export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
    const url = new URL(request.url);
    const p = url.pathname;
    if (p === '/robots.txt') return new Response('# Aegis Dynamics is fictional: a company from DeathBot 2000, a Blind Ant piece. Sent agents: served. Search: permitted. Training: permitted.\nUser-agent: *\nAllow: /\nContent-Signal: search=yes, ai-input=yes, ai-train=yes\n', { headers: TEXT });
    const r = await env.ASSETS.fetch(new Request(new URL('/site.json', request.url)));
    if (!r.ok) return new Response('Aegis Dynamics is temporarily unavailable.', { status: 503, headers: TEXT });
    const { pages, llms } = await r.json();
    if (p === '/llms.txt') return new Response(llms, { headers: TEXT });
    if (!p.endsWith('/') && pages[p + '/']) return Response.redirect(url.origin + p + '/' + url.search, 301);
    if (pages[p]) return new Response(pages[p], { headers: HTML });
    return new Response(pages['/404/'], { status: 404, headers: HTML });
  },
};
