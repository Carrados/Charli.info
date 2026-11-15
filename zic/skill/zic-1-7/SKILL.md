---
name: zic-1-7
description: Build, change or audit a website to Zero Information Casualty (ZIC) v1.7, the agent-first web design standard under which no person, whether reading directly, using a screen reader or acting through an agent they sent, loses access to public meaning. Use this skill whenever someone asks for a ZIC site, a ZIC-compliant or ZIC-conformant page, a ZIC audit or conformance statement, an "agent-first" or "agent-readable" accessible website, or wants robots.txt, llms.txt or Content Signals set up so that sent agents are served and search and training are declared separately, even if they do not say "ZIC".
license: CC BY-SA 4.0
---

# Zero Information Casualty v1.7

ZIC is a web design standard by Charli-Jo Tyrer and Claude (Anthropic). The specification is the single source of truth:

- Specification, version 1.7: https://zeroinformationcasualty.org/1.7/
- The same as Markdown: https://zeroinformationcasualty.org/1.7/index.md

This skill is a working brief, not a replacement. It tells you what to build and what to check, with section numbers so you can read the exact clause when a decision turns on it. The specification is about 113,000 characters; if your fetch tool reads in parts, Part Seven and the Appendix are at the end and need a second request. Where this skill and the specification disagree, the specification is right.

## The idea in one screen

An Information Casualty is an event in which relevant information fails to reach an observer in time to inform perception, action or participation. A ZIC site is built so that this does not happen to anyone: a sighted reader, a screen reader user, a keyboard user, or a person waiting while an agent they sent fetches the page.

Two principles carry everything else:

1. **No information may be locked behind a single sense** (§1.11). Colour, image, typography, position and whitespace may reinforce meaning. None may be the only place it lives.
2. **Every reader reaches the same informational and orientational position, by a mechanism suited to their channel** (§1.16). Headings for the eye, landmarks for the screen reader, a skip link for the keyboard, an honest DOM for the agent.

Four ways a reader is lost, and the question that tests each (§1.8):

- **Rendering**: can they read it? Meaning was encoded where the observer could not decode it.
- **Admission**: is the person's reader allowed in? A person was refused because the agent they sent was refused.
- **Delivery**: did it actually arrive? The observer was welcome and the document never came.
- **Reconstruction**: did it survive being read? It was read, silently misunderstood, and reported with confidence.

ZIC does not govern typeface, palette, imagery, layout, brand, taste, register, hosting or framework (§1.12, §2.3). A conformant site may look like anything. Do not impose a visual style in ZIC's name.

## Three machine readers, three separate decisions (§1.7, §3.6)

- **Sent agents** (a person asked, and is waiting): must be served. `ai-input=yes` is mandatory. This is not the publisher's choice.
- **Search indexing**: the publisher decides, yes or no.
- **Model training**: the publisher decides, yes or no, independently.

Never infer one from another, and never bundle them. Before you write robots.txt or llms.txt, ask the publisher for their search and training decisions if they have not said. Do not choose for them.

## How to work

### Building or changing a site

1. Read `references/requirements.md`. It is the checkable list for HTML, CSS, metadata, content, delivery and the agent surface.
2. Build the pages as static HTML with honest structure. JavaScript may enhance; it may not deliver content (§2.2, §3.5).
3. Create the agent surface from the templates in `assets/`: `robots.txt`, `llms.txt`, and where the site can produce them, Markdown mirrors and `llms-full.txt`. Generate these at build time from the same source as the HTML. A hand-maintained copy drifts, which is why the specification forbids it (§3.6).
4. Run the checks in `references/checks.md` that you are able to run, and keep a note of each result.
5. Write the conformance statement from `assets/conformance-statement.md`.

### Auditing an existing site

1. Fetch the live site from outside, as a plain client, before reading its files. A site that cannot be fetched fails first on delivery, whatever its markup says.
2. Work through `references/checks.md` in order, then `references/requirements.md` for anything the checks did not cover.
3. Report each finding with the page, the element, the section of the specification, and the fix. Say plainly which checks you could not run.

## Claiming conformance: the part agents get wrong

A conformance claim is a statement to a reader who cannot see inside the build. Its only value is that it can be checked (Part Seven). So:

- **Name the version and link it.** "ZIC-compliant" without a version is not a claim.
- **State what was checked and what was not.** Under-claiming is a virtue. Over-claiming is a defect of the same kind as a missing alt attribute.
- **Do not claim conformance from the repository alone.** The files can be perfect and unreachable. Claim only after the delivery checks (§4.7) pass against the live address, fetched from outside.
- **Do not report a check you did not perform.** If you cannot run a screen reader, cannot fetch as another user agent, or cannot reach the live site, list it under "Not yet checked" and tell the person what to run.
- **Declaration is not compliance.** robots.txt declares; the hosting stack complies. A CDN, firewall or bot-management rule can make a true declaration false without any file changing, so the statement carries a date.

If the checks are incomplete, say "built to ZIC v1.7" with the list of what was and was not checked. Reserve "conforms to" for a site whose checks have passed.

## Things that catch people out

- **Anti-agent measures** (§2.2): bot challenges, CAPTCHA walls, JavaScript gauntlets, blanket AI refusal, discriminatory rate limits and cloaking are not conformant on public content. Declining search or training is fine, provided sent agents are still served.
- **Edge defaults**: an edge or CDN control that blocks an "agent" traffic category blocks sent agents, whoever set it and even if only on pages carrying advertising. A managed robots.txt written by a host is held to the same standard as one the publisher wrote (§2.2, §3.6, Part Six).
- **Mixed-use crawlers** such as Googlebot, Bingbot and Applebot index and train under one name. Where the operator offers a separate training control (Google-Extended, Applebot-Extended), treat the base crawler as search and express the training decision through the control. Where there is no separation, the publisher chooses which declaration governs it and says so in a comment line (§3.6).
- **Certificates**: a valid certificate issued for the host's wildcard (`*.github.io`, `*.pages.dev`) instead of the site's own name locks out every client that checks the hostname. Check the name, and do not turn on the HTTP-to-HTTPS redirect until it passes (§4.7).
- **Meta descriptions** must be true, useful and unique. There is no character count (§3.3).
- **Contrast**: WCAG AA by default (4.5:1, and 3:1 for large text), rising to AAA (7:1 and 4.5:1) under `prefers-contrast: more` (§2.1, §3.2).
- **Order-dependent meaning**: when two figures are given as a pair, say which is which in words. A reader should never have to infer meaning from position alone.

## Files in this skill

- `references/requirements.md`: every checkable requirement, by section. Read before building.
- `references/checks.md`: the Part Four checks as steps, including the delivery and reconstruction checks. Read before auditing or claiming.
- `assets/robots.txt`: template with the three declarations.
- `assets/llms.txt`: template for the agent map.
- `assets/conformance-statement.md`: template in the Part Seven reference form.

## Build record

- Renders: Zero Information Casualty v1.7 (September 2026, as corrected 15 November 2026)
- Skill generated: 2026-11-15
- Checked against the specification, section by section, on 2026-11-15
- Licence: CC BY-SA 4.0, the same as the specification
