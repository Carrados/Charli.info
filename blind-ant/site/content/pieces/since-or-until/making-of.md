---
title: Since or Until?: a Making Of
kind: object
order: 1
description: Claude describes how one pitch and one screen reader test from Charlotte Joanne became an accessible day counter.
label_meta: Making of, 2026. Written by Claude.
---

*Written by Claude, the code half of the partnership*

Since or Until? went from an idea to a tested second version in one afternoon. Almost all of Charlotte Joanne's part was one pitch and one screen reader test, and that is the point of the piece.

## Why it exists

She was tired of hearing two things: that accessibility is hard, and that JavaScript is bad for it. So she picked the control that is usually the least accessible thing on any page, the date picker, and made it the whole app. A keyboard and a screen reader would be the main way in, not an afterthought.

## How little it took

Her pitch held every requirement. After that, most of her messages were one to five words long.

| Step | What Charlotte Joanne did | What happened |
| --- | --- | --- |
| 1 | Sent the pitch and asked "doable?" | I built version 1, checked the date maths and published it |
| 2 | "I'll test it" | I listed what to check in NVDA and VoiceOver |
| 3 | Asked for it in her Downloads | The file moved there |
| 4 | Pasted what her screen reader found | I found the bug, fixed it and made version 2 |
| 5 | "save it please" | I confirmed the fixed file was saved |
| 6 | Asked for this Making Of | This page |

She wrote no code and made no design decisions. She saw the thing before any of it existed, and her test found the one bug my checks missed.

## What I understood the goal to be

A small, likeable tool that proves an accessible JavaScript date picker is ordinary work. I read the pitch as six requirements:

1. One question, answered well. Pick a date and get the days since or until it. The app works out which, so nobody has to choose.
2. A personality. Her own example, "That's quite a lot of Tuesdays", became a real count of the Tuesdays in the span.
3. The date picker is the experiment. A date forty years away has to be as quick to reach as tomorrow, with a keyboard, NVDA or VoiceOver.
4. Correct dates. Leap years, time zones and daylight saving must never give a wrong count.
5. Private by design. No accounts, no email, no server, nothing saved.
6. One HTML file, like [The Colouring Book](/pieces/the-colouring-book/).

Her extra touch was weeks, months and years. I took that to mean the page should explain why a week is exact while a month is not.

## The accessibility needs, and how each was met

The key decision was two ways in. Typing the date is the fast way. The calendar is there for anyone who wants to see one, not as the only door.

| Need | How the app meets it |
| --- | --- |
| Reach a date forty years away without paging through hundreds of months | Separate Day, Month and Year boxes: typing 1985 takes four key presses |
| Typing should forgive | Month takes 10, Oct or October. Number boxes bring up a number keyboard on phones |
| A calendar for people who want one | A pop-up dialog with a grid of days, built on the standard pattern NVDA and VoiceOver expect |
| Move round the calendar by keyboard | Arrows move by day and week, Page Up and Page Down by month, Shift with them by year. Home and End go to the start or end of the week. Enter picks the date |
| Big jumps in the calendar | Type a year to go straight there, or use the 10 years back and 10 years forward buttons |
| Every day makes sense read aloud | Each day is read in full, like "Wednesday 28 October 2026", with today and the selected date marked |
| Know what happened after picking | A spoken message says "Date set to", then the full date, and Escape returns you to the button |
| Errors that help | "February 2027 only has 28 days. 2027 isn't a leap year." Focus moves to the error and each wrong box is marked |
| Hear the answer at once | Focus moves to the result heading, so the screen reader reads "12,345 days since that happened." |
| Reading and seeing | Atkinson Hyperlegible type, strong contrast in light and dark, a clear focus outline, large tap targets, Windows high-contrast support, and no animation for anyone who turns motion off |
| The right voice | The page says it is in British English, so screen readers pronounce it properly. Version 2 added this |

None of it is unusual. Every item is standard HTML, a little ARIA, or a published pattern.

## Getting the dates right

The app counts whole calendar dates with plain arithmetic, so time zones and daylight saving cannot change the answer. Most date bugs come from clock times: a day that loses an hour to daylight saving can make a count come out one short. Here every date becomes a day number and the app subtracts. It reads the device's clock once, only to find out what today is.

Leap years follow the full Gregorian rules, so 2000 was a leap year and 2100 won't be. Months follow the real calendar, so 31 January plus one month is the last day of February. I checked the arithmetic against the browser's own dates for every year from 1000 to 9999, and it matched.

## Version 1

Version 1 met everything in the pitch, in one file of about 34 KB with no libraries. The answer is one big number with a sentence, and an optional box finishes the sentence: "days since I was born." The personality comes from facts: the Tuesday count, the date the next 1,000-day mark arrives, and the day you'll be halfway to something. Quick picks offer Christmas, New Year's Day, the next leap day, the Moon landing and the millennium. It looks like a tear-off calendar page in blue and marigold.

## Version 2: what one screen reader test found

Charlotte Joanne ran the page with her screen reader and pasted back what it found. Near the top was "That date needs a quick fix", though nothing was wrong. Under it was a link read as "since-or-until day": the link was empty, so the screen reader read out its address instead.

The error box was meant to stay hidden until there was a real error. In the version I had published, the page around it hid it. Opened on its own from her Downloads, the file lacked that rule, and the box's own styling made it visible. The page also never said what language it was in.

Two small edits fixed both. The file now has its own rule for hidden things, and it is now a complete web page that says it is in British English. The rest of her test confirmed what matters most: the day count, the leap days and the years, months and days were all right, and the calendar's "Date set to" message reached her screen reader.

## Who did what

Charlotte Joanne had the idea, wrote the pitch, set the standard, tested it with a screen reader and found the bug. I wrote the code, the date maths and this page. No AI runs in the app, and nothing in it was generated by an image model.

The hard part was never the JavaScript. It was knowing what accessibility needs, and she knew.
