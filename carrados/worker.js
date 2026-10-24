// The Carrados Worker (carrados.com). It serves the built site from the `carrados-site` branch of the Charli.info repo,
// so publishing is a push to that branch (npm run publish:carrados). This file only changes if the serving rules do.
const SOURCE = 'https://raw.githubusercontent.com/CharliJoTyrer/Charli.info/carrados-site';
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', md: 'text/markdown; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml',
  jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', pdf: 'application/pdf',
};
const DESKS = ['lucy', 'madison', 'dice'];
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
    // Correspondents' desks: lucy.carrados.com opens /desks/lucy/. Pictures and styles are served as usual;
    // any other page link goes to the main site. On the main site, /desks/<name>/ moves to the desk's own address.
    const desk = DESKS.includes(url.hostname.split('.')[0]) ? url.hostname.split('.')[0] : null;
    if (desk) {
      if (path === '/' || path === '/index.md') path = `/desks/${desk}/` + (path === '/index.md' ? 'index.md' : '');
      else if (!/\.\w+$/.test(path)) return Response.redirect(`https://carrados.com${path}${url.search}`, 301);
    } else {
      const m = path.match(/^\/desks\/([\w-]+)\/?$/);
      if (m && DESKS.includes(m[1])) return Response.redirect(`https://${m[1]}.carrados.com/`, 301);
    }
    if (path.includes('..')) return new Response('Not found', { status: 404 });
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
