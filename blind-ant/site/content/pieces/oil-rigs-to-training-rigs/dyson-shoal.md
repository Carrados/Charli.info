---
title: Dyson Shoal
kind: object
order: 8
description: Ten years after the first sixty-four pods, 7,680 of them lie on the floor of the North Sea, and nobody is entirely sure where the data centre ends.
label_title: Dyson Shoal
label_meta: Sunday supplement, ten years on. Aberdeen, 2041.
label: |
  Ten years after the first sixty-four pods, 7,680 of them lie on the floor of the North Sea, and nobody is entirely sure where the data centre ends.
---

*Aberdeen, 2041. Ten years ago, Haar Compute put sixty-four computers on the seabed around an old oil platform. Today nobody is entirely sure where the data centre ends.*

From the helideck of Skerry Alpha, very little has changed. The cranes are newer, the accommodation block has been reclad twice, and the old drill floor is now mostly transformers and switchgear that hum loudly enough for visitors to be handed ear defenders. But the turbines still turn to the horizon, the helicopters still come in from Dyce, and the North Sea remains grey, cold and deeply unimpressed by whatever anyone thinks they have invented.

The interesting part is sixty metres down. And seventy kilometres east. And forty kilometres north. And, increasingly, almost everywhere in between.

There are now 7,680 compute pods on the floor of the central North Sea, linked by power and fibre into what Haar Compute rather boringly calls the Skerry Distributed Training Array. Nobody else calls it that. Everybody calls it the **Dyson Shoal**.

## From ring to shoal

It started with sixty-four. The first ring went live around Skerry Alpha in 2032: sealed pods arranged around a converted oil platform, powered by offshore wind and cooled by the sea. The idea sounds obvious now, as good ideas do afterwards. Scotland had electricity it couldn't always move south. The North Sea had platforms, cables, pipelines, helicopters, ports and half a century of experience keeping expensive machinery alive in extremely unpleasant places. Artificial intelligence needed extraordinary quantities of power and cooling. So you put the computers where the power was.

For the first few years, the platform was the data centre. Then someone laid another fibre trunk. The second cluster went down three kilometres away, the third eight. New subsea substations let clusters plug straight into the wind farms without routing everything through Skerry Alpha. By 2036 there were 900 pods and three converted platforms, and the word "ring" had become ridiculous.

The name that replaced it first appeared, apparently, in an engineering newsletter. The physicist Freeman Dyson once imagined a swarm of machines surrounding a star to capture its energy. The North Sea version is rather wetter and involves considerably more barnacles. Haar Compute disliked the name for approximately six weeks. Then somebody in marketing bought the domain.

## The rigs aren't the computers

This is the part people still get wrong. There are six training rigs in the Shoal, and they contain surprisingly little compute. They are workshops, power stations, crew hotels, helicopter terminals and ROV bases. Above all, they are places with cranes, where broken things come up from the sea and working things go back down.

The compute itself is spread across some 1,800 square kilometres of seabed. A modern pod is still roughly the size of the shipping container its ancestors resembled, although almost nothing inside looks like a conventional server. Each is a sealed pressure vessel of accelerators, optical networking, power conditioning and its own monitoring. Pods are laid in shoals of sixteen. Shoals form banks, and banks connect to one of six service nodes.

The software treats the whole thing as one machine. The hardware emphatically does not. If a pod fails, work routes round it. If a fibre trunk is cut, another path carries the traffic. If Skerry Alpha loses power, five other nodes carry on. That architecture grew out of a lesson learned early and painfully: putting a computer underwater is easy. Putting 7,680 of them underwater, when fishermen, anchors, corrosion, currents, storms, seals and everything else in the sea all get a vote, is considerably harder.

"We stopped trying to build a data centre," says Haar's founder, Fiona Gauld. "Data centres are buildings. This is infrastructure." She pauses. "Actually, the people who run it say it's a fishery."

## A quadrillion parameters

