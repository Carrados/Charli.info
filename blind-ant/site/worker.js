// The Blind Ant Worker. It serves the built site (dist, with the media from site/media.json) from its own
// Cloudflare static assets, uploaded by `npm run publish` with wrangler (wrangler.jsonc). Nothing is read from GitHub.
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', md: 'text/markdown; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml',
  js: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8', vtt: 'text/vtt; charset=utf-8',
  mp4: 'video/mp4', jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp', woff2: 'font/woff2', pdf: 'application/pdf', mp3: 'audio/mpeg', m4a: 'audio/mp4',
};
// Files come from this Worker's own static assets. Range requests (for the films and the song) pass straight through.
const pull = (env, request, path) => env.ASSETS.fetch(new Request(new URL(path, request.url), { headers: request.headers }));
function respond(r, path, status) {
  const ext = path.split('.').pop();
  const h = new Headers();
  for (const k of ['content-length', 'content-range', 'etag']) if (r.headers.get(k)) h.set(k, r.headers.get(k));
  h.set('content-type', TYPES[ext] || 'application/octet-stream');
  h.set('accept-ranges', 'bytes');
  h.set('vary', 'accept');
  h.set('x-content-type-options', 'nosniff');
  h.set('cache-control', path.startsWith('/media/') ? 'public, max-age=86400' : 'public, max-age=60');
  return new Response(r.body, { status: status || r.status, headers: h });
}
export default {
  async fetch(request, env) {
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
    const url = new URL(request.url);
    let path = decodeURIComponent(url.pathname);
    if (path.includes('..')) return new Response('Not found', { status: 404 });
    if (!/\.\w+$/.test(path)) {
      if (!path.endsWith('/')) {
        const probe = await pull(env, request, path + '/index.html');
        if (probe.ok) return Response.redirect(url.origin + path + '/' + url.search, 301);
      } else {
        const wantsMd = (request.headers.get('accept') || '').includes('text/markdown');
        path += wantsMd ? 'index.md' : 'index.html';
      }
    }
    const r = await pull(env, request, path);
    if (r.ok || r.status === 206) return respond(r, path);
    const nf = await pull(env, request, '/404.html');
    return nf.ok ? respond(nf, '/404.html', 404) : new Response('Not found', { status: 404 });
  },
};
