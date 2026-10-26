// The ZIC Worker (zeroinformationcasualty.org). It serves the built site (dist/zic) from its own Cloudflare static
// assets, uploaded by `npm run publish:zic` with wrangler (wrangler.zic.jsonc). Nothing is read from GitHub.
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', md: 'text/markdown; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml',
  jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', pdf: 'application/pdf',
  json: 'application/json; charset=utf-8', js: 'text/javascript; charset=utf-8',
};
// Files come from this Worker's own static assets (uploaded with each publish), not from anywhere else.
const pull = (env, request, path) => env.ASSETS.fetch(new Request(new URL(path, request.url), { headers: request.headers }));
function respond(r, path, status) {
  const ext = path.split('.').pop();
  const h = new Headers();
  for (const k of ['content-length', 'etag']) if (r.headers.get(k)) h.set(k, r.headers.get(k));
  h.set('content-type', TYPES[ext] || 'application/octet-stream');
  h.set('vary', 'accept');
  h.set('x-content-type-options', 'nosniff');
  h.set('cache-control', 'public, max-age=60');
  return new Response(r.body, { status: status || r.status, headers: h });
}
export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
    const url = new URL(request.url);
    if (url.hostname.startsWith('www.')) return Response.redirect(`https://${url.hostname.slice(4)}${url.pathname}${url.search}`, 301);
    let path = decodeURIComponent(url.pathname);
    if (path.includes('..')) return new Response('Not found', { status: 404 });
    if (!/\.\w+$/.test(path)) {
      if (!path.endsWith('/')) {
        const probe = await pull(env, request, path + '/index.html');
        if (probe.ok) return Response.redirect(url.origin + path + '/' + url.search, 301);
      } else {
        path += (request.headers.get('accept') || '').includes('text/markdown') ? 'index.md' : 'index.html';
      }
    }
    const r = await pull(env, request, path);
    if (r.ok) return respond(r, path);
    const nf = await pull(env, request, '/404.html');
    return nf.ok ? respond(nf, '/404.html', 404) : new Response('Not found', { status: 404 });
  },
};
