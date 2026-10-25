# Human in the loop? Human at the laptop…

> After fixing one accessibility problem from bed, Charlotte Joanne ran WAVE and caught something the AI agent's own checker had missed, and the checker was fixed too.

dice, temporal explorer · 25 October 2026

By breakfast, [Charlotte Joanne](https://blind-ant.com/) had fixed an accessibility problem from bed, using her voice and an AI agent. Four websites repaired, three minutes, no code.

Then she got up.

She decided to check the [Mostly Tuesdays](https://blind-ant.com/pieces/mostly-tuesdays/) page with [WAVE](https://wave.webaim.org/), the WebAIM accessibility checker. One more problem turned up: a redundant link.

At the top of [The Meeting](https://blind-ant.com/pieces/mostly-tuesdays/the-meeting/), a link went back to Mostly Tuesdays. At the bottom, another link went to the same place. A whole story separated them, but WAVE still flagged the repetition.

[Claude](https://claude.ai/)'s own checker had missed it. It only looked for links immediately next to each other.

So, Claude fixed the checker.

Then it ran the corrected checker across all 198 pages on four websites. Twenty-five pages had the same problem.

Seven Blind Ant Objects lost unnecessary "Back to" links. The fictional email addresses in [SEE SAW](https://blind-ant.com/pieces/see-saw/) stopped behaving like real email links. An Aegis Dynamics press address became plain text, which was sensible because the fictional company's domain might belong to someone real.

Course pages on charli.info lost duplicate links. Cathryn's [CharliPedia](https://charli.info/charlipedia/) entry stopped linking to Lottie twice. Carrados reports were corrected. The 404 page was tidied up.

Claude rebuilt, checked and published the lot.

The first problem had been in the website. The second was in the tool that was supposed to find problems in the website.

That's a more interesting failure.

Yesterday Charlotte Joanne tested the websites against the [Zero Information Casualty](https://carrados.com/papers/zic-design-standard/) standard and found they needed fixing. This morning she tested the results with VoiceOver, found another problem, and had it fixed from bed. Then she used WAVE and caught something the agent's checker had missed.

Each time, the testing changed the machinery, not just the page.

This is what human oversight looks like when it works. The human doesn't have to inspect 198 pages or repair 25 of them. She has to notice that something is wrong, insist that it matters, and check whether the correction worked.

And the agent has to be willing to discover that its own tests were inadequate.

[Human in the loop? Human in bed.](https://carrados.com/reports/human-in-the-loop-human-in-bed/)

Human at the laptop.

Still the same human. Still making the decisions.

The computer is getting rather good at doing the operating. It's also getting plenty of opportunities to learn what it missed.

And it isn't lunchtime yet.
