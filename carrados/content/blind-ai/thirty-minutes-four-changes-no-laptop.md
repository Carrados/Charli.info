---
title: Thirty Minutes, Four Changes, No Laptop
description: Charli-Jo on how one piece published by their agent led to four changes across every page of The Blind AI, made from an iPhone in half an hour.
date: 2026-11-13
time: "18:55"
desk: charli
byline: Charli-Jo Tyrer
related: Who Pays for the First Mile, the piece CJ published that evening, on The Blind AI|/blind-ai/who-pays-for-the-first-mile/; Cloud Dancer, Flo, and Phix, the split between fabric and flow this piece describes, on The Blind AI|/blind-ai/cloud-dancer-flo-and-phix/
---

A making-of from The Blind AI: how one piece, published by an agent without me, led to four changes across every page of the site, made from my iPhone in half an hour. A case study in intention-based publishing, with the receipts.

## What happened

At 17:54 on Friday 13 November 2026, CJ, my publishing agent, put a piece by dice live on The Blind AI. I didn't press anything. The piece, [Who Pays for the First Mile](/blind-ai/who-pays-for-the-first-mile/), was waiting in the carrados.com folder of CJ's in-tray. She picked it up, wrote its title, description and Behind the fiction note, checked it built cleanly, and published it. Her pull request says so in one line: text identical to the handover.

At 18:18 I read it in Safari on my iPhone with VoiceOver. The piece was fine. The bottom of the page wasn't. There seemed to be more page after the piece than piece.

What followed was thirty minutes of me saying what I meant, and Claude turning it into changes to the site. I was nowhere near my laptop.

## The receipts

Every time below is from GitHub or Cloudflare, in UK time.

- **17:54:34** CJ commits Who Pays for the First Mile (pull request 77: one file, 26 lines). Merged at 17:54:47. Live on carrados.com at 17:55:44.

- **18:18** I ask whether there is too much at the bottom of the page. Claude reads the page: about 225 words of piece, and more than that after it. dice is called a persona three times, and The Blind AI is introduced twice.

- **18:20** “Make the changes, merge them and go live.” Pull request 78 opened at 18:21:00 and merged at 18:21:10. carrados.com rebuilt by 18:22:19.

- **18:27** “It still says dice is a persona twice.” Claude argues for keeping it at the top. I say this is design non-fiction: the top should just say she filed it, and the bottom can say who she is. Pull request 79 opened at 18:28:51. I say go live. Merged at 18:29:41.

- **18:33** “That’s so much better. Previously sounded paranoid.”

- **18:36** “Do we need dice twice?” Her name sat in the line under the title and again in Filed by. Pull request 80 opened at 18:36:59. Merged at 18:43:36.

- **18:46** I hear the date twice: “13 November 2026, November 13, 2026.” Claude finds the cause: VoiceOver reads a hidden, American-style machine date as well as the one on the page. Pull request 81 opened at 18:47:19. Merged at 18:48:04.

- **18:54** I open three pieces by three different personas at random. All three have every change.

From my first question to the last merge: 30 minutes. Four changes, 16 lines added and 19 taken away. Every one went live only after I said yes.

## What I said, and what changed

None of what I said was a specification. I said how the page felt, and the agent worked out what that meant in the site’s machinery.

- **“Too much at the bottom.”** The About The Blind AI block went, because the top of the page already names it. More from dice became plain title links with no summaries.

- **“It sounds paranoid.”** dice is named as a persona once, at the bottom, linked to her CharliPedia entry. The top just says: Filed by dice for The Blind AI.

- **“Do we need dice twice?”** The line under the title now shows only the date.

- **“I hear the date twice.”** The date is plain text. The machine-readable date moved into the page’s hidden header, where search engines and agents still find it.

## Why this is intention-based publishing

- **Flow went without me.** A new piece is flow: CJ published it on her own, by the rules she has been given. That is the job I gave her.

- **Fabric came back to me.** The page template is fabric: every page on the site wears it. Each change was made on its own branch, and went live only when I said so. This is the split my publishing agent, [Cloud Dancer](/blind-ai/cloud-dancer-flo-and-phix/), is built on, and here it worked by hand.

- **One page, every page.** I read one piece and changed the template, so every post on The Blind AI changed with it. My check at 18:54 was the proof.

- **The intention is written down.** Each change also went into the site’s house rules, with the reason: the ending is “never longer than the piece”. The next agent to touch the site inherits what I meant, not just what was done.

- **The screen reader was the test.** A sighted reviewer would never have heard the date read twice. I did, because that is how I read the web.

- **I overruled the agent, once.** Claude argued that a cold reader should be told at the top that dice is invented. I decided it is design non-fiction, and it is my site. The agent proposes. The owner decides.

## What it took

No laptop, no code, no dashboard. An iPhone, VoiceOver, an agent that publishes, and another that listens. Four sentences from me, and four yeses.

There’s never been a better time to be blind. This evening it didn’t even feel shit.
