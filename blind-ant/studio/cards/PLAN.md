# Blind Ant Cards: the plan

The single, current plan for Blind Ant Cards. It merges Charli-Jo's *Build Brief 1.0*, Claude's working plan, and every decision made with Charli-Jo up to **4 November 2026**. Where this file and an older note disagree, this file wins. Update it whenever a decision is made.

## Where things stand (5 November 2026)

- **Launch:** Tuesday 1 December 2026, with the Christmas collection. Confirmed by Charli-Jo.
- **Milestone 1 (the PDF proof) is done:** a tagged, real-text PDF made in the browser with PDFKit. Charli-Jo tested it on iPhone with VoiceOver (Files, Mail, WhatsApp, how it looks, Share): **"everything works perfectly."** See `REPORT-milestone-1.md`.
- **Layout 2 and the first Blender picture are made:** *Christmas With Love* (`designs/christmas-with-love/`, `layout-2/`, `samples/christmas-with-love.pdf`). GPT read the PDF and described it accurately: nothing clipped, the headline clear of the flames. **A sighted person is checking it next.** No screen reader has read layout 2 yet.
- **5 November: the Sloppy Jo style goal and Christmas With Love round 2.** Charli-Jo set the *Sloppy Jo vision* (Synthetic Realism) as the style goal for the pictures. Round 1 was reviewed against it (competent, not yet convincing) and rebuilt as round 2: the two candles lean in together, the taller one just behind as if protecting the smaller and sharing its light (Charli-Jo's idea). The description was rewritten first. The sample PDF still uses round 1 until it's remade. Round 3 had a sighted check, with no hint of the idea (`designs/christmas-with-love/sighted-check-r3.md`): the protective lean and the shared light both read. Its seven words were love, warmth, togetherness, tenderness, peace, hope and remembrance. **Charli-Jo likes "remembrance"**, so the card may hold that meaning too. Round 4 fixes what didn't read. Round 4 was checked by GPT and Gemini (`sighted-check-r4.md`); round 5 strengthened the small candle's lean and made the melt pools visible. **Charli-Jo: round 5 is the last AI round; next, human eyes look at it.** Not yet approved.
- **Not done:** NVDA with Acrobat and Edge; veraPDF (needs portable Java, about 105 MB of downloads, waiting for Charli-Jo's go-ahead); PAC; Android and Windows sharing.
- **Code:** branch `claude/cards-pdf-proof`, pull request Carrados/Charli.info#38. Everything is under `blind-ant/studio/`, which is never published. Charli-Jo merges pull requests themself (Claude's merges are blocked by auto mode).

## The vision: all year round

Blind Ant Cards runs **all year, with accessible cards for every occasion**. Christmas 2026 is the first collection, not the whole product. So build it once, properly:

- Each **design** is a self-contained definition (picture, description, headline, occasion) kept apart from the app's logic, so a new collection is just new designs and messages.
- **Messages** are tagged by occasion (and Christmas or seasonal within Christmas).
- Nothing in the code may assume Christmas: the PDF title comes from the headline, and the file name will become occasion-neutral (`blind-ant-card.pdf`) or per occasion.
- Occasions to come (not yet decided or ordered): birthdays, thank you, thinking of you or sympathy, get well, new baby, weddings and anniversaries, Valentine's, Mother's and Father's Day, Easter, Eid, Diwali, Hanukkah, Lunar New Year.

## What it is

A free web app on Blind Ant. You choose a card, write a message, add names, preview it, then download or share it. The card is a **digital PDF made entirely in the visitor's browser**, that a blind person can make on their own and a blind recipient can read.

**The promise (from the brief):** making something lovely for another person shouldn't depend on being able to see. It's not a specialist tool for disabled people; it's a beautiful card maker designed for everyone. *A little love, beautifully made. For everyone.*

No accounts, no server, no database, no email service, no analytics on what people type, nothing in web addresses, no AI-written verses, no third parties at run time (the PDF library and fonts are served from blind-ant.com).

## Decisions

| Topic | Decision |
|---|---|
| **Format** | Digital only. No printed or folded card. No `format` field. |
| **Shape (layout 2, 4 Nov)** | A card opened out flat: **360 × 720 pt**, two squares, about one phone screen. **Front:** the picture, full bleed, with the **headline set over it** as real text. **Inside:** a cream square of the same size with "Dear …", the message, the closing, the sender, and at the foot the Blind Ant Cards mark and "Made with Blind Ant Cards". A faint fold shadow between them. |
| **Length** | The inside doesn't grow. A message that doesn't fit is refused kindly (with a count), never shrunk. At the current sizes the inside holds about 45 to 50 words in two paragraphs; the text could be made a little smaller if more room is wanted (Charli-Jo to decide). |
| **Order** | Picture → headline → recipient → message → closing → sender → footer line. **Drawn in this order as well as tagged in it**, so it reads right in viewers that ignore tags (Apple Preview, iPhone). Everything else (the shade behind the headline, the cream, the fold, the mark) is an artifact. |
| **Pictures (4 Nov)** | **Made in Blender** (5.2, on Charli-Jo's computer), not SVG. The description is **written first and always true**; the scene is modelled in code to match it. No image generators. After a render, someone (GPT, a sighted person) describes it, and anything they see that the description lacks is added (the gold baubles were added this way). |
| **Style (5 Nov)** | **The Sloppy Jo vision: Synthetic Realism** (Charli-Jo's file `Documents/narrative web/AW26 Found Girls/Sloppy Jo/sloppy-jo-vision.md`). Conviction, not belief: design before realism, elegant geometry, rich materials with no added wear, expressive lighting, a palette fixed in one sentence before modelling, a focal point named in one sentence, and an exceptional finish at phone size. For each picture: propose three treatments, recommend one, build what Charli-Jo chooses, and review against the intentions, never against photographic likeness. Christmas With Love sets the family's material language: luminous alabaster wax, lacquered holly, true gold, light from the flames themselves, on deep oxblood-black. |
| **Headline** | Real text, never in the picture. Each scene leaves the **top third calm** (sky, dark, bokeh) for it. Cream, bold, with a soft dark shade behind it for contrast. |
| **Design names** | Named by the picture (*The Christmas Robin*), not the headline. |
| **Words** | Always **message** and **closing**; never "greeting" for either. |
| **Sharing** | **Share or email your card** (Web Share with the file, only where `canShare` says files work) plus **Download your card** always, plus **Copy greeting**. No `mailto:`. After sharing: "Your card is ready to send", never "Sent". |
| **Font** | Atkinson Hyperlegible Next, Regular and Bold, embedded (OFL). |
| **Emoji** | Not supported by the font: they come out as empty boxes. **To decide:** black-and-white emoji font, or tell visitors plainly. |
| **PDF title** | Currently "<headline>: a card from <sender>". It shows in some viewers' title bars. **To decide** whether the sender's name stays. |
| **Where it lives** | A Blind Ant Piece at blind-ant.com/pieces/blind-ant-cards/ with a making-of (the ending is added by the build). Charli-Jo has called it a "micro site": **to decide** whether it should have its own address such as cards.blind-ant.com. |
| **Mark** | There's no Blind Ant logo yet. The little red ant in layout 2 is a **placeholder** drawn in code. The real Blind Ant Cards mark still needs designing (possibly in Blender). |

## The Christmas 2026 collection

All seven festive, wintery, warm and giftable, one visual family (palette, headline type, shade, inside, fold). They differ in headline, mood and picture. Working names; art direction from Charli-Jo's lineup.

| # | Design | Headline | Mood | Blender difficulty | State |
|---|---|---|---|---|---|
| 1 | The Christmas Robin | Merry Christmas | Traditional | Hardest (a creature): make it a round ornament-style robin; fallback a robin silhouette | Placeholder SVG only |
| 2 | Snow at Christmas | Merry Christmas | Snowy village or landscape | Medium (distance and lit windows help) | Not started |
| 3 | A Starry Night | Season's Greetings | Elegant stars, night sky | Easy | Not started |
| 4 | Christmas by the Fire | Happy Christmas | Cosy festive interior | Medium (fire: close-up glow, stockings, blur) | Not started |
| 5 | The Christmas Tree | Merry Christmas | Decorative festive design | Easy to medium (the lights do the work) | Not started |
| 6 | Christmas With Love | With Love at Christmas | Romantic: candlelight, holly, richer colours | Easy | **Round 2 made** (5 Nov, Sloppy Jo) |
| 7 | Winter Wishes | Happy Holidays | Winter, not Christmas: snow, trees, moonlight | Easy | Not started |

About twelve suggested messages, tagged Christmas or seasonal; Winter Wishes shows the seasonal ones first. Traditional, warm, humorous, romantic, short, for friends or family. Visitors can always write their own.

**Picture schedule:** style settled on Christmas With Love → the other six two or three at a time with Charli-Jo reviewing each batch → robin last → final renders, file sizes, descriptions rechecked in the last week. Time-box each scene: if one fights back after a session, simplify or change its subject.

## The app (from the brief)

Five linear stages, back and forward without losing anything, a progress indicator readable as text, no need to understand the site's navigation:

1. **Choose your card:** a radio group; each design has a visible preview, its name and its full description.
2. **Write your message:** suggestions that fill an editable box (never overwrite an edited message without warning), an accessible count against the inside's space.
3. **Personalise:** recipient (required), closing (optional), sender (required); visible labels, clear errors that name the field and move focus; any names, accents and Unicode the font has.
4. **Preview:** a visual preview and a text preview in reading order, from the same data; never announce the whole card on every keystroke.
5. **Download or share:** as above, with a file name free of personal information.

Controls are named **Continue**, **Back**, **Review your card**, **Download your card**, **Share or email your card**, **Copy greeting**. Native controls first. WCAG 2.2 AA for the app, 200% zoom and reflow. Build to `.claude/skills/voiceover-iphone-web-apps` from the start.

**Introduction (draft from the brief):** *Choose a card, write something lovely, make it personal and download it to send to someone who matters. No account. No fuss.* (The brief's version says "a Christmas card": keep it occasion-neutral.)

**Privacy (draft, check against the build):** *Your card is made in your browser. We don't receive or store the names or messages you enter. When you're happy with it, download it and share it however you like.*

## Milestones

| Milestone | What | Target |
|---|---|---|
| 1. The PDF proof | One tagged card made in the browser, checked and tested | 11 Nov, **done 4 Nov** |
| 2. Working prototype | All five stages, one design, three messages, preview, download, share, copy; keyboard alone | 18 Nov |
| 3. The collection | Seven designs, about twelve messages, styling, errors, accessibility review | 25 Nov |
| 4. Testing and fixes | Automated, keyboard, screen-reader, PDF and sharing tests; issue log and known limits | 30 Nov |
| 5. Launch | Live on Blind Ant: introduction, privacy note, help, a launch piece and a making-of | **1 Dec** |

## Parked: charity Christmas cards

Charli-Jo's note *Blind Ant Cards: Optional Charity Christmas Cards* (on their computer, `Downloads\blind-ant-cards-charity-christmas-2026-option.md`, not in this repo) describes a £10 charity delivery option. It is **parked and not approved**: revisit only after the free product works end to end, and it brings payments, storage, fundraising law and email delivery that the free app deliberately avoids. Launching free and leaving it parked is a perfectly good outcome.

## How things are made (what we learned)

See `.claude/skills/blind-ant-cards/SKILL.md`, the skill that sets Claude back up on this project. In short:

- **Blender scenes** are Python scripts run headless (`blender -b --factory-startup -P scene.py -- out.png 160 1080`), rendered with Cycles at 1080 × 1080, AgX "Punchy", with a compositor bloom for glow. **The lossless render is kept in the repo as `designs/<id>/master.png`** (Charli-Jo's rule, 4 November), and the card uses a JPEG made from it at quality 86 (about 64 KB). The finished card PDF is about 85 KB.
- **Checking a PDF:** pdf.js reads the structure tree and tagged text in Node. On this Windows ARM computer the Node canvas renderer crashes, so look at the page with pdf.js in the browser pane, served from a local folder.
- **Phone testing:** a temporary Cloudflare Worker at a secret path on workers.dev (noindex, no-store), deleted once tests are done. Never linked from anywhere.
- **Honesty:** never claim a screen-reader or device test that wasn't done, or PDF/UA without veraPDF evidence. Record who tested what, where and when.

## Still to decide

- Emoji: black-and-white emoji font, or a plain message.
- Whether the PDF title keeps the sender's name.
- Whether the inside's text is made a little smaller to hold longer messages.
- A Piece on blind-ant.com, or its own address.
- The Blind Ant Cards mark.
- Whether "Made with Blind Ant Cards" links to the site (one more thing a screen reader announces).
- The order of occasions after Christmas.
- veraPDF: go-ahead for the downloads.
