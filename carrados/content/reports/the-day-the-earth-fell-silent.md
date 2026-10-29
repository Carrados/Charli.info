---
title: The Day the Earth Fell Silent
description: A blind tester pastes what VoiceOver says into an AI coding agent on her iPhone, and a live web app is fixed in minutes, with no sighted developer in between.
date: 2026-10-29
time: "10:45"
---

The title is borrowed from [John Barry](https://johnbarry.org.uk/). "The Day the Earth Fell Silent" is the eleventh track on [The Beyondness of Things](https://www.filmtracks.com/titles/beyondness.html). It's what this morning sounded like.

## Five coffees in

I was sitting with my iPhone, testing [Since or Until?](https://blind-ant.com/pieces/since-or-until/), the little date app I wrote about in [Inside Since or Until?](/reports/inside-since-or-until/). Safari in one app. Claude in the other. Coffee in my hand. About my fifth of the day.

I flicked through the page with [VoiceOver](https://www.apple.com/accessibility/), Apple's screen reader, and told Claude what I heard. Claude changed the code, published it, and told me when it was live. I reloaded and listened again.

That was the whole loop.

## The timestamps

- 09:40: I said, in one sentence, that VoiceOver was reading the word "description" before the date hint.
- 09:42: The fix was live.
- 09:48: I flicked through again and reported that the hint was now read twice.
- 09:49: The second fix was live.
- 10:00: Rather than keep guessing, Claude put up a test page with the same question built three ways.
- 10:10: I listened to all three and said "version C is perfect".
- 10:11: Version C was live.

Then came the moment that made me swear at my phone.

## The bug report was the speech

I flicked to the calendar button and VoiceOver said:

"Use a calendar. Pop up button. Form end. Dialog pop up. Double tap to activate the picker."

I didn't describe it. I didn't explain what was wrong. I copied what VoiceOver said and pasted it into Claude.

Claude knew which button it was, which line of code was causing the chatter, which part was worth keeping, and what I wanted without my saying so: less noise. One attribute came out. A minute later it was live.

I reloaded. VoiceOver said:

"Use a calendar. Button. Form end."

Oh my God.

## What fell silent

Not VoiceOver. The chatter.

There is a great deal of talk about AI and accessibility. Automated testing that promises to catch everything. How hard JavaScript is to make accessible. Tools that simulate disabled people so you don't have to ask one.

As far as I'm concerned, that's over.

This morning there was no sighted developer between me and the code. No ticket. No screenshot. No "can you describe what's on the screen". No tester translating my experience into someone else's words, losing a bit of it on the way.

The person who knows what good sounds like was directing the change and judging the result. VoiceOver's own words were the bug report. My ears were the test.

Normally a blind person's feedback arrives last, filtered and weeks late. This morning it arrived first, word for word, and the code bent to it in a minute.

## How it's built

For anyone who wants to try it: the app is plain HTML and JavaScript. It lives on [GitHub](https://github.com/Carrados/Charli.info). [Cloudflare Workers](https://workers.cloudflare.com/) publishes it whenever a change is merged. [Claude Code](https://claude.com/claude-code) made each change on a branch, opened a pull request and merged it when I said yes.

Getting that set up took a morning of untangling old GitHub accounts. Using it took a cup of coffee.

It's going to be a high-caffeine practice.

A machine was involved.
