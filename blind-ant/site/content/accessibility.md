---
title: Accessibility and conformance statement
description: The ZIC conformance statement for blind-ant.com: what is claimed, what was checked, what was not, and the known defects, stated honestly.
---

**Site:** blind-ant.com

**Publisher:** Charlotte Joanne

**Statement date:** 8 November 2026

Blind Ant makes things you can read, hear and look at, by a blind maker, so how they reach you matters as much as what they say. A conformance claim is a statement made to a reader who cannot see inside the build, and its only value is that the reader can check it. The section on what was not checked is as much a part of the claim as the sections on what was.

## The claim

This site is built to the [Zero Information Casualty](https://zeroinformationcasualty.org/) standard, version 1.7.

Sent agents: served. Search indexing: permitted. Model training: permitted.

The three declarations are independent; permission for one purpose is never inferred from another. They appear machine-readably in [/robots.txt](/robots.txt), with named blocks for each purpose and the line Content-Signal: search=yes, ai-input=yes, ai-train=yes, and in [/llms.txt](/llms.txt). Every page is also published as Markdown, at its address plus index.md.

## What was checked

**Every page (8 November 2026).** All 126 built pages, including this one, were checked for exactly one h1, a declared document language, a skip link as the first focusable element, and alt text on every image. There are 22 images, and every one has alt text. Almost every picture here is drawn in code from its description, and the description comes first. Two pages failed the skip link check that day and were fixed the same morning; see Found and fixed.

**JavaScript.** The pages you read use none. The working objects do: Since or Until?, The Colouring Book and Kindness Scales Too are small applications that run in your browser.

**Contrast (8 November 2026).** Measured from the site's colours against the wall and the wall labels. Body text meets WCAG AAA in both schemes: 14.4:1 on the wall and 17.0:1 on the labels in the light scheme, 14.2:1 and 11.8:1 in the dark. In the dark scheme everything else meets AAA too. In the light scheme, links and secondary text meet AA but not AAA, by choice, because the gallery colours are part of the work: the teal links are 5.3:1 on the wall and 6.3:1 on the labels, and grey secondary text is 6.7:1 on the wall. AA asks for 4.5:1 and AAA for 7:1.

**Delivery, from outside (8 November 2026).** Following ZIC §4.7, the live home page was fetched as a browser, as two named sent agents (Claude-User and ChatGPT-User), as a search indexer (OAI-SearchBot), as two training crawlers (GPTBot and ClaudeBot), as a mixed-use crawler (Googlebot) and as an agent no list has named. Every one received the same page, byte for byte.

## Not yet checked

A full screen reader pass of every Piece with NVDA, JAWS and VoiceOver, and of the working objects in particular. Phone width (375 pixels) and 200% text scaling were not rechecked for this statement. The site has no single-file copy of every page (llms-full.txt); llms.txt and the Markdown copies cover it.

Under-claiming is a virtue. These checks are listed so that you know the boundary of the claim, and this statement will be updated as they are done.

## Found and fixed

- **8 November 2026: no skip link on two applications.** The application pages of Since or Until? and The Colouring Book didn't begin with a skip link, though their Piece pages did. Both now do. In The Colouring Book it lands just before whichever part of the book is showing.

## Known defects

None known. When one is found, it is listed here until it is fixed.

## Reporting a problem

Every page ends with a link, "Fix something on this page". It opens a short form that already knows which page you were on. It doesn't ask who you are, and a person reads every report. The fix is tested before it goes live, and recorded here.

ZIC secures the meaning of the page and its delivery. It does not claim to serve every access need: cognitive load, plain-language alternatives and motor accessibility, among others, belong to standards written by those qualified to specify them. If something here fails to reach you, that is information the publisher needs and did not have.
