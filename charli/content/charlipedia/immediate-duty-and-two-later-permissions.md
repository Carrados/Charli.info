---
title: The immediate duty and the two later permissions
description: Under the ZIC standard, sent agents must be served now, while search indexing and model training are two separate later decisions for the publisher.
status: real
---

The [Zero Information Casualty](/charlipedia/zero-information-casualty/) standard treats machine readers by purpose, "because time, agency, and consequence are different in each case." There is one duty and two independent permissions.

- **Sent agents: serve now.** A person has asked and is waiting. Admitting them is required for conformance. Declared as ai-input=yes. See [sent agent](/charlipedia/sent-agent/).
- **Search indexers: discover later.** An index for some unknown future person. The publisher may say yes or no. Declared as search=yes or search=no.
- **Training crawlers: model later.** Content for a future model. The publisher may say yes or no. Declared as ai-train=yes or ai-train=no.

## No bundled permission

Permission for a sent agent implies neither indexing nor training. Permission to index doesn't imply permission to train, and the reverse. Each is declared and read on its own. There are no profiles, levels or medals: a site is conformant or it isn't.

## Mixed-use crawlers

Some crawlers index and train under one name. Where the operator offers a separate training control, the crawler is treated as search and training is declared through the control. Where it doesn't, the publisher must say which declaration governs it, and that statement must be true of what the crawler actually receives.

## The fourth purpose

AI summaries in search results are neither indexing nor training: "Permission to be found is not permission to be replaced." There is no standard machine-readable field for them yet, so ZIC doesn't declare them; when there is, "the three declarations of §1.7 will become four."

## Infrastructure

In September 2026 the largest edge network on the web replaced its single "block AI bots" switch with three independent controls, Search, Agent and Training: the standard's taxonomy, now enforced by a network that hadn't consulted it.

## Behind the scenes

A real idea, from [Zero Information Casualty v1.7](https://zeroinformationcasualty.org/), the design standard by Charli-Jo Tyrer and Claude, §1.7 and §1.18. This entry summarises it; the standard is the authority. charli.info, carrados.com and blind-ant.com declare yes to all three.
