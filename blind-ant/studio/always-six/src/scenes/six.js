// six.js: "Always Six". One continuous shot, timed from STORY (six_story.js).
// Wash-only painting (no watercolour `fill`) so it renders quickly without a GPU.
(() => {
  const B = STORY.beats, G = 820, u = 26;
  const CLX = 760, DIE0 = [1010, G], LAND = [1330, G], S = 62;   // Clawd's spot, die start/landing (ground points), die half-size
  const RED = '#C8423A', RED_DK = '#8E2A25';

  // ---------- set ----------
  function room(t) {
    boilSeed('wall');
    paint(rectPts(-300, -300, W + 600, G + 300), { wash: mixCol(PAL.cream, PAL.ochre, .18), ink: null });
    boilSeed('window');
    paint(rrPts(240, 170, 360, 300, 14, 1.5), { wash: mixCol(PAL.sky, PAL.cream, .35), ink: PAL.ink, sw: .9 });
    inkLine([[420, 172], [420, 468]], .8, PAL.ink, 'ink', 0);
    inkLine([[242, 320], [598, 320]], .8, PAL.ink, 'ink', 0);
    boilSeed('floor');
    paint(rectPts(-300, G - 6, W + 600, 600, 2), { wash: mixCol(PAL.clayLt, PAL.cream, .45), ink: null });
    inkLine([[-300, G - 4], [W / 2, G - 9], [W + 300, G - 3]], 1, PAL.ink, 'ink', .5);
    for (let i = 0; i < 6; i++) {   // floorboard lines, fixed
      const x = 80 + i * 330 + hash(i) * 40;
      boilSeed('board' + i);
      inkLine([[x, G + 30], [x - 120, G + 300]], .5, mixCol(PAL.clay, PAL.cream, .4), 'inkfine', .2);
    }
  }

  // ---------- the die ----------
  const PIPS = { 1: [[0, 0]], 2: [[-1, -1], [1, 1]], 3: [[-1, -1], [0, 0], [1, 1]], 4: [[-1, -1], [1, -1], [-1, 1], [1, 1]],
    5: [[-1, -1], [1, -1], [0, 0], [-1, 1], [1, 1]], 6: [[-1, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [1, 1]] };
  function die(x, y, s, rot, face, key = 'die') {   // (x, y) = centre
    boilSeed(key + 'shadow');
    push(); translate(x, y); rotate(rot);
    boilSeed(key);
    paint(rrPts(-s, -s, 2 * s, 2 * s, s * .28, 1), { wash: RED, ink: PAL.ink, sw: 1.3 });
    paint(rrPts(-s * .82, s * .55, s * 1.64, s * .3, s * .12), { wash: RED_DK, washOp: 140, ink: null });   // a little shade on the bottom edge
    for (const [i, [px, py]] of PIPS[face].entries()) {
      boilSeed(key + 'pip' + i);
      paint(ellPts(px * s * .5, py * s * .5, s * .13, s * .13, 12), { wash: PAL.cream, ink: null });
    }
    pop();
  }
  const reach = (s, rot) => s * (Math.abs(Math.cos(rot)) + Math.abs(Math.sin(rot))) * .92;   // centre height above the ground for a tilted square
  function shadow(x, h, s, key) {
    boilSeed(key + 'sh');
    const k = clamp(1 - h / 700);
    paint(ellPts(x, G + 4, s * (.4 + .9 * k), s * .14 * (.4 + .6 * k), 20), { wash: PAL.clay, washOp: 60 + 90 * k, ink: null });
  }

  function shot(t, lt, dur) {
    const shake = t > B.land ? shakeXY(t, 9 * Math.exp(-(t - B.land) * 8)) : [0, 0];
    camBegin(kf(t, [[0, 1000], [B.throw, 1000], [B.land, 1080], [B.proud, 1040]]) + 14 * Math.sin(t * .7) + shake[0],
             kf(t, [[0, 600], [B.throw, 560], [5.5, 470], [B.land, 580], [B.proud, 590]]) + shake[1],
             kf(t, [[0, 1.08], [B.throw, 1.0], [5.5, .9], [B.land + .2, 1.02], [dur, 1.08]]));
    room(t);

    // Clawd: asleep → wakes and looks → idea → lift → wind-up, throw → watches it fly → lands: wide eyes → joy → proud
    const mood = emotions(t, [[0, 'sleepy'], [B.wake, 'surprised', { lookX: .9 }], [B.idea, 'idea', { lookX: .5 }],
      [B.lift, 'determined'], [B.throw + .05, 'hopeful', { lookX: .5, lookY: -.95 }], [5.7, 'nervous', { lookX: .9, lookY: .2 }],
      [B.six, 'surprised', { lookX: 1 }], [7.25, 'starstruck', { lookX: .8 }], [B.joy, 'excited'], [B.proud, 'proud', { lookX: .4 }]]);
    let pose = {};
    const head = [CLX + 20, G - 8 * u - 70];
    if (t >= B.lift - .2 && t < B.lift) pose = { sq: .16 * ease(seg(t, B.lift - .2, B.lift)), aL: -.3, aR: -.3 };   // crouch
    else if (t >= B.lift && t < B.throw) {
      const up = backOut(seg(t, B.lift, B.hold)), wind = ease(seg(t, B.hold + .12, B.throw));
      pose = { aL: lerp(-.3, 1.45, up) - .6 * wind, aR: lerp(-.3, 1.45, up) - .6 * wind, sq: .22 * wind };
    } else if (t >= B.throw && t < B.joy) {   // follow-through, arms settle while watching
      const a = t - B.throw, arms = 1.5 - 1.2 * ease(seg(a, .35, 1.0));
      pose = { aL: arms, aR: arms, sq: -.24 * Math.exp(-a * 7) * Math.cos(a * 18), dy: -1.1 * Math.exp(-a * 6) * Math.max(0, Math.cos(a * 9)) };
    }
    const hop = t > B.joy ? jump(t, B.joy + .15, B.joy + .8, 3.2) : { dy: 0, sq: 0 };
    const hop2 = t > B.joy ? jump(t, B.joy + 1.0, B.joy + 1.55, 2.2) : { dy: 0, sq: 0 };
    const cl = { ...mood, ...pose, sq: (mood.sq || 0) + (pose.sq || 0) + hop.sq + hop2.sq, dy: (mood.dy || 0) + (pose.dy || 0) + hop.dy + hop2.dy };
    if (t > B.joy) { const k = ease(seg(t, B.joy + .1, B.joy + .3)) * (1 - seg(t, B.proud, B.proud + .3)); cl.aL = lerp(cl.aL ?? .2, 1.45, k); cl.aR = lerp(cl.aR ?? .2, 1.3, k); }
    clawd(CLX, G, u, cl);

    // the die: resting (showing 3) → lifted overhead → thrown on a high arc, tumbling through faces → lands, bounces, SIX
    let x, y, rot, face, h;
    if (t < B.lift) { rot = -.08; face = 3; x = DIE0[0]; y = G - reach(S, rot); }
    else if (t < B.throw) {
      const k = easeOut(seg(t, B.lift, B.hold)), p = arcPt([DIE0[0], G - S], head, 90, k);
      x = p[0]; y = p[1] + 26 * ease(seg(t, B.hold + .12, B.throw)); rot = lerp(-.08, .15, k); face = 3;
    } else if (t < B.land) {
      const k = seg(t, B.throw, B.land), p = arcPt(head, [LAND[0], G - S], 620, k);
      x = p[0]; y = p[1]; rot = .15 + k * 9.4;
      face = 1 + Math.floor(hash(Math.floor(t * 9)) * 6);   // tumbling: a different face every ninth of a second
    } else {
      const a = t - B.land, bounce = 70 * Math.exp(-a * 5) * Math.abs(Math.sin(a * 11));
      rot = .35 * Math.exp(-a * 6) * Math.cos(a * 14);   // settles flat
      x = LAND[0] + 40 * easeOut(seg(a, 0, .6)); y = G - reach(S, rot) - bounce; face = 6;
    }
    h = G - S - y;
    shadow(x, Math.max(0, h), S, 'die');
    // a painted halo instead of glow(): glow forces a slow GPU read-back without a graphics card
    const halo = (t > B.land ? Math.exp(-(t - B.land) * 2.5) : 0) + (t > B.proud ? .45 + .15 * Math.sin(t * 6) : 0);
    if (halo > .03) { boilSeed('halo'); paint(ellPts(x, y, S * (1.5 + .6 * halo), S * (1.5 + .6 * halo), 28), { wash: '#FFE2A0', washOp: 150 * clamp(halo), ink: null }); }
    die(x, y, S, rot, face);
    if (t > B.land) for (let i = 0; i < 6; i++) {   // impact sparkle
      const q = seg(t, B.land + i * .02, B.land + .5 + i * .02), ang = -Math.PI / 2 + (i - 2.5) * .45;
      boilSeed('spark' + i);
      if (q > 0 && q < 1) paint(starPts(x + Math.cos(ang) * 150 * q, y + Math.sin(ang) * 120 * q, 16 * backOut(q) * (1 - q * .6), .25, 4), { wash: PAL.ochre, washOp: 255 * (1 - q * q), ink: null });
    }

    const mid = toScreen((CLX + x) / 2 - 10, G - 2.5 * u);
    camEnd();
    if (lt < .5) iris(...mid, lerp(0, 1500, easeIn(lt / .5)));
    if (lt > B.iris) {
      const r = lt < B.iris + .6 ? lerp(1500, 560, ease(seg(lt, B.iris, B.iris + .6))) : lt < dur - .35 ? lerp(560, 540, seg(lt, B.iris + .6, dur - .35)) : lerp(540, 0, easeIn(seg(lt, dur - .35, dur - .05)));
      iris(...mid, r);
    }
  }

  shots([[0, shot]]);
})();