At 02:14 on 3 February this year, the Shoal completed the main training run for **Kelvin**, the latest generation of Britain's national foundation model. By most counts it is the first model anywhere with more than a quadrillion parameters: a thousand trillion of the adjustable numbers in which a model stores what it has learned.

The number needs handling with care, and the people offshore are the first to say so. Kelvin is a "mixture of experts," built from thousands of specialist sub-networks, and only a small fraction of them wake for any given question. Most of the model, most of the time, is resting. The engineers like the comparison. A shoal of fish is never all moving at once either. Different experts trained in different banks, and the model's structure ended up looking, on the engineers' diagrams, uncannily like a map of the seabed it grew on.

Nor did Kelvin learn from a quadrillion words scraped from the internet. By 2041 almost no serious training works that way. It learned from text, code, scientific data, video, audio and simulated worlds, and above all from material made for it: curricula written by other models, problems reworked into new forms, and synthetic examples designed to probe weaknesses discovered earlier in the run. Models set exams for other models.

"It's a headline," one of the shift supervisors tells me. "We don't count parameters out here. We count weather."

What the number does capture is the work. For eleven weeks, thousands of pods joined the run whenever wind, scheduling and other customers allowed. At its peak the Shoal drew several gigawatts, and on windy nights it was among the largest single users of electricity in Britain. On calm nights it was considerably smaller, and that is the point. Haar still runs on the rule written into Skerry Alpha's operating procedures in the 2030s: **we follow the wind.** Training jobs are built to checkpoint, migrate, accelerate and wait. The North Sea does not sign service-level agreements.

## The computer that breathes

At three o'clock on a windy February morning, the Shoal can be almost frighteningly busy. Jobs expand into spare banks, electrolysers throttle back, batteries stop charging, and the fibre trunks fill with checkpoints and model state as thousands of accelerators run flat out.

Then the weather changes, and the machine exhales. Low-priority jobs pause first. Flexible contracts shed load. Whole banks drop away, and stored power takes over the small base load that can't easily stop. If the calm lasts, the hydrogen comes in. If it lasts longer still, the clients wait.

This horrified the old data-centre industry, which had spent decades treating uninterrupted power as something close to a religious requirement. Haar's engineers changed the other side of the equation. Instead of forcing variable renewable power to behave like a conventional power station, they made training behave like a variable industrial load. The idea has since been copied everywhere. Texas does it with solar, Québec with hydro, Patagonia with wind. But the first machines to learn they could wait for the weather learned it here.

## Listen carefully

Daniel Okafor retired from night shifts three years ago. His interface didn't.

Okafor was one of Skerry Alpha's first control-room technicians, and the first blind one. In 2033, irritated by a monitoring system that showed sixty-four pods as coloured boxes, he gave each of them a sound. Temperature bent the pitch, load set the volume and network quality changed the texture, and a healthy ring became a chord. It turned out he could hear changes that sighted colleagues missed while scrolling through dashboards. What began as his workaround became the company's standard monitoring layer.

The Shoal is far too big to give every pod its own note, so the system now compresses its state in layers: pods into shoals, shoals into banks, banks into regions. An experienced operator can listen to the North Sea at any level, from the whole array down to a single machine. Control rooms around the world use versions of the technique, and the discipline has acquired the slightly grand name **operational sonification**. Okafor still calls it listening.

These days he sits on the international standards board for non-visual interfaces, alongside Emma Heart, who in 2038 became the first totally blind skier to race Paralympic Super-G without a human guide. Her tactile field and his sonification began as different answers to the same question. "Daniel hears the sea, I feel the mountain," Heart says. "Neither of us is seeing anything. That was always the point." She is less diplomatic about the board's membership. "I have spent my entire career being told where to go by men called Daniel. At least this one only tells me what he can hear."

Haar Compute is the board's founding sponsor. It is also, quietly, one of the largest funders of independent safety assurance in Paralympic sport, a fact that appears nowhere in its marketing. Asked why, Gauld says only that she has "a professional interest in people who notice what everyone else misses."

When I ask whether he's surprised that something he built because he couldn't use the screens now helps run one of the largest computing systems on earth, there is a long silence on the line.

