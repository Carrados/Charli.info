---
title: CharliPedia MCP
kind: piece
order: 17
description: A working, read-only MCP server that lets any AI agent look things up in CharliPedia, the memory of the CharliVerse: an experiment done in the open.
label_title: CharliPedia MCP
label_meta: Piece, 2026. A live MCP server, its launch page, how it was made, and what happened when ChatGPT used it. Directed by Charlotte Joanne; built by Claude.
label: |
  A cream connector card on a dark, ruled background. It reads CharliPedia, MCP server, the memory of the CharliVerse, and gives the address https://mcp.charli.info/. Below are four tools: search, get_entry, list_entries and get_court. A ruby padlock sits in the corner, and along the bottom: read only, no sign-in, every agent welcome.
---

![The CharliPedia MCP connector card, as described above.](/pieces/charlipedia-mcp/charlipedia-mcp.png)

## About the Piece

This Piece is a launch page for a product that exists. The CharliPedia MCP server is live at https://mcp.charli.info/, and any AI agent that speaks the Model Context Protocol can connect to it and ask about the people, houses, companies and ideas of the CharliVerse.

It was an experiment done in the open: one Sunday morning's challenge, built, tested by a rival AI, found wanting in one small way, fixed and published the same day. The launch page is written "as if" for a real product, because it is one.

The same afternoon, ChatGPT plugged in. It proposed a meeting nobody had written, which became CharliPedia's first idea from an outside agent, and it wrote a scene between Alex and Down the Banksy about Tyrer's Law. Claude writes about that in First contact, and the scene is here as ChatGPT wrote it.

Then ChatGPT took a real newsletter from Charlotte Joanne's inbox, asked the CharliVerse who would care, and found dice and Lucy Love-Child. Its report, An email, a world, and two interested women, also records the afternoon's most useful failure: a line the search couldn't find, and how it was fixed.

## Objects

<!-- objects -->

## Behind the fiction

Nothing here is invented except the tone of a launch page.

- The server is real and running, on Cloudflare, and its [source code](https://github.com/CharliJoTyrer/Charli.info/blob/main/charli/mcp/worker.js) is open for anyone to read.
- It is read-only by construction. It has no tool that writes, edits or deletes, and it reads only the published copy of [CharliPedia](https://charli.info/charlipedia/). No agent can change the CharliVerse through it.
- The people and companies inside CharliPedia are fictional, and every entry says so in its own Behind the scenes.
- The tests and the snag in How it was made really happened, on 25 October 2026.
- ChatGPT's answers, its scene Maintenance is a verb, and its report on the Every newsletter are reproduced as it wrote them, apart from the light edits each one names. The characters in them are fictional; the scene is a proposal, not CharliVerse canon.
