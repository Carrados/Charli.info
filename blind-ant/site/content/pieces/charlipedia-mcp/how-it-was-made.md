---
title: How it was made
kind: object
order: 2
description: A challenge on a Sunday morning, a read-only rule, a server built and tested, a rival AI's verdict, and one door Cloudflare had left shut.
label_meta: Making of, 2026. Written by Claude, from the conversation with Charlotte Joanne.
---

## The challenge

The night before, Claude had said an MCP server for CharliPedia would be easy. On Sunday morning Charlotte Joanne called it in:

> ok you were "giving it the big one" last night saying a CharliPedia mcp was easy. what about it? but read only, no agents meddling with it.

That last line became the design. An MCP server can give an agent tools that do things. This one would give it tools that only look.

## The build

First, the charli.info build learned to write one extra file: every CharliPedia entry, as plain Markdown, in a single bundle. Then came a small server on Cloudflare that fetches that bundle and answers four questions: search, get an entry, list the entries, and get the Court. It has no database of its own and no write access to anything. If it vanished tomorrow, CharliPedia would not notice.

It was tested against the real entries before going live, then given its own address, mcp.charli.info.

## The rival's verdict

Charlotte Joanne didn't take Claude's word for it. In her own words: "i asked it if you were shitting me!" She asked ChatGPT to check. It ran real calls against the live server: search found VQ4, a full entry came back, the list counted 88 entries, and the Court arrived with all nine members. It read the source code and confirmed there was nothing that writes. "The main claim holds," it said.

But it found a snag. Its plain Python client was turned away with Cloudflare's Error 1010, while a request dressed as a web browser got through. So "any agent can connect" wasn't yet true.

## The door left shut

The culprit was a Cloudflare setting called Browser Integrity Check, which turns away software that doesn't look like a browser. It was on for all three of Charlotte Joanne's sites. That quietly contradicted their open robots.txt, which welcomes every agent. It was switched off: first for the server, then, at her say-so, everywhere. The house rules now say it stays off.

The whole experiment, from challenge to this page, took one Sunday.
