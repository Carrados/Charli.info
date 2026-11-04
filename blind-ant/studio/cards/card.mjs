// Blind Ant Cards, milestone 1: one card as a tagged PDF.
// The same function runs in the browser (bundled into cards.bundle.js) and in Node (for automated checks),
// so what is checked is exactly what a visitor's browser makes.
//
// The card is a long digital card: a fixed width shaped for a phone, and a height that grows with the message,
// up to MAX_HEIGHT. It is drawn in reading order as well as tagged in it, so it reads correctly in viewers that
// ignore tags (Apple Preview, iPhone): picture, headline, recipient, message, closing, sender, footer line.
// Design and colours are placeholders: milestone 1 tests structure, not looks.

export const WIDTH = 360;            // points (about 12.7 cm)
export const MAX_HEIGHT = WIDTH * 2; // past this, desktop viewers set to "fit page" show it too small
const MARGIN = 30;
const PICTURE_HEIGHT = 200;
const TEXT_WIDTH = WIDTH - MARGIN * 2;
const INK = '#1f1f1f';               // on white: about 16:1
const SOFT = '#555555';              // footer on white: about 7.5:1

// The placeholder design. In the real app, designs live in their own definitions.
export const ROBIN = {
  id: 'christmas-robin',
  title: 'The Christmas Robin',
  headline: 'Merry Christmas',
  description: 'A small robin with a round red breast sits on a snow-covered branch beneath a pale winter sky.',
  // Deliberately plain: a sky, a branch with snow on it, and a robin made of circles. Drawn in code, no text inside.
  svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 200" width="360" height="200">
  <rect width="360" height="200" fill="#dfe9f2"/>
  <path d="M0 150 Q120 130 360 140 L360 150 Q120 142 0 160 Z" fill="#6b4a32"/>
  <path d="M0 150 Q120 128 360 138 L360 141 Q120 132 0 154 Z" fill="#ffffff"/>
  <ellipse cx="190" cy="118" rx="34" ry="28" fill="#7a5a3c"/>
  <circle cx="168" cy="96" r="18" fill="#7a5a3c"/>
  <ellipse cx="180" cy="120" rx="20" ry="18" fill="#c8402d"/>
  <circle cx="163" cy="92" r="3" fill="#1f1f1f"/>
  <path d="M150 97 L141 100 L150 102 Z" fill="#e0a030"/>
  <path d="M222 112 L250 104 L246 122 Z" fill="#5e4430"/>
</svg>`,
};

// Paragraphs come from blank lines in the message; single line breaks stay inside a paragraph.
const paragraphs = (text) => String(text).replace(/\r\n?/g, '\n').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);

// Text styles, in reading order. Each block is one structure element.
function blocks(card, design) {
  const list = [
    { tag: 'H1', text: design.headline, font: 'Bold', size: 30, align: 'center', before: 22, after: 18 },
    { tag: 'P', text: `Dear ${card.recipientName},`, font: 'Regular', size: 17, before: 0, after: 12 },
  ];
  for (const p of paragraphs(card.message)) list.push({ tag: 'P', text: p, font: 'Regular', size: 16, before: 0, after: 12, lineGap: 3 });
  if (card.closing) list.push({ tag: 'P', text: `${card.closing},`, font: 'Regular', size: 17, before: 10, after: 2 });
  list.push({ tag: 'P', text: card.senderName, font: 'Bold', size: 19, before: card.closing ? 0 : 10, after: 0 });
  list.push({ tag: 'P', text: 'Made with Blind Ant Cards', font: 'Regular', size: 10, color: SOFT, align: 'center', before: 28, after: 0 });
  return list;
}

// Works out the page height before drawing, using the same fonts and widths.
export function measure(PDFDocument, fonts, card, design = ROBIN) {
  const doc = new PDFDocument({ size: [WIDTH, 2000], margin: 0, autoFirstPage: true, font: fonts.regular }); // our font as the default: the browser build has no standard fonts
  doc.registerFont('Regular', fonts.regular);
  doc.registerFont('Bold', fonts.bold);
  let y = PICTURE_HEIGHT;
  for (const b of blocks(card, design)) {
    doc.font(b.font).fontSize(b.size);
    y += b.before + doc.heightOfString(b.text, { width: TEXT_WIDTH, align: b.align || 'left', lineGap: b.lineGap || 0 }) + b.after;
  }
  return Math.ceil(y + MARGIN);
}

// Makes the card. Returns the PDFKit document (already ended): pipe it, or collect its 'data' events.
// Throws { code: 'TOO_LONG' } if the card would be taller than MAX_HEIGHT, so the app can explain instead of shrinking text.
export function makeCard(PDFDocument, SVGtoPDF, fonts, card, design = ROBIN) {
  const height = measure(PDFDocument, fonts, card, design);
  if (height > MAX_HEIGHT) throw Object.assign(new Error('This message is too long for the card.'), { code: 'TOO_LONG', height });

  const doc = new PDFDocument({
    size: [WIDTH, height],
    font: fonts.regular, // our embedded font as the default, never a standard PDF font
    margin: 0,
    pdfVersion: '1.7',
    subset: 'PDF/UA',
    tagged: true,
    displayTitle: true,
    lang: 'en-GB',
    info: { Title: `A Christmas card from ${card.senderName}`, Author: card.senderName, Subject: `${design.title}: a card made with Blind Ant Cards`, Creator: 'Blind Ant Cards' },
  });
  doc.registerFont('Regular', fonts.regular);
  doc.registerFont('Bold', fonts.bold);

  const root = doc.struct('Document');
  doc.addStructure(root);

  // 1. The picture: a figure with its description.
  root.add(doc.struct('Figure', { alt: design.description }, () => {
    SVGtoPDF(doc, design.svg, 0, 0, { width: WIDTH, height: PICTURE_HEIGHT, assumePt: true });
  }));

  // 2 to 7. The text, in reading order.
  let y = PICTURE_HEIGHT;
  for (const b of blocks(card, design)) {
    y += b.before;
    doc.font(b.font).fontSize(b.size).fillColor(b.color || INK);
    const opts = { width: TEXT_WIDTH, align: b.align || 'left', lineGap: b.lineGap || 0 };
    const h = doc.heightOfString(b.text, opts);
    root.add(doc.struct(b.tag, () => { doc.text(b.text, MARGIN, y, opts); }));
    y += h + b.after;
  }

  // Decoration last in the drawing, marked as an artifact so screen readers skip it: a thin frame round the card.
  doc.markContent('Artifact', { type: 'Layout' });
  doc.save().lineWidth(1.5).strokeColor('#c8402d').rect(8, 8, WIDTH - 16, height - 16).stroke().restore();
  doc.endMarkedContent();

  root.end();
  doc.end();
  return doc;
}
