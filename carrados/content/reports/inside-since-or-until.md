---
title: Inside Since or Until?
description: Charli-Jo asks an AI coding agent to build an accessible date picker, and gets a day counter that knows how many Tuesdays have passed.
date: 2026-10-28
time: "21:23"
---

Another day, another accessible web application. This time, it's about dates.

Yesterday I was making a colouring book. Today I've been counting Tuesdays.

Welcome to [Since or Until?](https://blind-ant.com/pieces/since-or-until/), a little web application from [Blind Ant](https://blind-ant.com/).

The idea is simple. Pick any date, past or future, and find out how many days have passed or how many remain.

You can add an occasion, too.

How many days since I got married? How many days until Christmas? How long since people first walked on the Moon?

The application gives you the answer, along with a few things you might not have thought to ask.

For example, I entered 20 October 2000, the day I got married.

It told me that 9,504 days had passed, including 1,358 Tuesdays.

"That's quite a lot of Tuesdays," it observed.

It also told me when the 10,000-day anniversary would arrive.

I rather like that.

## Why make a date calculator?

Because date pickers can be surprisingly difficult to use with screen readers.

Most people have encountered the little calendar that pops up when a website asks for a date.

For somebody using a mouse, it's usually straightforward. But for somebody using [NVDA](https://www.nvaccess.org/) or [VoiceOver](https://www.apple.com/accessibility/vision/), a calendar can become a maze of buttons, numbers, changing months and disappearing keyboard focus.

I wanted to see what would happen if I asked an AI coding agent to make one properly accessible.

Not to audit an existing date picker. Not to write a report about one.

To make one.

I came up with the concept and asked [Claude Code](https://claude.com/product/claude-code) to build it.

## What Claude actually built

Since or Until? is a single HTML file containing the interface, styling and JavaScript.

There is no framework, no database and no AI model running behind the scenes.

The application offers two ways of choosing a date.

You can type the day, month and year into three ordinary text fields. You can enter the month as a number or a name.

Or you can open a visual calendar.

The calendar is where things become interesting.

Looking inside the code, I can see that Claude has built a proper modal dialog. When it opens, keyboard focus moves to the date. When it closes, focus returns to the button that opened it.

Each date has an accessible name, not merely a number.

Instead of hearing "20", a screen-reader user can encounter "Friday 20 October 2000".

Arrow keys move between dates. Page Up and Page Down change months. Hold Shift and those keys change years.

There are also buttons to jump ten years backwards or forwards.

That last feature matters. Imagine trying to reach a date in 1969 by navigating backwards one month at a time.

The calendar also lets you enter a year directly.

None of this is especially glamorous. But it is the difference between a calendar that looks accessible and one designed around meaningful keyboard interaction.

## When the date goes wrong

The first version had an issue.

I had entered a date and obtained a perfectly sensible result, but the interface was still showing an error message: "That date needs a quick fix." Under it was a link with no words, only an address.

It was a display problem, not a problem with counting days.

The error box was meant to stay hidden until something actually went wrong. Opened on its own from my Downloads folder, the file was missing the rule that hid it, so the box was there from the start. The page also didn't say what language it was in.

That issue prompted a correction, and this is version 2.

The underlying design includes a rather thoughtful error-handling system.

If you enter something invalid, such as 29 February in a year that isn't a leap year, the application explains what's wrong.

The relevant fields can be marked invalid, and the error summary receives keyboard focus.

This matters because an accessible form should not merely detect an error. It should help the person understand and recover from it.

## A day is a day

Another interesting discovery is how Claude handles the arithmetic.

It doesn't simply subtract two JavaScript timestamps and divide the result by the number of milliseconds in a day.

That approach can become troublesome around daylight-saving changes.

Instead, the application converts dates into whole calendar-day numbers and calculates the difference between them.

It understands leap years, including the Gregorian rule that 2000 was a leap year but 2100 won't be.

It can calculate exact days, weeks and remaining days, leap days along the way, and calendar intervals expressed in years, months and days.

It can even calculate how many Tuesdays occurred between two dates.

And it looks for milestones. If an anniversary is approaching a round number of days, it can tell you when that milestone will arrive.

That wasn't strictly necessary to test a date picker.

But it makes the application fun.

And fun is a perfectly respectable design requirement.

## What about accessibility testing?

I have been totally blind for nearly forty years. I use NVDA, and I know how frustrating badly designed interactive controls can be.

But I wouldn't claim that an application is fully accessible just because its code contains the right ARIA attributes.

The real test is whether people can use it.

Can I navigate the calendar predictably? Does focus behave correctly? Does the application explain its state? Can somebody using VoiceOver accomplish the same task?

And can they do so without unnecessary effort?

Those are the questions that matter.

Looking inside version 2, I can see deliberate support for keyboard navigation, focus management, semantic controls, error recovery and screen-reader announcements.

That is a strong starting point. It is not a substitute for testing with actual assistive technology and actual users.

## No data, no accounts, no fuss

Since or Until? does its calculations in the browser.

It doesn't need your name, email address or an account.

It doesn't need to remember your wedding anniversary or your birthday.

It calculates the answer and leaves you alone.

The date comes from your own device's clock, and the calculations happen locally.

It's a lovely example of something AI can create without the finished product needing AI at all.

## Who made it?

My name is Charli-Jo Tyrer. Friends call me Charli. I'm totally blind, and I've spent much of my working life involved with accessibility and assistive technology.

These days, I'm exploring what happens when AI agents become collaborators rather than simply tools for answering questions.

I brought the idea for Since or Until?.

Claude Code made the application.

I decided that a date picker would be an interesting accessibility challenge, then decided that simply choosing a date wasn't much fun.

So I gave the date picker a purpose.

I wanted to know how many days since or until something happened.

That decision turned an accessibility exercise into a little application that somebody might actually enjoy using.

Claude worked out the implementation: the interface, the calendar, the keyboard interactions, the date arithmetic and the presentation.

I reviewed the outcome, spotted problems and directed corrections.

And here is the interesting part.

I am not a JavaScript developer. I couldn't have written this application myself using conventional programming methods.

But I could conceive it, direct its creation and evaluate whether it did what I wanted.

That's an increasingly important form of authorship.

If somebody describes this project as "a blind person getting AI to write some code", they're missing the interesting part.

Charli didn't have to become a JavaScript programmer before they could create a web application. They needed an idea, the ability to communicate it, and the judgement to recognise whether the result worked.

The coding agent supplied the implementation.

The human supplied the purpose.

## From accessibility testing to accessible creation

Earlier today I caught part of an [AbilityNet](https://abilitynet.org.uk/) and Microsoft webinar about AI and accessibility, [How Accessibility and Digital teams are using AI](https://abilitynet.org.uk/resources/financial-sector/free-webinar-how-accessibility-and-digital-teams-are-using-ai).

The discussion included how effectively AI can identify accessibility problems and whether AI can simulate disabled users for testing.

I found myself thinking about the previous few days, during which I'd been working with Claude Code and [Codex](https://openai.com/codex/) to build websites and applications.

There is a difference between asking AI to help us perform existing accessibility tasks and asking what AI makes possible in the first place.

Since or Until? is a tiny experiment.

It won't change the world. It counts days.

But it demonstrates something I find much more interesting than a percentage of accessibility errors detected.

A blind person can imagine an interactive visual application, direct an AI agent to build it with accessibility designed in, and participate in testing and improving the result.

That is what Charli-Jo's current practice is exploring: not just how AI can assist disabled people with existing technology, but how disabled people can use AI to become creators of technology themselves.

Yesterday it was a colouring book.

Today it's a date picker.

Tomorrow? Well, that's rather the point of Since or Until?.

Every day counts.

*Charli-Jo Tyrer (Charli) works on AI, accessibility and human–AI collaboration through Carrados. Since or Until? is a Blind Ant experiment, created with Claude Code. Version 2, October 2026. [Blind Ant](https://blind-ant.com/).*
