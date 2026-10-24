// The charli.info Worker (the CharliVerse). It serves the built site from the `charli-site` branch of the Charli.info repo,
// so publishing is a push to that branch (npm run publish:charli). It also forwards the old site's addresses to where
// that work lives now. This file only changes if the serving rules do.
const SOURCE = 'https://raw.githubusercontent.com/CharliJoTyrer/Charli.info/charli-site';
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', md: 'text/markdown; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml',
  jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', pdf: 'application/pdf',
};
// The old charli.info, mapped to where things live now. First match wins.
function moved(path) {
  let m;
  if ((m = path.match(/^\/carrados\/([\w-]+)\/?$/))) return `https://carrados.com/papers/${m[1]}/`;
  if (/^\/carrados\/?$/.test(path)) return 'https://carrados.com/';
  if ((m = path.match(/^\/perspectives(\/[\w-]+)?\/?$/))) return `https://carrados.com/perspectives${m[1] ? m[1] + '/' : '/'}`;
  if ((m = path.match(/^\/documents\/((?:The_Tyrer_Framework|Zero_Information_Casualty_v1_5)\.docx)$/))) return `https://carrados.com/documents/${m[1]}`;
  // Pieces already rehung at Blind Ant go straight to them; everything else waits on Blind Ant's front page.
  if (/^\/pieces\/deathbot-2000(\/|$)/.test(path)) return 'https://blind-ant.com/pieces/deathbot-2000/';
  if (/^\/pieces\/do-androids-dream-of-electric-ants(\/|$)/.test(path)) return 'https://blind-ant.com/pieces/do-androids-dream/';
  if (/^\/(blind-ant|pieces|collections|people)(\/|$)/.test(path)) return 'https://blind-ant.com/';
  if (/^\/charliverse\/?$/.test(path)) return '/';
  if (/^\/accessibility-statement\/?$/.test(path)) return '/accessibility/';
  if (path === '/rss.xml') return '/';
  return null;
}
const pull = (path) => fetch(SOURCE + path, { cf: { cacheEverything: true, cacheTtl: 60 } });
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
  async fetch(request) {
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
    const url = new URL(request.url);
    if (url.hostname.startsWith('www.')) return Response.redirect(`https://${url.hostname.slice(4)}${url.pathname}${url.search}`, 301);
    let path = decodeURIComponent(url.pathname);
    if (path.includes('..')) return new Response('Not found', { status: 404 });
    const to = moved(path);
    if (to) return Response.redirect(to.startsWith('/') ? url.origin + to : to, 301);
    if (!/\.\w+$/.test(path)) {
      if (!path.endsWith('/')) {
        const probe = await pull(path + '/index.html');
        if (probe.ok) return Response.redirect(url.origin + path + '/' + url.search, 301);
      } else {
        path += (request.headers.get('accept') || '').includes('text/markdown') ? 'index.md' : 'index.html';
      }
    }
    const r = await pull(path);
    if (r.ok) return respond(r, path);
    const nf = await pull('/404.html');
    return nf.ok ? respond(nf, '/404.html', 404) : new Response('Not found', { status: 404 });
  },
};
