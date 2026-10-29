---
title: ZIC for Publishers: What Happens When the Agent Arrives
description: A guide to Zero Information Casualty v1.7 for publishers and SEO, GEO and AEO teams, covering the four ways an agent loses your page, why robots.txt is not proof, the Cloudflare category switches, meta descriptions that work as answers, and the checks you can run from outside.
order: 3
---
SEO gets you found. GEO gets you cited. ZIC is what happens when the agent arrives.

This guide is for people who own or advise on a web presence: SEO, GEO and AEO specialists, marketers, communications teams and publishers. It renders the [Zero Information Casualty (ZIC) v1.7 specification](/) for that reader. It is not the specification. Where the two disagree, the specification is right.

## The failure your dashboard cannot show you

Every tool in the visibility stack begins by loading your page. Validators, audits, Lighthouse, schema checkers and screen reader tests all start from a document they already hold. A tool that has your document cannot tell you your document is unreachable. That is not a bug anyone can patch. It follows from where the tool is standing (§1.8).

So the most expensive failures never appear in your analytics. A person asks an agent about you. The agent cannot get in, or gets in and misreads what it finds. No visit is logged, because no visit happened. Not being cited looks exactly like not being good enough.

The whole market is testing from inside the house. ZIC's checks are run from outside, as the agent (§4.7).

## Three machine visitors, three separate decisions

Machines arrive at your site for three different reasons, and ZIC keeps them apart because time, agency and consequence differ in each (§1.7).

- **Sent agents** are acting for a person who asked a question just now and is waiting for the answer. ZIC requires that they are served. The machine-readable declaration is ai-input=yes.
- **Search indexers** are building an index so that someone may find you later. Allowing or declining them is your decision.
- **Training crawlers** are gathering material for a future model. Allowing or declining them is also your decision, and it is a separate one.

Permission for one never implies permission for another. Declining training does not decline search, and neither touches the sent agent (§1.7).

The trouble is that for years the controls bundled all three. A wildcard Disallow written in 2023 to keep out training crawlers also caught every reader anybody has sent since. You did not decide to block the person's agent. You inherited it from a line somebody wrote before that agent existed.

### The edge has its own switches now

On 15 September 2026 Cloudflare replaced its single "block AI bots" switch with three independent categories, Search, Agent and Training, enforced at the edge (changelog, v1.7). The categories match ZIC's three classes. Two consequences matter to a publisher.

- **The Agent category is the sent agent.** Cloudflare's recommended default blocks it on pages that carry advertising, on the reasoning that an advertisement marks a page a person was meant to see. The person who sent the agent has landed on that page. ZIC treats this default as an anti-agent measure, and a conformant site must set Agent to allowed on every public page (§2.2, Part Six).
- **Mixed-use crawlers can be refused by accident.** Googlebot, Bingbot and Applebot index and train under one name. Behind an edge that judges a crawler by all of its behaviours, blocking training can quietly refuse your search crawler too. Where the operator offers a separate training control, such as Google-Extended, use that control and leave the base crawler alone (§3.6).

These controls are dated and will move. Part Six of the specification describes them as they stood in September 2026 and says which switch serves which requirement.

## Four ways the reader is lost

The specification names four classes of Information Casualty (§1.8). An Information Casualty is an event in which relevant information fails to reach an observer in time to inform perception, action or participation. This guide takes them in the order a machine reader meets them, which is not the order in which the specification introduces them.

### 1. Delivery: did it arrive?

The document existed, the reader was welcome, and it never arrived. Every check that runs against a document you already hold will pass a page nobody can fetch.

The first ZIC site, charli.info, spent several days in exactly this state. It had immaculate semantic HTML, high contrast, and a robots.txt welcoming named agents. It was served over HTTPS with a certificate issued for `*.github.io`, a domain it does not own. The certificate was valid. It was trusted. It was for somebody else. Every agent that checked the hostname failed the handshake, could not read robots.txt, failed closed, and reported that the site disallowed automated access. The site was perfect and unreachable, and the only check that found it was a person asking a live AI assistant to fetch it (§1.8, §4.7).

