// node make.mjs <picture.jpg> <out.pdf> [long]
// Makes the Christmas With Love sample card with layout 2. Needs pdfkit@0.20.2 installed beside it (see ../README.md).
import { readFileSync, createWriteStream } from 'node:fs';
import { fileURLToPath } from 'node:url';
import PDFDocument from 'pdfkit';
import { makeCard, design, measure, HEIGHT } from './card2.mjs';

const [pic, out, mode] = process.argv.slice(2);
const F = fileURLToPath(new URL('../fonts/', import.meta.url));
const fonts = { regular: readFileSync(F + 'AtkinsonHyperlegibleNext-Regular.ttf'), bold: readFileSync(F + 'AtkinsonHyperlegibleNext-Bold.ttf') };

const d = design('christmas-with-love', 'Christmas With Love', 'With Love at Christmas',
  'Two lit candles glow side by side on a dark wooden table, among glossy holly leaves and clusters of red berries, with soft golden lights blurred in the darkness behind them.',
  readFileSync(pic));

let message = 'Wishing you a wonderful Christmas, full of good food, good company and at least one excellent nap.\n\nThank you for everything this year. It wouldn\'t have been the same without you.';
if (mode === 'long') message = Array(8).fill(message).join('\n\n');
const card = { recipientName: 'Charlotte', message, closing: 'With lots of love', senderName: 'Charlotte' };

console.log('inside text reaches', Math.round(measure(PDFDocument, fonts, card)), 'of', HEIGHT - 64);
try {
  const doc = makeCard(PDFDocument, fonts, card, d);
  doc.pipe(createWriteStream(out));
  doc.on('end', () => console.log('wrote', out));
} catch (e) { console.log('refused:', e.code, e.message); }
