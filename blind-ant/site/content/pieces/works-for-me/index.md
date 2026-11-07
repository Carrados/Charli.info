---
title: Works For Me
kind: piece
related: Unremarkable, the studio whose site heals itself here|https://unremarkable.me/; Zero Information Casualty, the standard the site is built to|https://zeroinformationcasualty.org/
order: 30
description: A website that fixes itself when a stranger emails to say it's broken, then waits for that stranger to say "works for me" before it trusts the fix.
label_title: Works For Me
label_meta: Piece, 2026. Design fiction in three Objects: an email thread, the design, and the fix that was held. Directed by Charlotte Joanne; written by Claude.
label: |
  A website that fixes itself when a stranger emails to say it's broken, then waits for that stranger to say "works for me" before it trusts the fix.
---

## About the Piece

"Works for me" is what a developer says when a bug report can't be reproduced, and it usually ends the conversation. This Piece turns the phrase around. It imagines a website that answers a bug report by building a copy of itself with the fix in, sends the reporter the link, and puts nothing live until the person who found the problem says the fix works for them.

The site is real: [Unremarkable](https://unremarkable.me/), a studio that designs and builds websites. The bug is real too. The loop doesn't exist yet. This Piece is how we decided to build it.

## Objects

<!-- objects -->

## Behind the fiction

- **Real:** Unremarkable and unremarkable.me. The bug in the email thread happened on 7 November 2026. The list of sites on the front page was numbered by the stylesheet, so VoiceOver read "02, 2 of 5" and gave each number twice. It was fixed that day by making the list a real numbered list, and the rule "use a numbered list, never add numerals" came out of it.
- **Real:** the automated check. The front page scored 10 out of 10 on [WAVE](https://wave.webaim.org/), WebAIM's accessibility checker, with the bug still in it. WAVE recognised the list and gave the page full marks. None of its checks caught the numbers VoiceOver read twice. A test written for this bug could catch it. Nobody had written one.
- **Invented:** Nadia Okafor, who reports the bug, and the person who tries to sneak a link onto the site. Neither is real, and neither email was sent.
- **Not built yet:** the loop. Everything in The design is a plan. The pieces it names are real: Cloudflare Email Routing, Workers preview addresses and Claude.