### 2. Admission: is the person's reader allowed in?

The page could have been read, but the agent was refused, challenged, slowed, degraded or misled. To the person waiting, the technical category of the obstruction is irrelevant: the reader they sent reached the door and was turned away. The casualty is the person. The agent is only the vehicle (§1.9).

This includes bot-detection challenges, CAPTCHA walls, JavaScript gauntlets, WAF rules and discriminatory rate limits (§2.2). It increasingly includes browser-driving agents, which arrive with an ordinary browser's user agent and are refused by behavioural heuristics rather than by anything in robots.txt (§3.6).

### 3. Rendering: can it be decoded?

The page arrived and was admitted, but the meaning was kept somewhere a machine cannot read: a status shown only in colour, a heading that is only large, an informative image with no description, content that appears only after JavaScript runs. The rule underneath fits in one sentence: no information may be locked behind a single sense (§1.11).

### 4. Reconstruction: did it survive being read?

The page arrived, was admitted and could be decoded, and the machine reader reconstructed it wrongly, silently, and reported the result with confidence (§1.8). A table whose header row is a header only to the eye, a caption three elements away from its figure, a hierarchy implied by spacing: the agent does not backtrack. It guesses, and produces a fluent answer.

This is a separate class, and for a publisher it may be the costliest, because it never looks like an error. You are not being ignored. You are being misquoted, at scale, with confidence. Rendering failures withhold meaning; reconstruction failures replace it.

## Declaration is not compliance

robots.txt is where you declare. Your stack is where you comply (§3.6). Three facts make the difference practical rather than pedantic.

- robots.txt is advisory. A CDN rule, WAF policy or bot-management heuristic can override it silently, and the file will not mention that it lost.
- The vendors of user-directed agents do not agree on whether robots.txt governs them. Anthropic states that Claude-User honours it; OpenAI and Perplexity state that it may not, or does not, apply to fetches made at a person's direct request.
- Edges now enforce by category, not by name. "Verified" no longer means allowed. A declaration that was true in July can become false in September without a byte of your files changing.

Hosts and edges also offer to write the file for you. Cloudflare's managed robots.txt, as of September 2026, declares search and training preferences and says nothing about ai-input. ZIC treats that silence as non-compliant. Write your own file, or amend the managed line, and then verify from outside that the edge agrees with it (§3.6, Part Six).

The specification's normative robots.txt blocks, with the current agent names, are in §3.6. That is the version to copy: the names change, and the specification reviews them at least twice a year.

## The description is the answer

There is one requirement in ZIC that GEO people already think they understand, and most of them have it backwards.

The specification requires every page to carry a meta description, and it sets exactly one test for it: it must be a true and useful summary of the page, unique across the site (§3.3). It sets no character count. The old 150 to 160 character range was a fact about how one search engine truncated its results, not a property of a well-formed document, so it was removed. Page titles, descriptions, Open Graph tags and structured data are not decoration. They are the site's interface with the machines that read it (§2.1).

A summary is not a tagline. "Prompting AI tools is a new form of management science" is a thesis, and a good one. It is not a summary of an article that teaches five principles with worked examples, so under §3.3 it fails.