"No," he says eventually. "They had sixty-four things happening at once and thought the sensible solution was sixty-four little green squares." Another pause. "I was blind, not stupid."

## Aberdeen did not become Silicon Valley

For years, politicians promised that Aberdeen would become the Silicon Valley of something: offshore wind, hydrogen, robotics, carbon capture, artificial intelligence. Aberdeen stubbornly remained Aberdeen. That turned out to be the advantage.

The Shoal employs software engineers and machine-learning researchers, certainly, but few of them work offshore. The offshore workforce is made up largely of people whose job titles would have made sense thirty years ago.

Marine engineers. Crane operators. Electricians. ROV pilots. Subsea technicians. Pilots. Deck crews. Weather forecasters.

The machinery changed far faster than the reasons people were needed.

Morag Leask flew the ten to seven out of Dyce for thirty-four years, carrying drillers first, then decommissioning crews, then compute technicians. She retired in 2038. Her daughter flies the route now.

"It was never really about oil," she tells me when we meet near the airport. "We thought it was, because oil was what was there." What was actually there, she says, was fifty years of knowing how to work in the North Sea.

"The oil ran out. Aberdeen didn't."

## Not everyone is delighted

There are good reasons to be uneasy about the Dyson Shoal.

Seven thousand six hundred and eighty pressure vessels add up to an extraordinary quantity of manufactured hardware sitting on a living seabed. Haar publishes its recovery rates, seabed surveys and ecological monitoring, and environmental groups argue, reasonably, that monitoring damage is not the same as preventing it. The company's own surveys show the pods behaving much as old platform legs did. They are colonised within months by mussels, anemones and soft corals, with cod and pollack gathering around the banks. Haar calls this an artificial reef. Its critics call it a flattering name for an industrial estate.

Fishermen have their own complaint. The Shoal's protection zones close a large stretch of sea to trawling. Some skippers say the fish are coming back at the edges. Others say they have simply lost their grounds to a computer. Two fibre trunks were snagged by trawl gear in the early years, and a third was cut in 2039, in circumstances the Royal Navy still won't discuss. The Shoal is now patrolled, which is not a sentence anyone in Aberdeen expected to hear about a data centre.

Then there is the hardware. Every pod is recovered and refitted every three or four years, which means a steady stream of retired accelerators coming ashore. Haar says nearly all the vessels and most of the components are reused or recycled. Campaigners say "most" is doing a lot of work.

And there is the question that has followed the project from the start: whose machine is it? A fifth of the Shoal's capacity is reserved for British research and public models. The rest is rented, much of it to foreign labs. Kelvin was trained here, and that matters, but for much of the year the North Sea's wind is teaching other countries' models. "We built the cathedral," one Scottish MP tells me, "and we're renting out the pews."

Gauld doesn't dismiss any of it. "Every one of those arguments is fair," she says. "The difference is that we're having them in public, with numbers. Nobody had that argument about the oil until it was nearly gone."

## Ten to seven

I fly home with the outgoing shift on a February evening. The pilot is Isla Leask, Morag's daughter. She spent most of the 2030s certifying drone swarms for the aviation regulator before, as she puts it, she started missing the weather. Below us, the turbines are turning hard in a westerly, which means the Shoal is breathing in.

I ask whether she skis.

"Badly," she says, eyes on the horizon. "My wife's teaching me."

Before I left the platform, one of the night operators, a young woman who learned the job from Okafor's training recordings, handed me her headset and let me listen to the whole thing at the regional level. I had expected music. It isn't music. It sounds like weather: a vast, slow, shifting roar, swelling and fading as the wind moves across the farms and the banks below them wake and settle.

"That's the North Sea thinking," she said.

For fifty years, Aberdeen went offshore to take out what the sea had stored. Now it goes offshore every morning at ten to seven to help the sea do something it has never done before.

The oil ran out. The wind didn't. And Aberdeen, it turns out, never did.

[Next: Behind the fiction](/pieces/oil-rigs-to-training-rigs/behind-the-fiction/).
