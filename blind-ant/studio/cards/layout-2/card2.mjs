// Blind Ant Cards, layout 2: a card opened out flat.
// The front is the picture, full bleed and square, with the headline set over it as real text.
// Below the fold is the inside, a cream square of the same size: "Dear …", the message, the closing, the sender,
// and at the foot the Blind Ant Cards mark with "Made with Blind Ant Cards".
//
// The page is always 360 × 720 pt: two squares, about one phone screen. The inside doesn't grow; a message
// that doesn't fit is refused kindly (TOO_LONG) rather than shrunk.
//
// Drawn in reading order as well as tagged in it: picture, headline, recipient, message, closing, sender, footer.
// Everything else (the shade behind the headline, the cream, the fold, the mark) is an artifact, so screen readers skip it.

export const WIDTH = 360;
export const FRONT = 360;
export const HEIGHT = FRONT * 2;
const MARGIN = 34;
const TEXT_WIDTH = WIDTH - MARGIN * 2;
const INSIDE_TOP = FRONT + 38;
const FOOTER_SPACE = 64;                 // kept clear at the bottom of the inside for the mark and the footer line
const CREAM = '#fbf4e6';
const INK = '#2b1d14';                   // warm near-black on cream: about 15:1
const SOFT = '#6b3a2a';                  // footer on cream: about 8:1
const HEADLINE = '#fff6e6';
const BERRY = '#a3172a';

// A design: its picture is a JPEG or PNG (as bytes), made in Blender from the description.
export function design(id, title, headline, description, image) {
  return { id, title, headline, description, image };
}

const paragraphs = (text) => String(text).replace(/\r\n?/g, '\n').split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);

function insideBlocks(card) {
  const list = [{ tag: 'P', text: `Dear ${card.recipientName},`, font: 'Regular', size: 17, after: 12 }];
  for (const p of paragraphs(card.message)) list.push({ tag: 'P', text: p, font: 'Regular', size: 15.5, after: 10, lineGap: 3 });
  if (card.closing) list.push({ tag: 'P', text: `${card.closing.replace(/,\s*$/, '')},`, font: 'Regular', size: 17, before: 8, after: 2 });
  list.push({ tag: 'P', text: card.senderName, font: 'Bold', size: 19, before: card.closing ? 0 : 8, after: 0 });
  return list;
}

function setup(PDFDocument, fonts, extra = {}) {
  const doc = new PDFDocument({ size: [WIDTH, HEIGHT], margin: 0, font: fonts.regular, ...extra });
  doc.registerFont('Regular', fonts.regular);
  doc.registerFont('Bold', fonts.bold);
  return doc;
}

// How far down the inside the text reaches, measured with the same fonts and widths.
export function measure(PDFDocument, fonts, card) {
  const doc = setup(PDFDocument, fonts);
  let y = INSIDE_TOP;
  for (const b of insideBlocks(card)) {
    doc.font(b.font).fontSize(b.size);
    y += (b.before || 0) + doc.heightOfString(b.text, { width: TEXT_WIDTH, lineGap: b.lineGap || 0 }) + b.after;
  }
  return y;
}

export const fits = (PDFDocument, fonts, card) => measure(PDFDocument, fonts, card) <= HEIGHT - FOOTER_SPACE;

