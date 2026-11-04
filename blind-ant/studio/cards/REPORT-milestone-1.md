# Blind Ant Cards: milestone 1 report (PDF proof)

4 November 2026. One card, The Christmas Robin, with a placeholder picture. Design, colours and artwork quality were out of scope.

## Summary

**A tagged, real-text PDF can be made entirely in the browser.** Microsoft Edge made one from the test page, and it is identical in structure to the Node-made samples. Every automated check I could run passed. Two things are still outstanding before the gate is fully met: the **veraPDF PDF/UA check**, which needs Java (not installed here), and **testing with real screen readers and devices**, which needs a person. One real limit was found: **emoji** aren't in the font, so they come out as empty boxes.

## The brief's gate questions

1. **Which PDF approach was chosen?** PDFKit 0.20.2 in the browser, bundled with svg-to-pdfkit 0.1.8, and Atkinson Hyperlegible Next (Regular and Bold) embedded. PDFKit really does provide tagging. I checked its code rather than relying on memory: structure elements, marked content, artifacts, alt text, document language, the shown title and PDF/UA metadata.
2. **Is the PDF tagged?** Yes. It is marked as tagged, has a structure tree (Document → Figure, H1, P…), and its pages are set to follow the structure order.
3. **Does text remain real text?** Yes. All text is real, selectable text in an embedded font. No standard PDF fonts are used. Accented names (Zoë, Siobhán, Aoife Ní Bhriain, Søren, crème brûlée) come out correctly.
4. **Is the picture description accessible?** Yes. The picture is a Figure whose alt text is the design's description. The decorative frame is marked as an artifact, so screen readers should skip it.
5. **Is reading order correct?** Yes, both ways. The structure order is picture → headline → "Dear Jane," → message paragraphs → closing → sender → "Made with Blind Ant Cards". The drawing order is the same, so viewers that ignore tags still read it correctly. Nothing is drawn outside tagged content.
6. **Which validation checks passed or failed?** See below. Passed: every automated check I could run. Not run: veraPDF and PAC.
7. **What still requires human testing?** See below: all screen-reader and device testing.

## What was checked, and how

| Check | Tool | Result |
|---|---|---|
| Made in a real browser | Microsoft Edge (headless), test page `?selftest` | Made; "Your card is ready." |
| Tagged, with a structure tree | pdf.js reading the file | Document → Figure (with alt text), H1, 6 × P |
| Alt text on the picture | pdf.js structure tree | "A small robin with a round red breast sits on a snow-covered branch beneath a pale winter sky." |
| Decoration marked as artifact | pdf.js operator list | The frame is inside an Artifact. No drawing outside marked content. |
| Text in drawing order | pdf.js text content | Merry Christmas · Dear Jane, · message · With love, · Charlotte · Made with Blind Ant Cards |
| Language | catalogue `/Lang` | en-GB |
| Title, shown as title | document info + `DisplayDocTitle` | "A Christmas card from Charlotte", shown |
| PDF/UA identification | XMP metadata | `pdfuaid:part 1` present |
| Fonts embedded, no standard fonts | file contents | 2 embedded TrueType fonts, no Helvetica, Times or Courier |
| Accented names | sample `accents.pdf` | Correct as text and on the page |
| Page size grows with the message | samples | 360 × 586 pt (normal), 360 × 527 pt (short). One page. |
| Height limit | 9-paragraph message | Refused: 1,730 pt is over the 720 pt limit. The app shows a kind message instead of shrinking the text. |
| Looks right: no overlap or cut-off text | rendered with pdf.js and checked by eye | Clean |
| **Emoji** | 🎄❤️ in a message | **Fails:** empty boxes on the page, blank characters as text |

## Not done yet

**Automated, but needs a download first:**
- **veraPDF** (the PDF/UA-1 checker) needs Java, which isn't installed on this computer. With your go-ahead I can download a portable Java (Eclipse Temurin, about 45 MB, from adoptium.net) and veraPDF (about 60 MB, from verapdf.org) into a temporary folder and run it. Neither installs anything into Windows.

**Needs a person (I can't do these, and won't claim them):**
- **PAC** (PDF Accessibility Checker, Windows).
- **NVDA** (installed on this computer) with Acrobat Reader, and with the Edge PDF viewer: does it read the description, then the headline, recipient, message, closing and sender, and skip the frame?
- **VoiceOver on iPhone**, opening the PDF from Files, Mail and WhatsApp.
- **How it looks** in Acrobat, Edge, Chrome, Apple Preview and on an iPhone: is the width comfortable, and does it open fitted to the width?
- **Sharing**: open `index.html` and tap Share. On iPhone, does Mail, Messages or WhatsApp appear with the card attached? On Android, Gmail? In Chrome and Edge on Windows, which email apps appear? In Firefox, does the Share button correctly stay hidden?

For the phone tests, the test page needs to be reachable at a web address. That would mean putting this folder somewhere private, such as a preview, which is a decision for you.

## Limits found

1. **Emoji aren't supported.** Atkinson Hyperlegible Next has no emoji. A monochrome emoji font could be added, but PDFKit can't embed colour emoji, so they'd be black-and-white. The alternative is that the app tells the visitor plainly that emoji can't go on the card. **To decide.**
2. **The document title includes the sender's name** ("A Christmas card from Charlotte"). That's not a privacy problem (the file never leaves the visitor's control), but it shows in some viewers' title bars. **To decide.**
3. **The bundle is 758 KB**, including both fonts. Fine for a card maker, but the app should load it only when the visitor reaches the download stage.
4. PDF/UA is claimed in the file's metadata. Until veraPDF passes, that's a claim, not evidence.

## Recommendation

The approach works. I'd accept PDFKit as the method once veraPDF passes and you've heard the card read by NVDA and VoiceOver. Next would be milestone 2: the five stages with one design.
