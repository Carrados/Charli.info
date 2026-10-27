# Blind Ant and Aegis Dynamics snapshot

Imported from the laptop repository at local main `471f5cf`, without its Git history. Website content and studio files are a snapshot; the uncommitted media-range Worker change is excluded.

Run from the repository root:

- `npm ci`
- `npm run build:blind-ant`: pages and Markdown mirrors, search chunks, then all seven public media files from `blind-ant/site/media.json`, into `dist/blind-ant`.
- `npm run build:aegis`: the nine-page site bundle into `dist/aegis/site.json`.

Root configurations are `wrangler.blind-ant.jsonc` and `wrangler.aegis.jsonc`. Only their Worker entry and asset paths differ from the laptop configurations. Worker names, account, compatibility date and bindings are preserved.

The nested package files preserve the original snapshot. Use the root build commands above. The historical nested publishing scripts are not adapted for this combined repository; do not use them.

Studio files are source and working material, not automatically published website assets. Only the seven files explicitly listed in the media manifest are copied to the Blind Ant build. Generated Aegis `out/site.json` was retained as part of the source-folder snapshot, but the root build writes a fresh bundle to `dist/aegis`.

Excluded: `.git`, dependencies, dist directories, environment files, credentials, and filenames containing token, secret or key. No source Git history was imported.
