# For Codex and other agents working here

Read `CLAUDE.md` first. Its house rules apply to every agent, not only Claude: identities and pronouns, CharliPedia's rules, the ZIC page rules, and what never gets published.

## How work arrives

There is no GitHub any more (the account was suspended on 26 October 2026). This folder on Charli-Jo's laptop is the source of truth. So:

- Work on a local branch named `codex/<topic>` and commit there. Never `git push`, and never add a remote.
- When a batch is ready, tell Charli-Jo which files changed and why. Claude reviews them here against `CLAUDE.md`.
- Once Charli-Jo approves, merge into `main` locally, build, check, and publish with `npm run publish:charli` or `npm run publish:carrados`. Publishing uses wrangler's Cloudflare login on the laptop (`npx wrangler login`, once); if a token file `.cloudflare-token` is ever used instead, never commit, print or paste it.
- Run the build before saying a batch is ready. It works on Windows. If it fails, say so rather than changing the build to make it pass.
- Content changes only, unless asked. If the build, a Worker or a `wrangler.*.jsonc` needs changing, describe it instead.
- Never commit private documents or anything not meant for publication. Say which source each page came from.
- List anything you left out on purpose and anything only Charli-Jo can decide.

## Lessons from the first batches

- Pictures: save portraits as JPEG, about 800 pixels wide, beside the entry. If a picture is generated (all current CharliPedia portraits are), Behind the scenes says "Her portrait is a generated image, to be replaced by a render of her 3D model when it is made", and the file is added to the list in `charli/parked/README.md`.
- Leave out anything that reads as Charli-Jo's own life rather than the character's: widowhood, cats, walking groups, real routines, real places they live. When in doubt, leave it out and list it in the pull request.
- Don't put "Birkenhead" in source lines; the specification series is just "2026".
- Proper names keep their capitals (Neon Hysterically Blind); sentence case is for headings that would otherwise be in capitals.
- Several pull requests touching the same list are fine; Claude merges them together.
