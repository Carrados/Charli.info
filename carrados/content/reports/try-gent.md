---
title: "gent: tell NVDA what you want"
description: Charli-Jo has made a small, free NVDA add-on called gent, which changes NVDA's settings when you type what you want in plain words, and would love people to try it.
date: 2026-11-03
time: "19:30"
---

I've made a little [NVDA](https://www.nvaccess.org/about-nvda/) add-on called gent, and I'd love some people to try it.

Instead of going through NVDA's settings menus, you just press NVDA+G and type what you want.

For example:

* "You're talking too slowly, speed up!"
* "That's too fast, slow down a bit."
* "Stop reading punctuation."
* "Tell me what keys I'm pressing."
* "Undo that."
* "Help."

gent works out what you mean and changes the appropriate NVDA setting for you.

It can currently change speech rate, punctuation level and typing echo. It also remembers your last five changes, so you can undo them.

## What's different about this?

gent uses a small AI decision model called [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), rather than a conventional large language model such as ChatGPT or Claude.

An LLM is designed to generate answers. You ask it a question and it produces text.

Jev does something rather different. It is given a short list of possible actions and decides which one best matches what you've asked for.

It doesn't write an answer, hold a conversation or invent new settings. It simply makes a choice from the actions gent is allowed to perform.

For example, if you type "way too slow, speed it right up", Jev identifies that you want to increase the speech rate. The add-on then makes the change directly in NVDA.

If gent isn't sufficiently sure what you mean, it asks you to clarify rather than guessing.

I find this rather exciting because it suggests a different way of controlling software. Instead of remembering where a setting lives, or the exact command to change it, you just say what you want to happen.

## Does it cost anything?

No. gent is free to use.

It needs an internet connection because Jev runs online, but you don't need an account, API key or subscription. I've provided the service it uses.

The first time you use gent, it asks permission before sending your request. It sends the words you type, not the contents of your screen or documents. The service doesn't keep logs of your requests.

## How did I make it?

I'm totally blind, and I built gent this afternoon with [Claude Code](https://claude.com/claude-code).

I didn't write the Python myself. I described what I wanted, made the design decisions, and had Claude examine NVDA's actual source code, build the add-on, test it and help me install it.

Then I pressed NVDA+G, typed a request, and it worked!

It's a small experiment in what I'm calling agentic accessibility: using AI agents to build and improve accessible technology, and using specialised AI models to make software easier to control.

## Would you like to try it?

gent is very much an early experiment. I've tested it myself with NVDA, but it hasn't had extensive testing by other users.

It requires NVDA 2025.1 or later.

The add-on and its source code are available at [Carrados/nvda-addons on GitHub](https://github.com/Carrados/nvda-addons).

You can find the installation file under the [latest release](https://github.com/Carrados/nvda-addons/releases/latest).

I've also written a longer account of how it was made, called [The Making of gent](/reports/the-making-of-gent/).

I'd particularly love to know three things: Does it work for you? Is it easier than changing settings manually? And what else would you like to be able to tell NVDA to do?

Because the interesting question isn't whether gent can change three settings.

It's what happens when you can simply tell your screen reader what you want it to do.
