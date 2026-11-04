---
name: blind-ant-cards
description: Work on Blind Ant Cards, Charli-Jo's accessible greeting-card maker (tagged PDFs made in the browser, pictures made in Blender), running all year with cards for every occasion. Use when Charli-Jo mentions Blind Ant Cards, a card design, a Christmas or occasion card, the card PDF, the card pictures in Blender, or runs /blind-ant-cards.
---

# Blind Ant Cards

## 1. Get back up to speed (do this first, every time)

1. The work lives in `C:\Users\Charli-Jo\Charli.info` (GitHub `Carrados/Charli.info`), folder `blind-ant/studio/cards/`. Until it's merged it's on branch **`claude/cards-pdf-proof`** (pull request #38). Check with `gh pr view 38 -R Carrados/Charli.info --json state`; if it's merged, work from `main` on a new `claude/cards-<topic>` branch.
2. Read, in this order:
   - `blind-ant/studio/cards/PLAN.md`: **the current plan and every decision.** It wins over older notes.
   - `blind-ant/studio/cards/REPORT-milestone-1.md`: what was proved and tested.
   - `CLAUDE.md` at the repo root: the house rules (names and pronouns, every piece is the front page, publishing, merging).
   - `.claude/skills/voiceover-iphone-web-apps/SKILL.md` before building any app page.
3. Tell Charli-Jo in two or three lines where things stand and what's next, from PLAN.md, then ask what they want to do.

Charli-Jo is **they/them**. Charlotte Joanne (she/her) is the pen name who runs Blind Ant and is shown as its author; the pen-name line appears only on Blind Ant's About page. Only GitHub account: **Carrados**. Check `gh auth status` before pushing.

## 2. The rules that never bend

- **The card is a tagged, real-text PDF made in the visitor's browser.** No server, accounts, database, email service, analytics on what people type, personal data in web addresses, AI-written verses, or third parties at run time.
- **Drawn in reading order as well as tagged in it:** picture (Figure with alt text) → headline (H1) → "Dear …" → message paragraphs → closing → sender → "Made with Blind Ant Cards". Every decoration is an artifact.
- **Every word is real text**, never painted into a picture.
- **A picture's description is written first and is always true.** The Blender scene is built to match it. After rendering, have someone describe the picture (Charli-Jo can ask GPT or a sighted person) and add anything they see that the description lacks.
- **No image generators.** Pictures are modelled in Blender (or drawn in code).
- **Text never shrinks to fit.** Too long is refused kindly.
- **Never claim a test that wasn't done.** Record who tested what, on what, and when. No PDF/UA claim without veraPDF.
- **Nothing in `blind-ant/studio/` is published.** Work goes in on a branch with a pull request; **Charli-Jo merges** (auto mode blocks Claude's `gh pr merge`; don't try to get round it).
- Nothing may assume Christmas: it runs all year, so designs and messages carry an occasion.

## 3. Files

```
blind-ant/studio/cards/
  PLAN.md                  the plan and decisions (keep it current)
  REPORT-milestone-1.md    the PDF proof and its tests
  README.md                milestone 1 files and how to rebuild the bundle
  card.mjs, browser-entry.mjs, index.html, cards.bundle.js   milestone 1 (layout 1, SVG robin)
  layout-2/card2.mjs       layout 2: 360 × 720, picture front with headline, cream inside
  layout-2/make.mjs        makes a sample card in Node
  designs/<id>/            one folder per design: README.md (headline + description), scene.py,
                           master.png (lossless render, always kept), picture.jpg (what the card uses)
  fonts/                   Atkinson Hyperlegible Next Regular and Bold (OFL)
  samples/                 made cards
```

## 4. Making a picture in Blender

Blender 5.2 is at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`. Copy `designs/christmas-with-love/scene.py` as the starting point for a new design: it builds everything from scratch in Python.

1. Write the design's `README.md` first: name, headline, description.
2. Build the scene in `scene.py`. Patterns that worked:
   - **Square 1080 × 1080**, Cycles, denoised, view transform AgX with the "Punchy" look.
   - **Leave the top third calm** for the headline: aim the camera *above* the subject (raising the target moves the subject down the frame).
   - **Soft focus does the heavy lifting:** camera depth of field at f/1.4, with small emissive spheres far behind that become golden bokeh.
   - **Candle flames:** a UV sphere with its top half narrowed into a teardrop, a dim outer emission (strength about 9) and a brighter core (about 18), with a warm point light at the flame. Strengths much higher than that blow out to white.
   - **Wax that glows near the flame:** emission driven by the object's local Z with a Map Range, rising towards the top.
   - **Holly leaves:** a bmesh fan with alternating spike and scallop widths, solidified 4 mm, glossy with a coat.
   - **Glow:** a compositor node group (`CompositorNodeTree`) with Render Layers → Glare (Bloom) → Group Output, set as `scene.compositing_node_group`. Wrap it in try/except in case the API differs.
   - Keep everything **stylised and handmade-feeling** (ceramic, felt, paper, candlelight), not photographic. Avoid creatures and people where possible; the robin is the hard one.
3. Test fast, then render properly:
   `blender -b --factory-startup -P scene.py -- test.png 32 540` (about 20 seconds), look at it with the Read tool, fix, repeat. Final: `-- master.png 160 1080`.
4. **Keep the lossless master in the repo (Charli-Jo's rule, 4 November 2026):** commit the final render as `designs/<id>/master.png`, exactly as Blender wrote it. Every other version is made from it, and it's never replaced by a compressed copy.
5. Make `picture.jpg` from the master: JPEG quality 86 with Blender itself (load the PNG, set the view transform to Standard so it isn't applied twice, `save_render`). About 64 KB.
6. Time-box: if a scene fights back for a whole session, simplify it or change its subject.

## 5. Making and checking a card

- Node libraries aren't in the repo. Install them in a scratch folder: `npm install pdfkit@0.20.2 pdfjs-dist@4.10.38`. ESM ignores `NODE_PATH`, so run scripts from that folder (copy `card2.mjs` and `make.mjs` in, and point the font path at `blind-ant/studio/cards/fonts/`).
- **Structure check (Node):** pdf.js `getDocument` → `page.getStructTree()` plus `getTextContent({ includeMarkedContent: true })` shows each tag with its text in order, and the Figure's alt text. Words joined at line breaks ("atChristmas") are just the extractor; it's fine.
- **Looking at it:** `@napi-rs/canvas` **crashes on this Windows ARM computer**. Instead, serve a folder with `python -I -m http.server <port> --bind 127.0.0.1` containing the PDF, `pdf.min.mjs`, `pdf.worker.min.mjs` (from `pdfjs-dist/build/`) and a tiny page that renders page 1 to a canvas; open it in the browser pane and screenshot or zoom. Stop the server afterwards.
- Check: one page, 360 × 720; the headline clear of the bright parts of the picture; nothing clipped; a deliberately long message refused with `TOO_LONG`.
- Give Charli-Jo the PDF (copy it into the session folder and send it), say plainly what was and wasn't tested.

## 6. Testing on a phone

Charli-Jo tests with VoiceOver on iPhone (Files, Mail, WhatsApp, Share). A phone needs a web address, so:

- Put the test page in a scratch folder at an unguessable path (`openssl rand -hex 12`), with a `_headers` file (`X-Robots-Tag: noindex, nofollow`, `Cache-Control: no-store`, `Referrer-Policy: no-referrer`).
- Deploy it as its own Worker with static assets (`wrangler.jsonc`: `workers_dev: true`, `preview_urls: false`, `assets.not_found_handling: "none"`), named like `blind-ant-cards-preview`. Wrangler is logged in to Charli-Jo's Cloudflare account.
- Check the root returns 404 and the secret path 200. Tell Charli-Jo it's private only by its address, not a login.
- **Delete it when the tests are done** (`npx wrangler delete --name <name> --force`) and record the results in the report.

## 7. Still open (check PLAN.md for the current list)

Emoji, whether the PDF title keeps the sender's name, the inside's text size, a Piece or its own address, the Blind Ant Cards mark (the red ant is a placeholder), NVDA and veraPDF, and the six remaining Christmas pictures before 25 November. Launch is **Tuesday 1 December 2026**.
