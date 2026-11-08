---
title: Accessibility and conformance statement
description: The ZIC conformance statement for zeroinformationcasualty.org, the standard's own site: what is claimed, what was checked and what was not.
---

**Site:** zeroinformationcasualty.org

**Publisher:** Charli-Jo Tyrer

**Statement date:** 8 November 2026

The site that publishes a standard should meet it, and say exactly how far. A conformance claim is a statement made to a reader who cannot see inside the build, and its only value is that the reader can check it. The section on what was not checked is as much a part of the claim as the sections on what was.

## The claim

This site is built to the Zero Information Casualty standard it publishes, version 1.7.

Sent agents: served. Search indexing: permitted. Model training: permitted.

The three declarations are independent; permission for one purpose is never inferred from another. They appear machine-readably in [/robots.txt](/robots.txt), with named blocks for each purpose and the line Content-Signal: search=yes, ai-input=yes, ai-train=yes, and in [/llms.txt](/llms.txt), which links every page and its Markdown copy. Every page is also published as Markdown, at its address plus index.md, and the whole site as one file at [/llms-full.txt](/llms-full.txt).

## What was checked

**Every page, at every build.** Exactly one h1, a declared document language, a skip link as the first focusable element, and alt text on every image. The build refuses a page with a stray top-level heading. On 8 November 2026 every built page passed these checks. No page uses JavaScript, and the specification has no images.

**Contrast (8 November 2026).** Measured from the site's colours against the page background. All text meets WCAG AAA, at least 7:1, in both the light and the dark scheme: body text 16.9:1 and 15.2:1, secondary text 9.3:1 and 10.2:1, links 8.1:1 and 10.5:1, and the green accent 9.6:1 and 10.3:1.

**Delivery, from outside (8 November 2026).** Following §4.7 of the specification, the live home page was fetched as a browser, as two named sent agents (Claude-User and ChatGPT-User), as a search indexer (OAI-SearchBot), as two training crawlers (GPTBot and ClaudeBot), as a mixed-use crawler (Googlebot) and as an agent no list has named. Every one received the same page, byte for byte.

## Not yet checked

An end-to-end screen reader pass of the specification with NVDA, JAWS or VoiceOver. Phone width (375 pixels) and 200% text scaling were not rechecked for this statement. The Word renderings in Downloads were not checked for this statement.

Under-claiming is a virtue. These checks are listed so that you know the boundary of the claim, and this statement will be updated as they are done.

## Known defects

None known. When one is found, it is listed here until it is fixed.

## Reporting a problem

Every page ends with a link, "Fix something on this page". It opens a short form that already knows which page you were on. It doesn't ask who you are, and a person reads every report. The fix is tested before it goes live, and recorded here.

ZIC secures the meaning of the page and its delivery. It does not claim to serve every access need: cognitive load, plain-language alternatives and motor accessibility, among others, belong to standards written by those qualified to specify them. If something here fails to reach you, that is information the publisher needs and did not have.