// The Blind Ant Cards mark, drawn small: a little ant walking left to right. A placeholder until the real mark is made.
function antMark(doc, cx, cy, s, color) {
  doc.save().fillColor(color).strokeColor(color).lineWidth(0.9 * s).lineCap('round');
  doc.circle(cx - 7 * s, cy, 3.2 * s).fill();        // abdomen
  doc.circle(cx, cy - 0.6 * s, 2.2 * s).fill();      // thorax
  doc.circle(cx + 5.5 * s, cy - 1.6 * s, 2.5 * s).fill(); // head
  for (const [dx, a, b] of [[-1.5, -4, 5], [0, 0, 5.5], [1.5, 4, 5]]) {  // six legs
    doc.moveTo(cx + dx * s, cy).lineTo(cx + (dx + a * 0.5) * s, cy + 3 * s).lineTo(cx + (dx + a) * s, cy + b * s).stroke();
    doc.moveTo(cx + dx * s, cy - 1 * s).lineTo(cx + (dx + a * 0.5) * s, cy - 4 * s).lineTo(cx + (dx + a) * s, cy - 6.5 * s).stroke();
  }
  doc.moveTo(cx + 7 * s, cy - 3.2 * s).quadraticCurveTo(cx + 9 * s, cy - 8 * s, cx + 11.5 * s, cy - 7.5 * s).stroke(); // antennae
  doc.moveTo(cx + 6.5 * s, cy - 3.6 * s).quadraticCurveTo(cx + 7 * s, cy - 9 * s, cx + 9.5 * s, cy - 9.8 * s).stroke();
  doc.restore();
}

export function makeCard(PDFDocument, fonts, card, d) {
  if (!fits(PDFDocument, fonts, card)) throw Object.assign(new Error('This message is too long for the card.'), { code: 'TOO_LONG' });

  const doc = setup(PDFDocument, fonts, {
    pdfVersion: '1.7', subset: 'PDF/UA', tagged: true, displayTitle: true, lang: 'en-GB',
    info: { Title: `${d.headline}: a card from ${card.senderName}`, Author: card.senderName, Subject: `${d.title}: a card made with Blind Ant Cards`, Creator: 'Blind Ant Cards' },
  });
  const root = doc.struct('Document');
  doc.addStructure(root);

  // 1. The front: the picture, full bleed.
  root.add(doc.struct('Figure', { alt: d.description }, () => { doc.image(d.image, 0, 0, { width: WIDTH, height: FRONT }); }));

  // A soft shade at the top of the picture, so the headline stays readable over any light.
  doc.markContent('Artifact', { type: 'Layout' });
  const shade = doc.linearGradient(0, 0, 0, 150);
  shade.stop(0, '#000000', 0.55).stop(1, '#000000', 0);
  doc.rect(0, 0, WIDTH, 150).fill(shade);
  doc.endMarkedContent();

  // 2. The headline, over the picture.
  doc.font('Bold').fontSize(31).fillColor(HEADLINE);
  root.add(doc.struct('H1', () => { doc.text(d.headline, MARGIN - 10, 34, { width: TEXT_WIDTH + 20, align: 'center', lineGap: 2 }); }));

  // The inside: cream paper, with a faint shadow where the card folds.
  doc.markContent('Artifact', { type: 'Layout' });
  doc.rect(0, FRONT, WIDTH, FRONT).fill(CREAM);
  const fold = doc.linearGradient(0, FRONT, 0, FRONT + 14);
  fold.stop(0, '#5a3a20', 0.28).stop(1, '#5a3a20', 0);
  doc.rect(0, FRONT, WIDTH, 14).fill(fold);
  doc.endMarkedContent();

  // 3 to 6. Recipient, message, closing, sender.
  let y = INSIDE_TOP;
  for (const b of insideBlocks(card)) {
    y += b.before || 0;
    doc.font(b.font).fontSize(b.size).fillColor(INK);
    const opts = { width: TEXT_WIDTH, lineGap: b.lineGap || 0 };
    const h = doc.heightOfString(b.text, opts);
    root.add(doc.struct(b.tag, () => { doc.text(b.text, MARGIN, y, opts); }));
    y += h + b.after;
  }

  // 7. The foot of the inside: the mark (decoration) and "Made with Blind Ant Cards" (real text).
  doc.markContent('Artifact', { type: 'Layout' });
  antMark(doc, WIDTH / 2 - 2, HEIGHT - 46, 1.5, BERRY);
  doc.endMarkedContent();
  doc.font('Regular').fontSize(10).fillColor(SOFT);
  root.add(doc.struct('P', () => { doc.text('Made with Blind Ant Cards', 0, HEIGHT - 28, { width: WIDTH, align: 'center' }); }));

  root.end();
  doc.end();
  return doc;
}
