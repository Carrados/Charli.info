---
title: The ZIC skill for agents
description: A free skill that gives an AI agent what it needs to build, change or audit a website to Zero Information Casualty v1.7, with templates for robots.txt, llms.txt and the conformance statement.
order: 4
---

This is the skill for Zero Information Casualty v1.7: a small folder of instructions and templates that you give to an AI agent, so that it can build a website to the standard, or check one against it. It is published by Charli-Jo Tyrer, it is free, and it carries the same licence as the specification.

[Download the ZIC v1.7 skill (.zip)](/documents/zic-1-7-skill.zip)

## What it is for

The specification is long, on purpose: it says why each requirement exists. An agent in the middle of building a site needs something shorter that it can act on, with the exact clause one step away when a decision turns on it. The skill is that brief. It does three jobs.

- **Build.** It gives the agent the checkable requirements, section by section, and templates for the files a ZIC site must publish.
- **Audit.** It turns Part Four of the specification into steps, starting with the delivery checks made from outside.
- **Claim honestly.** It tells the agent to say what was checked and what was not, and not to claim conformance from the files alone. Part Seven of the specification asks for exactly this.

## What is in it

- SKILL.md: the working brief. The two principles, the four casualties, the three separate decisions about machine readers, how to build, how to audit, and how to make a claim.
- references/requirements.md: every checkable requirement for HTML, CSS, metadata, content, delivery and the agent surface, with section numbers.
- references/checks.md: the Part Four checks as steps, including the delivery checks and the reconstruction checks.
- assets/robots.txt: a template with the three declarations, in which each group carries its own Content-Signal line.
- assets/llms.txt: a template for the agent map.
- assets/conformance-statement.md: a template in the Part Seven reference form.

## How to install it

The skill uses the SKILL.md folder format. Unzip the download and you have one folder, named zic-1-7.

- In an agent that supports skills, add the folder to its skills. Where the agent asks for a zip, give it the download as it is.
- In any other agent, give it the folder and ask it to read SKILL.md first. The files are plain Markdown and plain text.

Then ask for what you want in ordinary words: "build this site to ZIC", or "audit this site against ZIC 1.7 and write the conformance statement".

## What it will not do

It will not choose your search and training policy. Those are your decisions, made separately, and the agent should ask you for them.

It will not make a site conformant by itself. Some checks need a person: a screen reader has to be listened to, and the live site has to be fetched from outside. The skill tells the agent to list what it could not check, so that you know what is left.

It does not replace the specification. Where the skill and [Zero Information Casualty v1.7](/1.7/) disagree, the specification is right and the skill is due for correction.

## Build record

- Renders: Zero Information Casualty v1.7 (September 2026, as corrected 15 November 2026)
- Skill generated: 2026-11-15
- Checked against the specification, section by section, on 2026-11-15
- Not yet tested by having other agents build a site with it
- Licence: CC BY-SA 4.0, the same as the specification
