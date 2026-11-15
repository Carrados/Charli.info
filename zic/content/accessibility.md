---
title: Accessibility and conformance statement
description: The ZIC conformance statement for zeroinformationcasualty.org, the standard's own site: what is claimed, what was checked and what was not.
---

**Site:** zeroinformationcasualty.org

**Publisher:** Charli-Jo Tyrer

**Statement date:** 15 November 2026

The site that publishes a standard should meet it, and say exactly how far. A conformance claim is a statement made to a reader who cannot see inside the build, and its only value is that the reader can check it. The section on what was not checked is as much a part of the claim as the sections on what was.

## The claim

This site is built to the Zero Information Casualty standard it publishes, version 1.7.

Specification: [Zero Information Casualty v1.7](/1.7/)

Sent agents: served. Search indexing: permitted. Model training: permitted.

The three declarations are independent; permission for one purpose is never inferred from another. They appear machine-readably in [/robots.txt](/robots.txt), with named blocks for each purpose and the line Content-Signal: search=yes, ai-input=yes, ai-train=yes, and in [/llms.txt](/llms.txt), which links every page and its Markdown copy. Every page is also published as Markdown, at its address plus index.md, and the whole site as one file at [/llms-full.txt](/llms-full.txt).

## What was checked

**Every page, at every build.** Exactly one h1, a declared document language, a skip link as the first focusable element, and alt text on every image. The build refuses a page with a stray top-level heading. On 8 November 2026 every built page passed these checks. No page uses JavaScript, and the specification has no images.

**Contrast (8 November 2026).** Measured from the site's colours against the page background. All text meets WCAG AAA, at least 7:1, in both schemes. In the light scheme: body text 16.9:1, secondary text 9.3:1, links 8.1:1 and the green accent 9.6:1. In the dark scheme: body text 15.2:1, secondary text 10.2:1, links 10.5:1 and the green accent 10.3:1.

**Delivery, from outside (8 November 2026).** Following §4.7 of the specification, the live home page was fetched as a browser, as two named sent agents (Claude-User and ChatGPT-User), as a search indexer (OAI-SearchBot), as two training crawlers (GPTBot and ClaudeBot), as a mixed-use crawler (Googlebot) and as an agent no list has named. Every one received the same page, byte for byte.

**Screen readers.** The publisher uses NVDA and VoiceOver, and this site has been listened to with both.

**Phone width and text size (15 November 2026).** Each of the three pages was loaded at 375 pixels wide, and again at that width with the text size doubled. No page scrolled sideways and no text was cut off. The code examples scroll sideways inside their own boxes. This was an emulated phone in a desktop browser, with the root text size doubled, not a phone in the hand.

**Reconstruction (15 November 2026; reader: Claude, Anthropic).** Following §4.8 of the specification, Claude fetched each live page, summarised it, said what it had to guess and rebuilt the structure, and each account was compared with the page. The headings, lists and code examples were rebuilt correctly on all three pages, which have no tables or figures. One defect was found, on this page: the contrast figures were given in pairs, and only their order said which was light and which was dark, so the reader gave both body-text figures to the light scheme. The sentence now names the scheme for each figure. The reader flagged two things it could not determine: on ZIC for Publishers, how the study's 2,484 sessions divide into the 240 behind each result; and in Part Seven, whether the example.org address in the reference form is a real citation (it is a placeholder). In one summary the reader said version 1.7 adds the fourth Content Signals field, where the specification says Content Signals gained it; no element on the page permits that reading.

One fact about the reader is recorded here, as §4.8 asks. It read the specification 100,000 characters at a time, and the page is about 113,000. Part Seven, the Appendix and Downloads arrived only on a second request.

**Word renderings (15 November 2026).** The three specification files and the Publishers file in Downloads were checked for a title, real heading styles with no skipped levels and a declared language. None has a table or a picture. Four things were corrected. The v1.7 file had no title, and its Preamble heading was missing, its text run into the paragraph before. The v1.5 and v1.6 files had a stray backslash before the title. All three declared US English and now declare British English. The author's name now reads Charli-Jo Tyrer, as on this site.

## Not yet checked

JAWS. The Word renderings have not been listened to with a screen reader. High contrast (prefers-contrast: more) and reduced motion were not checked for this statement.

Under-claiming is a virtue. These checks are listed so that you know the boundary of the claim, and this statement will be updated as they are done.

## Known defects

None known. When one is found, it is listed here until it is fixed.

Fixed on 15 November 2026: the contrast sentence on this page, found by the reconstruction check above.

## Reporting a problem

At the foot of every page is a link, "Fix something on this page". It opens a short form that already knows which page you were on. It doesn't ask who you are, and a person reads every report. The fix is tested before it goes live, and recorded here.

ZIC secures the meaning of the page and its delivery. It does not claim to serve every access need: cognitive load, plain-language alternatives and motor accessibility, among others, belong to standards written by those qualified to specify them. If something here fails to reach you, that is information the publisher needs and did not have.
