---
name: cloudflare-builds-check
description: Check Cloudflare Workers Builds for the five sites after a merge or when a site looks wrong - latest build per Worker, outcome, commit, logs on failure, the serving version, bindings and domains. Read-only. Use after merging to main, when asked "did it deploy", or to investigate Workers errors.
---

# Check Workers Builds

Uses the Cloudflare API tools (`search`, `execute`) with the account `25fb70ed788c5f04f8bfba0688a3e24a`. This skill is read-only: GET requests only. Do not start, cancel or change builds, and do not run `npm run publish:*` or `deploy:*`, unless Charli-Jo asks.

Workers: `charli`, `carrados`, `zic`, `blind-ant`, `aegis-dynamics`. Also `charlipedia-mcp` and `charliverse-indexer`, which are deployed by hand, not by builds.

1. Get each Worker's tag: `GET /accounts/{id}/workers/scripts` (the `tag` field).
2. Latest builds: `GET /accounts/{id}/builds/workers/{tag}/builds`. Report `status`, `build_outcome` and the commit (`build_trigger_metadata.commit_hash`). `queued` and `initializing` can take a few minutes; wait and check again rather than guessing.
3. A failure: read `GET /accounts/{id}/builds/builds/{build_uuid}/logs` and quote the last lines. Typical causes: a failing `npm ci`, a build script error, or a wrong `-c wrangler.<site>.jsonc`.
4. The serving version: `GET .../workers/scripts/{name}/deployments` (should be one version at 100%) and `.../settings` (bindings: `ASSETS` for the sites; `AI`, `VEC` and the four or five service bindings for the MCP and indexer).
5. Domains: `GET /accounts/{id}/workers/domains` should still map each hostname to the right Worker.
6. A site that did not build after a merge is usually expected: each trigger only watches its own folder plus `engine/`, its wrangler file, `package.json` and `package-lock.json`.

Live-site checks from this environment may be blocked. Say so and ask Charli-Jo to look rather than claiming the page is fine.

For "Workers errors": check the trigger of the problem (a 404 on a missing path is normal; a spike after a deploy is not) before drawing a conclusion.
