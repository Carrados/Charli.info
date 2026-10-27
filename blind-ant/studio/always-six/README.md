# Always Six

A 12-second hand-painted cartoon, made by a blind director with Claude, with its audio description built from the same storyboard as the pictures.

Clawd dozes beside a big red die, wakes, gets an idea, hurls the die high, and it lands on six. It always lands on six, because in this world every roll is code.

- `out/video_described.mp4`: the film, with the voiced description as its audio track and the same lines as a text track
- `out/video.mp4`: the film on its own
- `out/description.vtt`: the description as WebVTT (`Kind: descriptions`)
- `out/ad_report.json`: the timing check for every description line
- `out/contact_sheet.jpg`: nine frames from the finished film

## The idea: description by construction

This is built on John Heibel's [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) (MIT), a kit for animating hand-painted cartoons in p5.js and p5.brush. Its guide asks the model to storyboard every shot as a list of timed **reads**: what the viewer must understand, and from when to when. It also forbids on-screen text, so as it stands it makes the least accessible kind of video there is.

Those timed reads are already an audio description script, written before a single frame is drawn. So here they are the single source of truth:

- `src/scenes/six_story.js` holds the storyboard as data: the reads, with their text and timings, and the beats the animation is timed to.
- `src/scenes/six.js` is the scene. It takes its timings from that file.
- `build_ad.mjs` takes the same reads and writes the WebVTT track, speaks each line, places it at its start time, and muxes the result into the video.

The picture is specified, not implied: every frame is a pure function of time, so the same code draws the same film every time. That means the description can be checked against what was built, not guessed from what was rendered.

## The check

The guide's hardest rule is timing for the viewer: one read at a time, with time for each to land. `build_ad.mjs` applies the same rule to a listener. It speaks every line, trims the silence, measures it, and fails any line that runs past the end of its moment.

On the first pass, five of the six lines overran. They were tightened until all six fit:

| read | slot (s) | speech (s) | line |
|---|---|---|---|
| A | 2.30 | 1.83 | Clawd dozes beside a big red die. |
| B | 1.70 | 1.50 | Clawd wakes. An idea! |
| C | 1.55 | 1.07 | Clawd hurls it high. |
| D | 1.90 | 1.22 | It lands. Six! |
| E | 1.80 | 1.12 | Clawd leaps for joy. |
| F | 1.90 | 1.63 | Always six. It's code. |

Every read in the storyboard is spoken, and nothing is spoken that isn't in the storyboard.

## Run it

You need Node.js, Google Chrome, ffmpeg and espeak-ng.

```
npm install
node render.mjs --frames --workers=2          # add --soft-gl with no GPU
node render.mjs --encode --out=out/video.mp4
node build_ad.mjs                              # writes out/description.vtt and out/video_described.mp4
```

Changes from the upstream kit: `studio.html` loads this scene instead of the demo and no longer pulls in a web font; `render.mjs` waits for `domcontentloaded` rather than network idle. The scene paints with flat washes only (no watercolour fills or `glow()`), so it renders on a machine without a graphics card.

## Notes

- The voice is espeak-ng, the only speech engine on the machine it was built on. Any text-to-speech engine can replace it in `build_ad.mjs`.
- Clawd is the Claude Code mascot, as drawn in the upstream kit.

A machine was involved.
