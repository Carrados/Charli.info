# Charli-Jo's sites: house rules

This repo holds the sites where Charli-Jo Tyrer writes as herself. Read this before changing anything.

## Which site is which

- **carrados.com** (`carrados/`): the work. Accessibility as information integrity (the Tyrer Framework, the ZIC standard, essays), Reports from the frontier of accessibility AI (the posts of The Blind AI), and Perspectives. Bylined Charli-Jo Tyrer.
- **charli.info** (`charli/`, not built yet): Charli-Jo in real life. Who she is, training, talks, consulting, contact, and the way to the other sites. Anything where she might have to be Charli-Jo in person belongs here.
- Design fiction is not here. It lives at **blind-ant.com** (repo CharliJoTyrer/Blind-Ant), in role, as Charlotte Joanne.
- The frame: Charli-Jo is an explorer, and Carrados and Blind Ant are two learned societies she reports back to. charli.info is her own house.
- CharliVerse personas who drop into work (for example Big Charli) get charli.info subdomains. Blind Ant's own characters and companies get blind-ant.com subdomains.

## How a site is built

- `engine/build.mjs <site>` builds `<site>/content` into `dist/<site>/`. Every Markdown file is a page plus a Markdown mirror, with llms.txt, robots.txt (every crawler welcome) and a sitemap.
- Frontmatter: `title`, `description` (one sentence), and optionally `date`, `order`, `byline`. `<!-- list -->` in a folder's index lists that folder's pages (by order, then newest first).
- Pictures and documents sit beside pages in `content/` and are published at the same path. Site settings (name, address, navigation, footer) are in `<site>/site.config.mjs`; styles in `<site>/public/styles.css`.
- To add a Report: a Markdown file in `carrados/content/reports/` with a `date`.

## Rules for every page

- Built to the Zero Information Casualty (ZIC) standard: exactly one H1 per page (from the title; page text starts at `##`; the build refuses a `#` heading outside code), real headings, AAA contrast for body text, alt text on every picture, no sideways scroll at phone width.
- Keep Charli-Jo's words as she wrote them. Fix obvious typos and say which ones you fixed.
- Everything is CC BY-SA 4.0.

## Publishing

- `npm install`, then `npm run publish:carrados` builds and pushes `dist/carrados/` to the `carrados-site` branch. The Cloudflare Worker `carrados` (`carrados/worker.js`) serves that branch. Commit the source to `main` too.
- The Worker reads the branch from raw.githubusercontent.com, which only works while this repo is public.
- `carrados/worker.js` only needs redeploying to Cloudflare if the serving rules change.
- Before publishing, check every page builds, has one H1, and has no sideways scroll at phone width.

## Domains

- carrados.com is a Cloudflare zone on Lottie's account (registered at IONOS). carrados.com and www.carrados.com are custom domains of the `carrados` Worker, which sends www to the plain address. Preview: carrados.charlijotyrer.workers.dev.
- Its email stays with IONOS: never touch the MX, SPF, DKIM, DMARC, autodiscover or domainconnect records.

## Where the old site came from

The pages were carried over from the old Astro site (GitHub org `charliverse`, repo `charli.info`, served by GitHub Pages at charli.info until the new charli.info replaces it). Paths changed: `charli.info/carrados/<paper>/` is now `carrados.com/papers/<paper>/`, and `charli.info/perspectives/<essay>/` is now `carrados.com/perspectives/<essay>/`.
