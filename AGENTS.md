# For Codex and other agents working here

Read `CLAUDE.md` first. Its house rules apply to every agent, not only Claude: identities and pronouns, CharliPedia's rules, the ZIC page rules, and what never gets published.

## How work arrives

GitHub is the source of truth: the repository is `Carrados/Charli.info`, on the account Carrados only. Never use or mention CharliJoTyrer, CharliVerse or Blind-Ant GitHub accounts.

- Work on a branch named `codex/<topic>`, commit there, push the branch and open a pull request to `main`. Never push to `main`, never merge, and never publish or deploy: `main` is built and deployed by Cloudflare Workers Builds when Claude merges.
- In the pull request, list which files changed and why, which source each page came from, anything you left out on purpose, and anything only Charli-Jo can decide. Claude reviews it against `CLAUDE.md`.
- Run the relevant build before opening the pull request (`npm ci`, then `npm run build:charli`, `build:carrados`, `build:zic`, `build:blind-ant` or `build:aegis`). It works on Windows. If it fails, say so rather than changing the build to make it pass.
- Content changes only, unless asked. If the build, a Worker or a `wrangler.*.jsonc` needs changing, describe it instead.
- Never commit private documents, tokens, `.env` files or anything not meant for publication. Never run `npm run publish:*` or `deploy:*`.
- The laptop copy is a backup. If it differs from GitHub, say so before changing anything.

## Lessons from the first batches

- Pictures: save portraits as JPEG, about 800 pixels wide, beside the entry. If a picture is generated (all current CharliPedia portraits are), Behind the scenes says "Her portrait is a generated image, to be replaced by a render of her 3D model when it is made", and the file is added to the list in `charli/parked/README.md`.
- Leave out anything that reads as Charli-Jo's own life rather than the character's: widowhood, cats, walking groups, real routines, real places they live. When in doubt, leave it out and list it in the pull request.
- Don't put "Birkenhead" in source lines; the specification series is just "2026".
- Proper names keep their capitals (Neon Hysterically Blind); sentence case is for headings that would otherwise be in capitals.
- Several pull requests touching the same list are fine; Claude merges them together.
