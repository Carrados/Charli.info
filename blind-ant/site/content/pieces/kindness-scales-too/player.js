// Progressive enhancement: the native player and complete lyrics work without this script.
document.querySelectorAll('[data-kindness-player]').forEach(async (player) => {
  const audio = player.querySelector('audio');
  const panel = player.querySelector('[data-caption-panel]');
  const current = player.querySelector('[data-current-caption]');
  const list = player.querySelector('[data-timed-lyrics]');
  const toggle = player.querySelector('[data-follow-lyrics]');
  const status = player.querySelector('[data-player-status]');
  let follow = false;
  let active = -1;
  const clock = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  const seconds = (s) => s.split(':').reduce((total, part) => total * 60 + Number(part), 0);
  try {
    const response = await fetch(player.dataset.captions);
    if (!response.ok) throw new Error('Captions unavailable');
    const source = (await response.text()).replace(/\r/g, '');
    const cues = source.split(/\n\s*\n/).flatMap((block) => {
      const lines = block.trim().split('\n');
      const i = lines.findIndex((line) => line.includes(' --> '));
      if (i < 0) return [];
      const [start, end] = lines[i].split(' --> ');
      return [{ start: seconds(start), end: seconds(end), text: lines.slice(i + 1).join('\n') }];
    });
    if (!cues.length) throw new Error('No captions');
    const buttons = cues.map((cue) => {
      const item = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = `${clock(cue.start)} — ${cue.text.replace(/\n/g, ' ')}`;
      button.addEventListener('click', () => {
        audio.currentTime = Math.min(cue.start, Number.isFinite(audio.duration) ? audio.duration : cue.start);
        sync();
        audio.play().catch(() => { status.textContent = 'Press Play on the audio controls to continue.'; });
      });
      item.append(button);
      list.append(item);
      return button;
    });
    function sync() {
      const index = cues.findIndex((cue) => audio.currentTime >= cue.start && audio.currentTime < cue.end);
      if (index === active) return;
      if (active >= 0) buttons[active].removeAttribute('aria-current');
      active = index;
      current.textContent = index >= 0 ? cues[index].text : (audio.ended ? 'End of song.' : '♪');
      if (index >= 0) {
        buttons[index].setAttribute('aria-current', 'true');
        if (follow && !audio.paused) buttons[index].scrollIntoView({
          block: 'nearest',
          behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
        });
      }
    }
    toggle.addEventListener('click', () => {
      follow = !follow;
      toggle.setAttribute('aria-pressed', String(follow));
    });
    ['timeupdate', 'seeked', 'ended'].forEach((event) => audio.addEventListener(event, sync));
    panel.hidden = false;
    current.textContent = 'Press Play to hear the song and follow the captions.';
  } catch {
    status.textContent = 'Timed captions could not be loaded. The audio controls, readable lyrics and caption downloads are still available below.';
  }
});
