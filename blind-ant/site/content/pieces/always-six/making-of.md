---
title: The making of
kind: object
order: 2
description: How Always Six was made, with its audio description as the storyboard rather than an afterthought, and the timing check every line had to pass.
---

## Description by construction

Always Six is built on [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) by John Heibel, an open-source kit (MIT licence) for painting cartoons in code. Its guide asks the model to storyboard every shot as a list of timed **reads**: what the viewer must understand, and from when to when. It also forbids any text on screen. As it stands, then, it makes the least accessible kind of video there is: silent, wordless, and visual only.

But those timed reads are already an audio description script, written before a single frame is drawn. So in Always Six they are the single source of truth:

- **The storyboard is data.** One file holds the reads, with their words and timings, and the beats the animation is timed to.
- **The scene takes its timings from the storyboard.** Change a read, and the picture follows.
- **The description is built from the same reads.** A script writes the text track, speaks each line, places it at its start time, and mixes it into the film.

The picture is specified, not implied. Every frame is a pure function of time, so the same code draws the same film every time. That means the description can be checked against what was built, not guessed from what was rendered.

## The check

The kit's hardest rule is about timing for the viewer: one read at a time, with time for each to land. Always Six applies the same rule to a listener. The build speaks every line, trims the silence, measures it, and fails any line that runs past the end of its moment.

On the first pass, five of the six lines overran. They were tightened until all six fit.

| Read | Time available | Time spoken | Line |
|---|---|---|---|
| A | 2.30s | 1.83s | Clawd dozes beside a big red die. |
| B | 1.70s | 1.50s | Clawd wakes. An idea! |
| C | 1.55s | 1.07s | Clawd hurls it high. |
| D | 1.90s | 1.22s | It lands. Six! |
| E | 1.80s | 1.12s | Clawd leaps for joy. |
| F | 1.90s | 1.63s | Always six. It's code. |

Every read in the storyboard is spoken, and nothing is spoken that isn't in the storyboard.

## Frames from the film

<figure>
<img src="/media/always-six/contact-sheet.jpg" width="1440" height="810" alt="Nine frames from Always Six in a three-by-three grid, painted in soft flat colour on a cream wall above a pink floor, with a pale blue window. Clawd, a small orange rectangular creature with stubby legs, sleeps beside a red die, with a zzz above it. Then it smiles with a light bulb over its head, the die flies high, Clawd stares with an exclamation mark as the die lands showing six, jumps with sparkles, and stands with eyes closed, pleased. Last, the picture closes to a circle around Clawd and the die, then to black.">
<figcaption>Nine frames, left to right and top to bottom, from the first sleep to the closing iris.</figcaption>
</figure>

## The voice and the code

The voice is espeak-ng, a free text-to-speech engine. It was the only one on the machine the film was built on, and any other engine can replace it.

Clawd is the Claude Code mascot, as drawn in the original kit.

The code, the storyboard and the films are all [in the Blind Ant repository on GitHub](https://github.com/CharliJoTyrer/Blind-Ant/tree/main/studio/always-six), to read, run or remake.

[Back to the cartoon](/pieces/always-six/cartoon/).
