// The Carrados Worker (carrados.com and the correspondents' desks). It serves the built site (dist/carrados) from
// its own Cloudflare static assets, uploaded by `npm run publish:carrados` with wrangler (wrangler.carrados.jsonc).
// Nothing is read from GitHub.
const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', md: 'text/markdown; charset=utf-8',
  txt: 'text/plain; charset=utf-8', xml: 'application/xml; charset=utf-8', svg: 'image/svg+xml',
  jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', pdf: 'application/pdf',
  json: 'application/json; charset=utf-8', js: 'text/javascript; charset=utf-8', vtt: 'text/vtt; charset=utf-8',
};
const DESKS = ['lucy', 'madison', 'dice', 'charli'];
// Pieces that moved from Reports to The Blind AI on 29 October 2026. Their old addresses forward.
const MOVED_TO_BLOG = ['please-state-the-nature-of-the-accessibility-emergency', 'already-in-the-game', 'playing-the-game',
  'a-tale-of-two-emails', 'agents-provocateurs', 'flip-the-ai-toggle-and-feel-righteous', 'except-why-id-want-one',
  'human-in-the-loop-human-at-the-laptop', 'human-in-the-loop-human-in-bed', 'human-in-the-loop-human-with-the-final-word',
  'give-it-a-tuesday', 'price-both-columns-peak-cluster', 'the-day-the-earth-fell-silent', 'apparently-were-doing-this-now',
  'sloppy-thinking', 'the-persistence-of-vision'];
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
    // ZIC now has its own canonical home. Preserve old HTML, Markdown and download links.
    const zicPage = path.match(/^\/papers\/zic-design-standard(?:\/(index\.(?:html|md))?)?$/);
    if (zicPage) {
      const markdown = zicPage[1] === 'index.md' || (!zicPage[1] && (request.headers.get('accept') || '').includes('text/markdown'));
      return Response.redirect('https://zeroinformationcasualty.org/' + (markdown ? 'index.md' : '') + url.search, 301);
    }
    if (/^\/documents\/Zero_Information_Casualty_v1_[57]\.docx$/.test(path))
      return Response.redirect('https://zeroinformationcasualty.org' + path + url.search, 301);
    if (path === '/images/zic-v1-5-cover.jpg')
      return Response.redirect('https://zeroinformationcasualty.org/documents/zic-v1-5-cover.jpg' + url.search, 301);
    const moved = path.match(/^\/reports\/([\w-]+)(\/(?:index\.(?:html|md))?)?$/);
    if (moved && MOVED_TO_BLOG.includes(moved[1]))
      return Response.redirect(`https://carrados.com/blind-ai/${moved[1]}${moved[2] || '/'}${url.search}`, 301);
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
