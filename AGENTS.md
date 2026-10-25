# For Codex and other agents working here

Read `CLAUDE.md` first. Its house rules apply to every agent, not only Claude: identities and pronouns, CharliPedia's rules, the ZIC page rules, and what never gets published.

## How work arrives

Charli-Jo uses two agents. Codex prepares batches; Claude checks, builds and publishes them. So:

- Work on a branch named `codex/<topic>`, and open a pull request into `main`. One pull request per batch is fine.
- Never push to `main`, `charli-site` or `carrados-site`, and never run `npm run publish:*`. Claude merges and publishes after review.
- Run `npm run build:charli` (or `build:carrados`) before opening the pull request. It works on Windows. If it fails, say so in the pull request rather than changing the build to make it pass.
- Content changes only, unless asked. If something in `engine/` or a site config needs changing, describe it in the pull request instead.
- Never commit Charli-Jo's private canon documents, Word originals or handoff notes. Summarise into Markdown, and say in the pull request which source each page came from, its version and its date.
- Every CharliPedia entry ends with `## Behind the scenes`, and has `status:` in its frontmatter.
- In the pull request, list anything you left out on purpose and anything only Charli-Jo can decide.

## Lessons from the first batches

- Pictures: save portraits as JPEG, about 800 pixels wide, beside the entry. If a picture is generated (all current CharliPedia portraits are), Behind the scenes says "Her portrait is a generated image, to be replaced by a render of her 3D model when it is made", and the file is added to the list in `charli/parked/README.md`.
- Leave out anything that reads as Charli-Jo's own life rather than the character's: widowhood, cats, walking groups, real routines, real places they live. When in doubt, leave it out and list it in the pull request.
- Don't put "Birkenhead" in source lines; the specification series is just "2026".
- Proper names keep their capitals (Neon Hysterically Blind); sentence case is for headings that would otherwise be in capitals.
- Several pull requests touching the same list are fine; Claude merges them together.
