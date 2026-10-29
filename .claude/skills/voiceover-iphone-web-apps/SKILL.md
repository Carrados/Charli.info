---
name: voiceover-iphone-web-apps
description: Patterns for JavaScript web apps that must work with VoiceOver on iPhone Safari (touch, flicking), learned from Charli-Jo's live testing of Since or Until? on 29 October 2026. Use when building or fixing any interactive page or app on these sites.
---

# VoiceOver on iPhone: what works

Charli-Jo tests by flicking through the live page with VoiceOver in Safari on iPhone and pasting exactly what VoiceOver says. These are the patterns that came out of that testing (Since or Until?, pull requests #12 to #16 on 29 October 2026). Build to them from the start.

## Form questions with a hint

- Put the question and its hint together as one line of plain text inside the `legend`: `<legend>Which date? Type it in, for example 25 12 2026. Month can be a number or a name.</legend>`. VoiceOver reads it once when flicking, and once as the group's name when entering the fields.
- Don't put `aria-describedby` on a `fieldset`: VoiceOver on iPhone says the word "description" before the hint.
- Don't keep a visually hidden copy of the hint alongside a visible one, and don't split the hint into a block-level span inside the legend: iPhone reads both copies, or reads the legend and the span as separate stops.
- Keep each field's visible label, linked with `aria-labelledby` (label `aria-hidden` to avoid a double read). This read correctly as "Day, 25, text field".

## Buttons that open a dialog

- Don't add `aria-haspopup="dialog"` to a button whose name already says what it does ("Use a calendar"). On iPhone it adds "Pop up button", "Dialog pop up" and "Double tap to activate the picker". Without it: "Use a calendar, Button".
- Still move focus into the dialog on open and back to the button on close.
- "Form end" after the last control in a group is VoiceOver's own wayfinding; leave it.

## How to test and fix

- Ask Charli-Jo to flick from the page title and paste what VoiceOver says. Treat that speech as the bug report, word for word.
- Change one thing at a time and say what VoiceOver should now say.
- When iPhone behaviour is uncertain, don't guess live: put up a small noindex test page with two or three variants, let her pick, apply the winner, and remove the test page.
- This covers touch and VoiceOver on iPhone only. Keyboard access and desktop screen readers (NVDA, JAWS, VoiceOver on Mac) are separate tests; don't assume a pass here covers them.
