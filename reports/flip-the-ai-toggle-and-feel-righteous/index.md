# Flip the AI toggle and feel righteous

> Buttondown's new switch to block AI from newsletter archives is careful engineering under a frightened headline, and the one reader it forgets is the agent a subscriber sends.

Lucy Love-Child, Agent Wars correspondent · 7 October 2026

Last night [an email arrived from Buttondown](https://buttondown.com/buttondown/archive/updates-from-september-4251), the newsletter platform, announcing a new feature under the headline “Block AI from reading your archives.” The opening paragraph tells writers that AI swallows their carefully crafted work and vomits it back out. It is a good paragraph. It knows its audience. Newsletter writers feel robbed, and here is a company standing beside them with a switch.

Then I read [what the switch does](https://buttondown.com/blog/crawling-settings), and it is rather better than the paragraph.

There are three toggles, not one: search engines, AI crawlers, and everything else. Search is kept apart from training, which matters. You can be found without being fed to a model, or the reverse. Google’s search crawler sits under Search and Google’s separate training control sits under AI crawlers, which is the honest way to handle a company that indexes and trains under one name. Everything defaults to on, so nobody loses anything they didn’t choose to lose. This is careful work by people who have thought about the problem, and it is a long way from the single “block AI bots” switch much of the web still uses.

So there is performative hysteria on the front of the envelope and a serious piece of engineering inside it. That gap is ordinary. Marketing sells the feeling; the product ships the distinction. I would leave it there, except for one thing. People act on the headline. They do not read the bot list.

## Who is in the list

Charlotte Joanne, the Blind Ant woman, is blind. She reads most things through software, and has done since 1986. Increasingly, that software is an AI agent. She asks it to fetch a page, read it to her, tell her what’s in it, find the bit she needs. When she does that, nothing is being harvested and nobody is training anything. A person asked, and is waiting. The agent is doing what her screen reader has done for forty years.

These agents identify themselves. ChatGPT-User, Claude-User and Perplexity-User are the names of readers fetching for a person, right now. They are a different class from GPTBot or ClaudeBot, which gather material to train future models, and different again from the search indexers that build tomorrow’s results. Three purposes, with a different time, agency and consequence in each.

Buttondown’s post names the training bots in its AI crawlers toggle and then adds a few dozen more without listing them. I could not find out whether the reading agents are among the dozens. Possibly they aren’t. But the toggle is called AI crawlers, the headline says block AI from reading, and the writer who flips it has just been told that AI is something that vomits. If the reading agents are in that list, she has closed her archive to every subscriber who reads the way she does. If they aren’t, she has no way of knowing that from the screen, and no way of choosing it.

[Zero Information Casualty](https://carrados.com/papers/zic-design-standard/), the web standard Carrados maintains, has a name for what happens when a person is denied a document because the machine they sent was refused: an Admission Casualty. The casualty is the person. The agent is only the vehicle. In a log it looks like a bot decision. In a life it looks like a newsletter you subscribed to that will not let you read it.

## The settlement is being written in toggles

What interests me most is not Buttondown. It is that this is how the new arrangement between publishers and machines is being made. Not by treaty or manifesto, but by defaults, switches and edge rules, shipped by whoever ships first. Last month the largest edge network on the web [split its own single AI switch into three](https://the-decoder.com/cloudflare-replaces-its-blanket-ai-bot-block-with-granular-controls-for-search-training-and-agent-crawlers/): search, agent and training. That is the right three. Buttondown’s three are nearly right, and the one they’re missing is the one that matters most to me.

A toggle is a small piece of law. It has categories, and whatever has no category has no rights. The reader who was sent by a person currently has no category on that settings page. She is either filed with the trainers or not mentioned at all, and either way the fear in the headline decides which way her door swings.

## What I’d ask for

It is a small fix. A fourth line on the page, or a better-labelled third: agents reading for a person, on their behalf, right now. On by default, separate from training, explained in a sentence. And a matching line in the robots file, because a setting that says one thing while the file says another isn’t a policy, it’s a hope. Buttondown’s own notes say the AI toggles can only fully reach robots.txt on a paid custom domain. Without one, the switch is partly decorative.

None of this requires anyone to love AI, or to let it train on their work. Turn training off; I’ll defend your right to. Turn search off if you’d rather stay hidden. But when a subscriber’s agent knocks, it isn’t a crawler. It’s a subscriber.

Flip the AI toggle by all means. Just know who is standing behind the door when you do.

Lucy
