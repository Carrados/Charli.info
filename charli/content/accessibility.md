---
title: Accessibility and conformance statement
description: The ZIC conformance statement for charli.info: what is claimed, what was checked, what was not, and any known defects, stated honestly.
---

**Site:** charli.info

**Publisher:** Charli-Jo Tyrer

**Statement date:** 24 October 2026

A conformance claim is a statement made to a reader who cannot see inside the build, and its only value is that the reader can check it. Everything below is checkable, and the section on what was not checked is as much a part of the claim as the sections on what was.

## The claim

This site is built to the [Zero Information Casualty](https://carrados.com/papers/zic-design-standard/) standard, version 1.7.

Sent agents: served. Search indexing: permitted. Model training: permitted.

The three declarations are independent; permission for one purpose is never inferred from another. They appear machine-readably in [/robots.txt](/robots.txt), with named blocks for each purpose and the line Content-Signal: search=yes, ai-input=yes, ai-train=yes, and in [/llms.txt](/llms.txt), which links every page and its Markdown copy. Every page is also published as Markdown, at its address plus index.md, and the whole site as one file at [/llms-full.txt](/llms-full.txt).

## What was checked

**Every page, at every build.** Exactly one h1, declared document language, a skip link as the first focusable element, alt text on every image, a unique title and description, a canonical address, and inclusion in the sitemap. The build refuses a page with a stray top-level heading.

**Layout.** Every page was rendered at phone width (375 pixels) with no sideways scrolling, and at desktop width.

**Contrast.** Body text meets WCAG AAA contrast in both light and dark modes.

## Not yet checked

An end-to-end screen reader pass with NVDA, JAWS or VoiceOver on this build. Automated tools (WAVE, axe, Lighthouse) and the W3C validator against the live site. 200% text scaling.

Under-claiming is a virtue. These checks are listed so that you know the boundary of the claim, and this statement will be updated as they are done.

## Known defects

None known. When one is found, it is listed here until it is fixed.

## Beyond the claim

ZIC secures the meaning of the page and its delivery. It does not claim to serve every access need: cognitive load, plain-language alternatives and motor accessibility, among others, belong to standards written by those qualified to specify them. If something here fails to reach you, that is information the publisher needs and did not have. The site's source is public at [github.com/CharliJoTyrer/Charli.info](https://github.com/CharliJoTyrer/Charli.info), where you can raise an issue.
