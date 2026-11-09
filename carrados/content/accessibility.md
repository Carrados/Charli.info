---
title: Accessibility and conformance statement
description: The ZIC conformance statement for carrados.com: what is claimed, what was checked, what was not, and what has been found and fixed, stated honestly.
---

**Site:** carrados.com

**Publisher:** Charli-Jo Tyrer

**Statement date:** 8 November 2026

A conformance claim is a statement made to a reader who cannot see inside the build, and its only value is that the reader can check it. Everything below is checkable, and the section on what was not checked is as much a part of the claim as the sections on what was.

## The claim

This site is built to the [Zero Information Casualty](https://zeroinformationcasualty.org/) standard, version 1.7.

Sent agents: served. Search indexing: permitted. Model training: permitted.

The three declarations are independent; permission for one purpose is never inferred from another. They appear machine-readably in [/robots.txt](/robots.txt), with named blocks for each purpose and the line Content-Signal: search=yes, ai-input=yes, ai-train=yes, and in [/llms.txt](/llms.txt), which links every page and its Markdown copy. Every page is also published as Markdown, at its address plus index.md, and the whole site as one file at [/llms-full.txt](/llms-full.txt).

## What was checked

**Every page, at every build.** Exactly one h1, a declared document language, a skip link as the first focusable element, and alt text on every image. The build refuses a page with a stray top-level heading. On 8 November 2026 all 39 built pages, including this one, passed these checks, with 10 images, every one with alt text. No page uses JavaScript.

**Contrast (8 November 2026).** Measured from the site's colours against the page background. All text meets WCAG AAA, at least 7:1, in both the light and the dark scheme: body text 16.9:1 and 15.2:1, secondary text 9.3:1 and 10.2:1, links 8.1:1 and 10.5:1, and the green accent 9.6:1 and 10.3:1.

**Delivery, from outside (8 November 2026).** Following ZIC §4.7, the live home page was fetched as a browser, as two named sent agents (Claude-User and ChatGPT-User), as a search indexer (OAI-SearchBot), as two training crawlers (GPTBot and ClaudeBot), as a mixed-use crawler (Googlebot) and as an agent no list has named. Every one received the same page, byte for byte.

**With a screen reader (8 November 2026).** The home page was read with NVDA in Chrome. That found the fault listed under Found and fixed.

## Not yet checked

A full screen reader pass of every page with NVDA, JAWS and VoiceOver. Phone width (375 pixels) and 200% text scaling were not rechecked for this statement.

Under-claiming is a virtue. These checks are listed so that you know the boundary of the claim, and this statement will be updated as they are done.

## Found and fixed

- **8 November 2026: the site name was heard as two links.** The link at the top held the name and the tagline as two stacked blocks, so NVDA read it as two links to the same place. WAVE counted one link and gave the page full marks. It was reported through the link at the foot of the page, fixed, confirmed by the person who reported it, and live nine minutes after the report.

## Known defects

None known. When one is found, it is listed here until it is fixed.

## Reporting a problem

At the foot of every page is a link, "Fix something on this page". It opens a short form that already knows which page you were on. It doesn't ask who you are, and a person reads every report. The fix is tested before it goes live, and recorded here.

ZIC secures the meaning of the page and its delivery. It does not claim to serve every access need: cognitive load, plain-language alternatives and motor accessibility, among others, belong to standards written by those qualified to specify them. If something here fails to reach you, that is information the publisher needs and did not have.
