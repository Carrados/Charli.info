---
title: The thread
kind: object
order: 1
description: Five emails over one afternoon: a bug report from a VoiceOver user, a link to a copy of the site with the fix in, "works for me", one word from the owner, and a thank-you.
label_title: The thread
label_meta: Email thread, 2026. Invented correspondence about a real bug. Written by Claude.
---

## 1. The report

*From Nadia Okafor to fix@unremarkable.me, 14:02. Subject: Your list says everything twice*

Hello,

I use VoiceOver on an iPhone. On your front page, under The work, every site is read with its number twice. Before the second site I hear "02, 2 of 5". It's only a small thing, but you say you test with a screen reader, so I thought you'd want to know.

Nadia

## 2. The mirror

*From Unremarkable to Nadia Okafor, 14:19. Subject: Re: Your list says everything twice*

Hello Nadia,

Thank you. You're right, and it's our mistake. The numbers 01 to 05 were added by our stylesheet, and VoiceOver read them as well as giving each item's place in the list.

I've built a copy of the front page with a fix. The list is now a proper numbered list, and the numbers you can see are hidden from screen readers so you'll only hear them once:

https://fix-12.unremarkable.me/

Could you try it the way you found the problem? Just reply to this email to say whether it works. Nothing changes on the real site until you do.

Unremarkable

## 3. Works for me

*From Nadia Okafor to Unremarkable, 14:40. Subject: Re: Your list says everything twice*

Works for me. "List, 5 items", then each site with no number in front. Much better.

I've never been asked to check a fix before. Usually I report something and never hear another word.

Nadia

## 4. Ship

*From Unremarkable to the owner, 14:41. Subject: Fix 12 ready: The work list read its numbers twice*

Reported by a VoiceOver user, who has tested the fix and says it works.

- **Changed:** the front page's list of work is now a numbered list, and the numbers you can see are hidden from screen readers. The Markdown version is numbered 1 to 5.
- **Words changed:** none.
- **Links changed:** none.
- **Checks:** build passed, one H1 per page, links all work, no sideways scroll at phone width.

Reply "ship" to put it live, or "hold" to keep it back.

*From the owner, 14:52*

ship

## 5. Thank you

*From Unremarkable to Nadia Okafor, 14:54. Subject: Re: Your list says everything twice*

Hello Nadia,

Your fix is live on unremarkable.me. It's also a rule now on every site we build: when things are numbered, use a numbered list and never add numbers of our own.

Thank you for telling us, and for checking it.

Unremarkable
