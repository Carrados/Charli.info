// Browser entry for the milestone 1 test page. Bundled with esbuild into cards.bundle.js (see README.md).
// Everything happens in this browser: the card's names and message never leave it.
// The fonts are built into the bundle, so the page also works opened straight from a file.
import PDFDocument from 'pdfkit'; // esbuild picks the package's browser build
import SVGtoPDF from 'svg-to-pdfkit';
import regular from './fonts/AtkinsonHyperlegibleNext-Regular.ttf';
import bold from './fonts/AtkinsonHyperlegibleNext-Bold.ttf';
import { makeCard, MAX_HEIGHT } from './card.mjs';

// Collects the finished PDF into a File, named without any personal information.
function toFile(doc) {
  return new Promise((resolve) => {
    const chunks = [];
    doc.on('data', (c) => chunks.push(c));
    doc.on('end', () => resolve(new File(chunks, 'blind-ant-christmas-card.pdf', { type: 'application/pdf' })));
  });
}

export function buildCardFile(card) {
  return toFile(makeCard(PDFDocument, SVGtoPDF, { regular, bold }, card));
}

window.BlindAntCards = { buildCardFile, MAX_HEIGHT };
