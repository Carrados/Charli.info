// six_story.js: the storyboard for "Always Six", as data. It is the single source of truth for BOTH the picture and
// the audio description. The scene (six.js) takes its timings from the reads below, and build_ad.mjs turns the same
// reads into a WebVTT description track and a voiced description. Change a read here and both follow.
var STORY = {
  title: "Always Six",
  logline: "Clawd wants to roll a six, throws the die as hard as it can, and gets one, because in this world every roll is code.",
  duration: 12,
  reads: [
    { id: "A", start: 0.3, end: 2.6, text: "Clawd dozes beside a big red die." },
    { id: "B", start: 2.7, end: 4.4, text: "Clawd wakes. An idea!" },
    { id: "C", start: 4.45, end: 6.0, text: "Clawd hurls it high." },
    { id: "D", start: 6.1, end: 8.0, text: "It lands. Six!" },
    { id: "E", start: 8.1, end: 9.9, text: "Clawd leaps for joy." },
    { id: "F", start: 10.0, end: 11.9, text: "Always six. It's code." }
  ],
  // the beats the scene animates to; each sits inside the read that describes it
  beats: { wake: 2.7, idea: 3.4, lift: 4.0, hold: 4.45, throw: 4.75, land: 6.4, six: 6.55, joy: 8.1, proud: 10.0, iris: 10.4 }
};
