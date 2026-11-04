# Blind Ant Cards: studio folder

Working material for Blind Ant Cards. The plan is in Charli-Jo's files (`blind-ant-cards-plan.md`). This folder is under `blind-ant/studio/`, so **nothing here is published**.

## Milestone 1: one card as a tagged PDF

- `card.mjs` makes the card. The same code runs in the browser and in Node, so the automated checks test exactly what a browser makes.
- `browser-entry.mjs` is the browser side. It's bundled with PDFKit, svg-to-pdfkit and the two fonts into `cards.bundle.js`, which is generated: don't edit it.
- `index.html` is the test page. Open it in a browser (it works from a file or from a web address), make the card, then download or share it. Add `?selftest` to the address and it also writes the PDF into the page, for automated checks.
- `make-sample.mjs` makes the sample PDFs in Node.
- `samples/` holds the made cards: `blind-ant-christmas-card.pdf` (a normal card), `accents.pdf` (accented names), and `made-in-edge.pdf` (the same card, made by Microsoft Edge from the test page).
- `fonts/` holds Atkinson Hyperlegible Next Regular and Bold, under the SIL Open Font Licence (`OFL.txt`).
- `REPORT-milestone-1.md` is the gate report.

## Rebuilding

The libraries aren't installed in the repo, so the sites' own builds are untouched. In a separate folder:

```
npm install pdfkit@0.20.2 svg-to-pdfkit@0.1.8 esbuild
```

Then, with `NODE_PATH` pointing to that folder's `node_modules`:

```
esbuild browser-entry.mjs --bundle --format=iife --platform=browser --minify --target=es2020 --loader:.ttf=binary --define:import.meta.url='"https://blind-ant.com/"' --outfile=cards.bundle.js
node make-sample.mjs <that folder>/node_modules
```

`import.meta.url` is defined only because PDFKit uses it to find its PDF/A colour profile, which this card doesn't use.