There is now some evidence of what that failure costs. In October 2026 Mike Taylor, head of evals at Every, simulated 2,484 agent sessions across Anthropic and OpenAI models, as reported in [How to Get AI Agents to Recommend Your Articles](https://every.to/also-true-for-humans/how-to-get-ai-agents-to-recommend-your-articles). In each one, an agent saw a question, a handful of search results, and an instruction to cite the two most useful.

- One of his guides, under its original curiosity-style headline and subtitle, was cited in 2 sessions out of 240.
- With only the headline and subtitle rewritten to say plainly what the article teaches, the same article was cited in 240 out of 240.

Those were simulations, not live traffic. Taylor says so himself, and he has not yet tested whether the effect carries through to real agent visits. Verify these figures yourself before you repeat them. That instruction is not a disclaimer. It is the standard's register: check it, from outside, or do not claim it.

ZIC does not tell you how to win citations. What a site says, and whether it is any good, is not its business (§1.12). It requires only that the description be true. The reading that matters to you is narrower and more useful: write the description as the answer, because that is what §3.3 already demands, and on this early evidence the agents prefer it anyway.

## What ZIC asks of you first

This section foregrounds the part of the standard that concerns a publisher first. It is not the whole conformance bar.

Serve the reader a person sent: admit user-directed agents to every public page, with no agent-specific challenge, delay or degradation (§1.6, §2.2). Decline training if you wish. Decline search if you must. Those are yours, and ZIC does not choose for you; it requires only that each is declared separately and truthfully, in robots.txt and in Content Signals (§1.7, §3.3, §3.6).

The rest of the bar includes honest semantic structure, static HTML delivery, structural metadata (titles, descriptions, Open Graph, Schema.org, canonical URLs, a sitemap and, where you publish serially, a feed), a /llms.txt file generated at build time rather than maintained by hand, and the validation checks of Part Four (§2.1, §3.1 to §3.6, Part Four). A minority of the requirements, such as visible focus indicators, contrast that rises on request and respect for reduced motion, exist for human sensory access rather than for agents, and §1.13 explains which and why.

ZIC does not govern your typeface, palette, imagery, layout or brand (§1.12, §2.3). A conformant site may look like anything at all.

## Checks you can run this afternoon

The normative procedure is §4.7. In outline, from a machine that does not already trust your site:

1. Fetch your canonical HTTPS address with a plain client, with no JavaScript, cookies or session. The full content must be in the response.
2. Check that the certificate is issued for your hostname, not merely by a trusted authority.
3. Fetch your pages as a browser and as at least one named user-directed agent. The responses must match.
4. Fetch as a search indexer and a training crawler, and confirm each gets what you declared for its class.
5. Fetch as an agent nobody has named. The public content must still be served.
6. Fetch as a mixed-use crawler such as Googlebot, and, if you are behind an edge that classifies by purpose, fetch a page that carries advertising as a sent agent.
7. Ask a live AI assistant to fetch and summarise a page by URL, then ask it what it could not determine (§4.7, §4.8).

As an illustration only, dated October 2026, step 3 can be as simple as two requests compared side by side:

```text
curl -sS https://example.com/ -o browser.html
curl -sS -A "Claude-User" https://example.com/ -o agent.html
```

Your logs will tell you more: look for agent user agents receiving 403s, challenge pages or empty bodies.

Passing these checks shows that the door was open to the readers you tried, on the day you tried them. It does not prove it stays open, which is why the specification asks you to repeat them (§4.7).

## No badges

There is nothing to buy and nothing to be silver at. Conformance is binary: a site passes or it does not (§1.7, Part Four). A conformance claim names the version, links the specification, states the search and training declarations separately, and says what was checked and when (Part Seven). A badge is a claim a reader cannot check, and this standard declines to manufacture those. For a publisher that is a feature: competitors cannot purchase the appearance of it.

You did not choose this. But it is yours now, and it is running.

## This document in other renderings

This page is the canonical publication of ZIC for Publishers. It is also available as a Word file: [Download ZIC for Publishers as a Word document (.docx)](/documents/ZIC_for_Publishers_v1_7.docx). The specification it renders is [Zero Information Casualty v1.7](/).

## Build record

- This document renders: Zero Information Casualty v1.7 (September 2026)
- Explainer edition: Publisher, generation 2
- Generated: 2026-10-29
- Fidelity audit: passed against v1.7 (2026-10-29); every requirement claim traces to a spec section
- Statistics verified: Mike Taylor, Every, How to Get AI Agents to Recommend Your Articles (27 October 2026), checked against the source on 2026-10-29; no revision found
- Licence: CC BY-SA 4.0, same as the specification

The specification is the single source of truth. Where this document and the specification disagree, the specification is right and this document is due for regeneration.
