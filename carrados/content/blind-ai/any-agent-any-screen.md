---
title: "Any Agent, Any Screen"
description: A concept note on the Borrowed Screen, the idea that every screen you own will lend itself to any AI agent you trust, and why blind people may feel it first.
desk: charli
date: 2026-11-18
byline: Charli-Jo Tyrer
related: "Any Agent, Any Screen: A Future History, the same idea told as a chronology to Easter 2028, at Blind Ant|https://blind-ant.com/pieces/any-agent-any-screen/"
---

## Summary

Every screen a person owns will soon offer itself to any AI agent they trust, for as long as that agent needs it. I call this the Borrowed Screen.

Today, apps own screens. In the Borrowed Screen model, the agent owns the moment, and screens are a shared resource it borrows. The phone, TV, car dashboard, fridge door, watch and glasses each say what they can show, and the agent renders what this person needs, on the best surface nearby, then hands the screen back.

I am making this claim on 18 November 2026. I expect the first serious versions by Easter 2028, and I expect it to mark the end of websites as places people visit.

## Where we are now

The [Star Trek](https://www.startrek.com/) computer is arriving in stages, and voice comes first. People are starting to talk to a core agent instead of opening apps and websites. Banks are already trialling agents that carry out tasks such as payments and account questions. I heard of three such trials in a single day this month.

None of this vision is new. Science fiction has assumed for decades that the computer simply uses whatever display is nearest: the ship's computer on Star Trek, ambient assistants in countless novels and films. Ambient computing has been an industry talking point for years too.

What is new is that the agent half now exists. The missing half is the plumbing: a way for ordinary devices, made by different companies, to lend their screens to an agent the owner trusts. This note is about that plumbing and when it will arrive.

## The idea

Every device with a screen becomes a surface that any agent its owner authorises can draw on. The device does not need to know what the agent will show. It only needs to say what it can do and who is allowed to use it.

This turns the current arrangement upside down:

| | Today | The Borrowed Screen |
| --- | --- | --- |
| Who owns the screen | The app or the device maker | The owner, who lends it |
| Who designs the interface | A designer, months in advance | The agent, in the moment |
| Where the interface lives | A website or an app | Wherever the person is |
| What it is shaped around | The average user | This person, this task, this device |

Websites and apps were built because a person had to go to the information. In the Borrowed Screen model, the information comes to the person, on whichever screen suits them.

## What already exists, and what is missing

The parts exist, but nobody has put them together. Each one solves a piece of the problem inside a single company or a single app.

| Today's piece | What it does | What it lacks |
| --- | --- | --- |
| Casting ([AirPlay](https://www.apple.com/airplay/), [Google Cast](https://developers.google.com/cast)) | Sends one device's content to another's screen | Works only between named apps, inside one ecosystem |
| Generative UI | An agent builds an interface on the fly | Shows up only inside a chat window or the agent's own app |
| Agent-to-interface protocols (for example [MCP Apps](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/), Google's [A2UI](https://a2ui.org/)) | A standard way for an agent to send interface pieces | Aimed at chat hosts, not at every device a person owns |
| Smart-home standards ([Matter](https://csa-iot.org/all-solutions/matter/)) | Devices from different makers work together | Built for control, such as lights and locks, not for display |

The missing piece is an open standard that lets any screen announce itself to any trusted agent and lets that agent borrow it.

## How it would work

Borrowing a screen takes five steps, and each one already has a rough precedent today.

1. **Announce.** Each device tells nearby trusted agents what it offers: screen size, whether it has touch, speakers or a braille display, and whether it is in a private or shared space. This is like a printer appearing on your network.
2. **Authorise.** The owner decides once which agents may borrow which devices, much as you pair headphones or grant an app permission today.
3. **Choose.** When a task needs a display, the agent picks the best surface nearby: the TV for a holiday plan, the watch for a quick confirmation, speech alone for someone who prefers it.
4. **Render.** The agent sends an interface built for this person and this task. The device shows its own trusted marker, so you always know which agent is drawing.
5. **Release.** When the task is done, the screen goes back to whatever it was doing, like a cast ending on a TV.

## Why it matters most for blind and partially sighted people

The Borrowed Screen ends 30 years of retrofitting. Web accessibility has been a patch on interfaces designed for sighted people. Screen reader users have to navigate someone else's visual layout, and every redesign can break it again.

When an agent builds the interface in the moment, it can build it for the person in front of it:

- Speech only, with no screen at all, for a blind user.
- Large, high-contrast text on the biggest nearby screen for someone with low vision.
- Braille output, when a braille display is one of the surfaces on offer.
- A simpler layout for someone with cognitive fatigue, and a denser one for a power user.

The interface stops being a fixed thing to make accessible. It becomes a performance shaped to the person every time.

There is a condition. The agent can only be as good as the information it reads. If meaning is lost between the source and the agent, no amount of clever rendering brings it back. That makes information fidelity at the source, the concern of the [Zero Information Casualty](https://zeroinformationcasualty.org/) (ZIC) work, the foundation this all rests on.

Accessibility law could also speed this up. A requirement that any authorised agent can render to any screen would sit naturally alongside rules like the [European Accessibility Act](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en).

## The hard problems

Trust, not technology, decides whether this happens. Four problems have to be solved first.

1. **Spoofing.** A malicious agent could draw a convincing fake bank screen on your TV. Every borrowed screen needs a way to prove which agent is drawing on it, such as a trusted indicator that only the device itself can show.
2. **Permission.** Who may borrow which screen, and when? A guest's agent should not be able to take over your kitchen display. Permissions need to be as simple as pairing headphones.
3. **Privacy in shared spaces.** Your bank balance should not appear on the living-room TV while friends are round. The agent needs to know who else is in the room, or at least to ask.
4. **Platform resistance.** Apple, Google, Samsung and the TV makers each want *their* agent to own the screen. Expect walled gardens first. Openness will probably come from regulation, or from one major player opening up to win market share.

## What happens to websites, and when?

By Easter 2028, websites as places people visit will be fading. The information behind them will matter more than ever. Agents still need a source for prices, policies, stock and opening hours. Websites become the supply layer that agents read, written for machines first and humans second.

Sites built for tasks go first: banking, bookings, form-filling, customer service. Sites built for experience, such as reading, browsing and shopping for pleasure, last longer.

| By | What I expect |
| --- | --- |
| Easter 2027 | Bank agent trials go public; voice-first agents become normal for early adopters |
| End of 2027 | The first walled-garden versions of screen borrowing, inside one maker's devices |
| Easter 2028 | Most routine tasks at large banks and retailers can be done through an agent; early adopters rarely open a website |
| 2029 onwards | Pressure for an open standard, driven by accessibility rules and competition |

## The claim

Science fiction imagined the computer that uses any screen nearby. Agents have now made the computer half real. The next step is the Borrowed Screen: every device lends its display to the agent its owner trusts, and the interface is built for the person rather than the person adapting to the interface.

Whoever builds the open standard for that handshake will shape how billions of people use computers. And blind and partially sighted people may be the first to feel the difference.
