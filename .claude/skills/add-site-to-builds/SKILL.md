---
name: add-site-to-builds
description: Add a new site or Worker (for example Iceberg Hosiery, Seamiotics, LULU TOM, a new correspondent desk) to this repo and to Cloudflare Workers Builds, with build script, wrangler file, MCP and indexer bindings, search label and subdomain. Use when a new CharliVerse or Carrados site is wanted.
---

# Add a site

Read `CLAUDE.md` (Publishing, Domains, the architecture) first. Which site a thing belongs to is Charli-Jo's decision: fictional does not mean Blind Ant. CharliVerse entities get charli.info subdomains, Blind Ant's get blind-ant.com subdomains, correspondents get carrados.com subdomains.

Do this on a branch and open a pull request. Do not change Cloudflare until the PR is approved and merged, and say what you will change on Cloudflare before doing it.

## In the repo
1. Content in `<site>/content/`, settings in `<site>/site.config.mjs`, styles in `<site>/public/styles.css`, a Worker `<site>/worker.js` (copy `zic/worker.js` for a plain static site; it reads only `env.ASSETS`).
2. `package.json`: `"build:<site>": "node engine/build.mjs <site> && node engine/chunks.mjs dist/<site> https://<domain> <label>"`.
3. `wrangler.<site>.jsonc`: copy `wrangler.zic.jsonc`; change `name`, `main`, `assets.directory` (`dist/<site>`). Keep `account_id`, `compatibility_date`, `workers_dev: false`, `preview_urls: false`, `run_worker_first: true`, `html_handling` and `not_found_handling` as `"none"`.
4. Search: add a service binding for the Worker in `wrangler.mcp.jsonc` and `wrangler.indexer.jsonc`, the site label in `charli/mcp/worker.js` and `charli/mcp/indexer.js` (and the list in `CLAUDE.md`). The MCP and indexer are deployed by hand (`npm run deploy:mcp`, `deploy:indexer`) only after the site's Worker exists, and only with Charli-Jo's go-ahead. A binding to a Worker that does not exist makes that deploy fail.
5. Update the table in `CLAUDE.md` (Publishing) and the Domains section.
6. Run `npm ci`, `npm run build:<site>`, `node --test tests/zic-migration.test.mjs`.

## In Cloudflare (after merge, with approval)
1. The Worker must exist: deploying once with `wrangler deploy -c wrangler.<site>.jsonc` creates it. Attach the custom domain in the dashboard (Worker, Settings, Domains and Routes) and add the DNS if the zone needs it. Never touch MX, SPF, DKIM or DMARC records.
2. Create the build trigger: `POST /accounts/{id}/builds/triggers` with
   - `external_script_id`: the Worker's tag
   - `build_token_uuid`: `fc3837ba-31a6-4ec1-9b3f-929daa823a07` (the shared token; check with `GET /builds/tokens`)
   - `repo_connection_uuid`: `7a68ddaf-637a-4c0c-b0d7-8be11e433c2a` (`Carrados/Charli.info`)
   - `build_command`: `npm ci && npm run build:<site>`; `deploy_command`: `npx wrangler deploy -c wrangler.<site>.jsonc`
   - `root_directory`: `/`; `branch_includes`: `["main"]`; `branch_excludes`: `[]`
   - `path_includes`: `["<site>/**","engine/**","wrangler.<site>.jsonc","package.json","package-lock.json"]`; `path_excludes`: `[]`
   Then `PATCH /builds/workers/{tag}` with `{"previews_enabled": false}`. A manual first build is `POST /builds/triggers/{trigger_uuid}/builds` with `{"branch":"main"}`.
3. Check with the `cloudflare-builds-check` skill.
