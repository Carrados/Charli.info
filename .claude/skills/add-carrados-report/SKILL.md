---
name: add-carrados-report
description: Turn pasted text or a Word file into a Carrados Report, or a Blind AI post (Charli-Jo's own desk, or dice, Lucy Love-Child or Madison McDonnell) following the house rules. Use when Charli-Jo gives text or a file to publish as a Report on carrados.com.
---

# Add a Carrados Report

Read `CLAUDE.md` (Identities and pronouns, Rules for every page) first.

1. Decide the register first. A professional account in Charli-Jo's own name (the work, methods, findings, limits) is a Report: `carrados/content/reports/<slug>.md`. An informal same-day dispatch, a humorous or experimental piece, or anything a character files is a Blind AI post: `carrados/content/blind-ai/<slug>.md`. If unsure, ask Charli-Jo which it is.
2. Frontmatter: `title`, `description` (one sentence), `date`, and `time: "HH:MM"` if several are filed the same day (newest first). If a character filed it: `desk: <dice|lucy|madison>` and `byline`. Charli-Jo's own Blind AI dispatches: `desk: charli` and `byline: Charli-Jo Tyrer` (no character line is added). The closing line saying the writer is a character is added automatically.
3. The `date` is the date the file was last saved (a Word document's modified date, or the file's date on their computer). With pasted text and no file, use the date it is sent, and say so.
4. Body starts at `##` (the title is the only H1). Keep Charli-Jo's words as written; fix only obvious typos and tell Charli-Jo which ones.
5. Links: link the first mention of a person, product or source with the name as link text; link what a piece quotes or summarises, and earlier pieces by name; link to the most official page; never "click here" or a bare address; never force a new tab.
6. Real people appear only as they really were, attributed and linked; characters never meet real people in made-up scenes. If Charli-Jo has read the source themself, their account stands, but link it. When a character mentions the person behind an experiment, they say Charlotte Joanne (she/her), sometimes "Charli"; leave that as written.
7. For a character piece, include a "Behind the fiction" note saying which parts are real and sourced. Anything with a fact you cannot check goes in `carrados/parked/` with a line in its README, not into the site.
8. Run `npm ci` and `npm run build:carrados` (it refuses a `#` heading outside code). Open a PR; it deploys when merged.
