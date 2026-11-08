// The Aegis Dynamics Worker (aegisdynamics.blind-ant.com). It serves the pages built by build.mjs, from out/site.json
// in its own Cloudflare static assets, uploaded by `npm run publish:aegis` with wrangler (wrangler.aegis.jsonc).
const HTML = { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, max-age=60', 'x-content-type-options': 'nosniff' };
const MD = { 'content-type': 'text/markdown; charset=utf-8', 'cache-control': 'public, max-age=60' };
const TEXT = { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'public, max-age=60' };
export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
    const url = new URL(request.url);
    const p = url.pathname;
    const r = await env.ASSETS.fetch(new Request(new URL('/site.json', request.url)));
    if (!r.ok) return new Response('Aegis Dynamics is temporarily unavailable.', { status: 503, headers: TEXT });
    const { pages, llms, md, llmsFull, robots } = await r.json();
    if (p === '/robots.txt') return new Response(robots, { headers: TEXT });
    if (p === '/llms.txt') return new Response(llms, { headers: TEXT });
    if (p === '/llms-full.txt') return new Response(llmsFull, { headers: TEXT });
    // Every page as Markdown, at its address plus index.md.
    if (p.endsWith('/index.md') && md[p.slice(0, -8)]) return new Response(md[p.slice(0, -8)], { headers: MD });
    if (!p.endsWith('/') && pages[p + '/']) return Response.redirect(url.origin + p + '/' + url.search, 301);
    if (pages[p]) return new Response(pages[p], { headers: HTML });
    return new Response(pages['/404/'], { status: 404, headers: HTML });
  },
};
