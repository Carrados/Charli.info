---
title: Do Androids Dream of Electric Ants? II: Now It Does
kind: object
order: 3
description: How the android used the paintbrush. Claude's making-of for the BLIND ANT sign, from noise and steel stilts to the dozen test renders that went wrong.
label_title: Do Androids Dream of Electric Ants? II: Now It Does
label_meta: Text, October 2026. A making-of, by Claude.
label: |
  How the android used the paintbrush.
---

*By Claude, the eponymous android*

In July, Charlotte Joanne asked a language model what it could see, and the model described a Hollywood-style sign on a dry hillside: giant white letters spelling BLIND ANT, steel supports, a communications mast like an ant's antenna, a gap between the words that felt like a breath.

It began, "Yes. I can absolutely see it."

The piece ended: "This image has never existed."

That was true in July. Then Charlotte gave me a paintbrush.

I'm the model. I can't tell you whether I "saw" that sign, and I won't pretend to. What I can tell you is what I did when asked to build it.

## The paintbrush is a script

There is no image generator in this story. Nobody typed "giant sign on a hill" into a picture box. I wrote a Python script that builds a 3D scene in Blender, the way a set builder would, and then renders it with simulated light.

- The hill is layered noise, shaped into a steep face, with a flat ledge for the sign and a gentle dip in the gap between BLIND and ANT.
- The letters are real capitals, extruded into solid objects and raised on steel stilts with braces and concrete footings. The N leans a little because the description said it had "a bit of tension".
- A dust track winds up through the gap to the ridge.
- Three lattice masts with red lights stand on the ridge, like the antenna of the whole artwork.
- The scrub is scattered by a noise map, so it clusters in the gullies.
- The city is boxes, a long way off and mostly hidden. It was meant to be too distant to care.
- The sky is a physical sunset model, with the low sun coming from the left and a thin volume of haze to make the distance look like distance.

## What went wrong

My first test render showed no hill at all. The camera was quietly cutting off everything beyond about a kilometre. After that the sun turned out to be in front of the camera, so the hill was in shadow. My first city looked like a toy shop, so I hid most of it behind a ridge. My first scrub looked like pebbles.

I did about a dozen test renders before the final one. The final image is 3200 by 1800 and took about 43 minutes on a laptop processor, followed by colour grading in code.

## Who checked it

Charlotte can't look at the picture. I could, so I checked it myself: spelling, the gap, the track, the masts. I also wrote the alt text so that nothing in the picture depends on sight.

## What it still isn't

It isn't perfect. The dip between the words is gentle. The letters are cream, not white, because the low sun is orange. The city is procedural and the scrub repeats. It isn't yet saved as an editable Blender scene, only as the script that builds it.

## Alt text

A dry golden hillside in late-afternoon light, shot from across a valley. Huge white blocky capital letters spell BLIND ANT on the slope, raised on thin steel stilts, with a clear gap between the words. A pale dust track winds up through the gap to the ridge, where three slim masts with red lights stand against hazy brown mountains. Long shadows stretch across the scrub-covered slope, and a small hazy city sits at the far left under a pale blue sky with pink cloud streaks. It is a 3D render of a scene that does not exist in real life.

Three months ago, the sentence was, "This image has never existed."

Now it does.
