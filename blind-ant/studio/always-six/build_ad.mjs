// build_ad.mjs: audio description by construction.
// Reads the storyboard (src/scenes/six_story.js), the same data the picture is timed from, and builds:
//   out/description.vtt         a WebVTT description track (one cue per read)
//   out/ad.wav                  each read spoken and placed at its start time
//   out/video_described.mp4     the video with the voiced description and the text track muxed in
// It also checks that every read is spoken and that each line fits inside its read's time slot.
// Usage: node build_ad.mjs [--video=out/video.mp4] [--voice=en-gb] [--wpm=185]
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { execFileSync } from 'child_process';
import vm from 'vm';

const args = Object.fromEntries(process.argv.slice(2).map(a => a.replace(/^--/, '').split('=')));
const VIDEO = args.video || 'out/video.mp4', VOICE = args.voice || 'en-gb', WPM = args.wpm || '185';
const src = readFileSync('src/scenes/six_story.js', 'utf8');
const STORY = vm.runInNewContext(src + ';STORY');   // run the storyboard file as-is: no second copy of the data

mkdirSync('out/ad', { recursive: true });
const ts = s => { const ms = Math.round(s * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, ss = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(ss).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`; };
const dur = f => +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString().trim();

let vtt = `WEBVTT\nKind: descriptions\n\nNOTE ${STORY.title}: description generated from the storyboard reads\n\n`;
const report = [];
for (const r of STORY.reads) {
  vtt += `${r.id}\n${ts(r.start)} --> ${ts(r.end)}\n${r.text}\n\n`;
  const wav = `out/ad/${r.id}.wav`;
  execFileSync('espeak-ng', ['-v', VOICE, '-s', String(WPM), '-w', `out/ad/${r.id}_raw.wav`, r.text]);
  // trim the synthesiser's leading and trailing silence, so what's measured is the speech itself
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', `out/ad/${r.id}_raw.wav`, '-af', 'silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse', wav]);
  const d = dur(wav), slot = r.end - r.start;
  report.push({ id: r.id, start: r.start, slot: +slot.toFixed(2), speech: +d.toFixed(2), fits: d <= slot, text: r.text });
}
writeFileSync('out/description.vtt', vtt);

// place each line at its read's start and mix
const inputs = STORY.reads.flatMap(r => ['-i', `out/ad/${r.id}.wav`]);
const delays = STORY.reads.map((r, i) => `[${i}]adelay=${Math.round(r.start * 1000)}|${Math.round(r.start * 1000)}[a${i}]`).join(';');
const mix = STORY.reads.map((_, i) => `[a${i}]`).join('') + `amix=inputs=${STORY.reads.length}:normalize=0,apad,atrim=0:${STORY.duration}[out]`;
execFileSync('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex', `${delays};${mix}`, '-map', '[out]', '-ar', '44100', 'out/ad.wav']);

execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', VIDEO, '-i', 'out/ad.wav', '-i', 'out/description.vtt',
  '-map', '0:v', '-map', '1:a', '-map', '2:s', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-c:s', 'mov_text',
  '-metadata:s:a:0', 'title=Audio description', '-metadata:s:a:0', 'language=eng',
  '-metadata:s:s:0', 'title=Description (text)', '-metadata:s:s:0', 'language=eng',
  '-shortest', 'out/video_described.mp4']);

console.log('read  start  slot  speech  fits  text');
for (const r of report) console.log(`${r.id.padEnd(5)} ${r.start.toFixed(2).padStart(5)} ${r.slot.toFixed(2).padStart(5)} ${r.speech.toFixed(2).padStart(6)}  ${r.fits ? 'yes ' : 'NO  '}  ${r.text}`);
const bad = report.filter(r => !r.fits);
console.log(bad.length ? `\n${bad.length} line(s) overrun their read: shorten the text or lengthen the read in six_story.js.` : `\nAll ${report.length} reads spoken, each inside its slot. Nothing described that isn't in the storyboard; nothing in the storyboard left undescribed.`);
writeFileSync('out/ad_report.json', JSON.stringify(report, null, 2));
