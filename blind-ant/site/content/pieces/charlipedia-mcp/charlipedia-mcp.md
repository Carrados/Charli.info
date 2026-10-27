---
title: CharliPedia MCP
kind: object
order: 1
description: The launch page for the CharliPedia MCP server: what it does, how to connect, and what it will never do.
label_title: CharliPedia MCP
label_meta: Launch page, 2026. Directed by Charlotte Joanne; server and page by Claude.
---

**The CharliVerse, on tap for your agent.** CharliPedia is the memory of the CharliVerse: its people, fashion houses, companies, technologies and ideas, written from inside the world. Now your AI can read it too. Ask who someone is, what a house stands for, or what the Court would make of your idea, and get answers drawn from the canon, with a link to every source.

## The address

https://mcp.charli.info/

That is all you need. It's a remote MCP server over Streamable HTTP. There's no account, no key and no sign-in.

## Connecting

- **Claude:** add a custom connector and paste the address.
- **ChatGPT:** with Developer mode on, add an app with the address https://mcp.charli.info/mcp and choose no authentication.
- **Claude Code:** `claude mcp add --transport http charlipedia https://mcp.charli.info/`
- **Anything else:** any app or agent that takes a remote MCP server can use the same address.

## Five tools

- **search** finds entries by the words in them, with a snippet and a link for each.
- **get_entry** fetches one entry in full, by name, such as "Big Charli" or "First Layer".
- **list_entries** lists everything, or just one letter, or just one status: canon, idea or stub.
- **semantic_search** searches by meaning, not just words, across CharliPedia, Blind Ant, Carrados, charli.info and the Training courses there, and says which site every passage comes from, so fiction and fact never blur. Ask it a theme or a question, such as "who has been let down by a beautiful interface?", or keep it to the Training courses for practical how-to questions
- **get_court** fetches the CharliVerse Court and all nine of its women, so your agent can hold a deliberation in their voices.

## Things to ask

- "Search CharliPedia for robot dogs."
- "Search the CharliVerse by meaning for people who made something hidden perceptible."
- "Who is Big Charli, and what is she for?"
- "List the canon entries."
- "Get the Court, then let them argue about whether I should launch my product next week."

## What it will never do

It reads. That's all. There is no tool that writes, edits or deletes, not even a hidden one. CharliPedia changes only when its next edition is published, and the server picks that up within five minutes.

It is also a source of continuity, not an authority. Your agent is told, when it connects, that anything it makes up is an idea, not canon. The Court's deliberation is your agent's performance, built from their entries, not theirs.

## The small print

Everything in CharliPedia is CC BY-SA 4.0. Cite entries by their address. Every agent is welcome, including training crawlers.
