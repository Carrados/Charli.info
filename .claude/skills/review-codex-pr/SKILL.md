---
name: review-codex-pr
description: Review a Codex pull request (branch codex/<topic>) on Carrados/Charli.info against CLAUDE.md, scan it for secrets, run the builds, and merge it once Charli-Jo approves. Use when Codex says a batch is ready, a PR is opened, or the user asks to review or merge a PR.
---

# Review a Codex pull request

Read `CLAUDE.md` and `AGENTS.md` first. Their rules are the checklist; do not rely on memory.

## 1. Look at what changed
- Fetch the branch locally (`git fetch origin <branch>`, `git diff --stat origin/main...origin/<branch>`) rather than reading the PR through the API: big PRs overflow the API output.
- Group the changed files by site (`charli/`, `carrados/`, `zic/`, `blind-ant/`) and say which Workers the merge will rebuild.

## 2. Check against the house rules
- Names (see "Names and pronouns" in CLAUDE.md): Charli-Jo is they/them; Charlotte Joanne is she/her, Charli-Jo's pen name, never a character or persona, and never swapped for Charli-Jo in a piece about her; personas write as themselves and are labelled as personas; characters only appear in stories; personas and characters never mention Charli-Jo, "Charli", the CharliVerse or CharliPedia in their own voice; Big Charli is she/her, never "it"; no CharliVerse Court; nobody real appears in a made-up scene.
- Front page: a substantial piece opens with where you are, what it is and who's speaking, and ends with More about this, More like this and About the author, without repeating the footer's author line. CharliPedia: `status:` frontmatter, an entry ends with `## Behind the scenes`, no entry for Charli, only approved canon, `status: author` for Charlotte Joanne (never the surname Tyrer).
- Pages: exactly one H1 (the title; text starts at `##`), real headings, alt text on every picture, first mention of a person/product/source linked with the name as link text, no "click here", no forced new tabs.
- Charli-Jo's words are unchanged except obvious typos, and the PR says which typos were fixed.
- Reports: `date` rule (file's saved date, or the sent date, and says so), `time:` if several the same day, `desk` and `byline` for characters.
- Pictures: generated portraits are JPEG about 800 px, noted in Behind the scenes and listed in `charli/parked/README.md`.
- Nothing from Charli-Jo's real life in a character (widowhood, cats, routines, real places), no "Birkenhead" in source lines.
- Licence: CC BY-SA 4.0 unless the page says `license:`.
- Out of scope: no changes to the build, a Worker or `wrangler.*.jsonc` unless asked. Anything in `parked/` is not built.

## 3. Scan for secrets and personal data
Search the added files for tokens and keys (`AKIA`, `-----BEGIN`, `ghp_`, `github_pat_`, `sk-`, `cfut_`, `Bearer `, `CLOUDFLARE_API_TOKEN=`), file names containing token, secret, key or `.env`, and email addresses (in-world addresses are fine, real private ones are not). Check no file is over 100 MB.

## 4. Build
`npm ci`, then the build for each site touched: `npm run build:charli`, `build:carrados`, `build:zic`, `build:blind-ant`, `build:aegis`. Run `node --test tests/zic-migration.test.mjs` (build zic and carrados first). If something fails, say so with the output and do not change the build to make it pass.

## 5. Report, then merge
Say what is fine, what must change, and what only Charli-Jo can decide. Merge only after Charli-Jo says so. A merge to `main` deploys live, so then run the `cloudflare-builds-check` skill.
