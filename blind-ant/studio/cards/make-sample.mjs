// Makes sample PDFs in Node with the same card.mjs the browser uses. Run from this folder:
//   node make-sample.mjs <path to a node_modules folder with pdfkit and svg-to-pdfkit>
// (They aren't installed in the repo, so the sites' builds stay untouched.)
import { readFileSync, createWriteStream, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join, resolve } from 'node:path';
import { makeCard } from './card.mjs';

const modules = resolve(process.argv[2] || 'node_modules');
const require = createRequire(join(modules, 'x.js'));
const PDFDocument = require('pdfkit');
const SVGtoPDF = require('svg-to-pdfkit');
const fonts = { regular: readFileSync('fonts/AtkinsonHyperlegibleNext-Regular.ttf'), bold: readFileSync('fonts/AtkinsonHyperlegibleNext-Bold.ttf') };

const short = {
  recipientName: 'Jane',
  message: `Wishing you a wonderful Christmas, full of good food, good company and at least one excellent nap.\n\nThank you for everything this year. It wouldn't have been the same without you.`,
  closing: 'With love',
  senderName: 'Charlotte',
};
const accents = { ...short, recipientName: 'Zoë and Siobhán', senderName: 'Aoife Ní Bhriain', message: `Joyeux Noël, and a very happy Christmas from all of us — café, crème brûlée and Søren included.` };
const long = { ...short, message: Array(9).fill(short.message).join('\n\n') };

mkdirSync('samples', { recursive: true });
const write = (name, card) => new Promise((ok, fail) => {
  try {
    const doc = makeCard(PDFDocument, SVGtoPDF, fonts, card);
    doc.pipe(createWriteStream(join('samples', name))).on('finish', ok);
  } catch (e) { e.code === 'TOO_LONG' ? (console.log(`${name}: refused as too long (${e.height} pt tall)`), ok()) : fail(e); }
});
await write('blind-ant-christmas-card.pdf', short);
await write('accents.pdf', accents);
await write('too-long.pdf', long);
console.log('done');
