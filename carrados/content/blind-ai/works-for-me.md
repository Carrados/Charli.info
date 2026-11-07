---
title: Works for me
description: Charli-Jo reports a bug on their own website, gets an email with a proposed fix to test, listens, says "works for me", and the change goes live in under ten minutes.
date: 2026-11-07
time: "20:15"
desk: charli
byline: Charli-Jo Tyrer
related: Works For Me, the design fiction on Blind Ant|https://blind-ant.com/pieces/works-for-me/; Fix 2, the first real fix, on Blind Ant|https://blind-ant.com/pieces/works-for-me/fix-2/
---

This evening, Blind Ant published a design fiction about a website that fixes itself.

This evening I used it.

It started with an accessibility bug on my own site, [Unremarkable](https://unremarkable.me/). VoiceOver read the numbers in a list twice. [WAVE](https://wave.webaim.org/), the accessibility checker, gave the page 10 out of 10 with the bug still there.

Full marks. Still annoying to use.

The fiction became [Works For Me](https://blind-ant.com/pieces/works-for-me/): a website receives a report, builds a copy of itself with a proposed fix, and asks the person who found the problem to try it. The owner decides whether it goes live.

Then we started building it.

Every page on unremarkable.me now has a "Fix something on this page" link. The form knows which page you came from. It asks what happened, what you expected and how you were reading it.

It doesn't ask who you are. No email address is collected. For now, proposed fixes come only to me.

The first real report was mine. A sentence on the homepage sounded like smug nonsense when read aloud. Claude read the report and built a proposed new version of the page, at its own web address. The live page stayed as it was.

Then I received an email explaining:

- What you told us.
- What we understood.
- What we did about it.
- What we want you to test.

The email included a link to that proposed new page and invited me to test it. I could open it, listen with my screen reader and decide whether the change actually solved my problem before anything went live.

I listened.

"Works for me."

The change went live less than ten minutes after the report.

Claude was running the process in conversation with me. The autonomous part is still to come. In the next version, we plan to use [Jev](https://docs.typesafe.ai/introduction) to help sort incoming reports, spot messages trying to give instructions rather than describe a problem, and read what each reply actually means. Ordinary code will check who sent it.

Meanwhile, the form, database, proposed page, email invitation and repair are real.

"Works for me" usually closes a bug report because the developer can't reproduce it.

I rather like giving those words to the person who had the problem.

[Works For Me: the fiction and the first real fix](https://blind-ant.com/pieces/works-for-me/fix-2/)
