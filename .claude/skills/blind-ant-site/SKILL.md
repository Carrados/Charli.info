---
name: blind-ant-site
description: Work on blind-ant.com or Aegis Dynamics inside Carrados/Charli.info - add a Piece or Object, change the site, or add a blind-ant.com subdomain. Replaces the older Blind-Ant-repo instructions. Use when Charli-Jo or Charlotte Joanne's Blind Ant work is mentioned.
---

# Blind Ant in this repo

Blind Ant is design fiction authored and operated by Charlotte Joanne (she/her), a pseudonym with her own voice. Present her as the author and operator, not as a character or an assistant, and keep her distinct from Charli-Jo (they/them). Pieces needn't explain the link. Read `CLAUDE.md` and `blind-ant/IMPORT.md` first.

## Where things are
- Site source: `blind-ant/site/` (`content/` for pages, `build.mjs`, `chunks.mjs`, `worker.js`, `media.json`).
- Aegis Dynamics: `blind-ant/subdomains/aegisdynamics/`.
- `blind-ant/studio/`: source and working material. It is not published. Only the seven files in `blind-ant/site/media.json` are copied into the site, by `engine/copy-blind-ant-media.mjs`.
- Workers: `blind-ant` (blind-ant.com, www, dev) and `aegis-dynamics` (aegisdynamics.blind-ant.com), configured in `wrangler.blind-ant.jsonc` and `wrangler.aegis.jsonc` at the repo root.
- Do not use the historical nested publish scripts or the nested `package.json` publish commands.

## Adding a Piece or Object
1. Add the Markdown under `blind-ant/site/content/pieces/<slug>/` (follow a neighbouring piece for frontmatter and structure). Pictures and documents sit beside the page.
2. If the Piece needs public media, add it to `blind-ant/site/media.json` and the file under `blind-ant/studio/`. Only listed files are published.
3. Every page: one H1, alt text, links per `CLAUDE.md`. A "Behind the thread" or "Behind the fiction" note says what is real and what is invented. Real evidence, fictional people, plausible consequences.
4. `npm ci && npm run build:blind-ant`, and `npm run build:aegis` for Aegis. Open a PR; Workers Builds deploys on merge (the `blind-ant` trigger watches `blind-ant/site/**`, `blind-ant/studio/**`, `engine/copy-blind-ant-media.mjs`, `wrangler.blind-ant.jsonc` and the package files).

## A new blind-ant.com subdomain
Blind Ant's own companies and characters get blind-ant.com subdomains. Follow the `add-site-to-builds` skill for the Worker, wrangler file and trigger (use `blind-ant/subdomains/<name>/` as its folder), and attach the subdomain in Cloudflare.

## Known open item
An uncommitted change to `site/worker.js` on Charli-Jo's laptop adds byte-range responses for media seeking. It was kept out of the import on purpose. Do not recreate it; it needs Charli-Jo's review as its own pull request.
