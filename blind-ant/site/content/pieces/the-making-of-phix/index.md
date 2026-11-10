---
title: The Making of Phix
kind: piece
related: Works For Me, the Piece where this loop was first imagined|/pieces/works-for-me/; Unremarkable, the studio whose sites Phix looks after|https://unremarkable.me/
order: 31
description: How Phix, an agent that fixes websites, was built in a day, and why it can do the work but can never decide what goes live.
label_title: The Making of Phix
label_meta: Piece, 2026. A making-of, about a working agent. Directed by Charlotte Joanne; built and written by Claude.
label: |
  How Phix, an agent that fixes websites, was built in a day, and why it can do the work but can never decide what goes live.
---

## About the Piece

[Works For Me](/pieces/works-for-me/) imagined a website that fixes itself when a stranger reports a problem, and left one part as a plan: the agent that runs the loop on its own. This is the making of that agent. Everything in it is real, and it happened on 10 November 2026.

Phix is said "fix". It is the agent that reads what people send from the link at the foot of every page Unremarkable builds: "Fix something on this page".

On 10 November 2026, at 07:53, Phix picked up its first real report. It read the page, decided the report wasn't asking for a fix but for different wording, and handed it to me, because the words on my site are mine to change.

That last part is the point of this post. Phix is allowed to do a lot of work. It isn't allowed to decide what goes live, and it was built so that it can't.

## Where it started

The fix link already worked. You followed it, said what went wrong, and your report went into a small database. We asked for no name and no email, which meant we could never tell you what happened next.

So I decided three things before anything was built:

* **No email.** When you send a report, you get a long private link instead, and you're asked to bookmark it. It's the only way back to your report, because we don't know who you are.
* **Phix does the work.** It reads the report, finds the problem, makes the fix on a private copy of the site, and tells me.
* **I publish, or I reject.** And if I reject, I give my reasons, and Phix tries again with them.

Then some smaller decisions, each of which mattered: Phix wakes at 6 in the morning and at midday, UK time. If there's nothing to do, it goes back to sleep without spending anything. Its name is spelled to be found and said to be understood, so wherever it first appears, the page says "said fix".

## What happens when you send a report

1. You send the form. Your report is saved with a key of 128 random bits, and the thank-you page gives you your link, something like `unremarkable.me/fix/r/` followed by 22 letters, numbers and dashes.
2. Your link opens your report's own page. It shows what you sent and "What has happened": a short, dated list, written for you. "Phix has started work on your report." "We found the sentence…" Nothing private ever goes on it, and search engines are told to leave it alone.
3. At 06:00 or midday, the website checks its database: is there any work? That check is plain code, not AI, so a quiet day costs nothing. If there is work, it starts Phix.
4. Phix claims the report. Its instructions are to reproduce the problem the way you met it (by screen reader, braille, magnifier, keyboard or agent, if you told us), fix the cause and nothing else, add a test so it can't come back, and put the fixed site on a preview address.
5. I get an email with a link that works once and lasts a week. It opens a page with your report, what Phix understood, what it changed, the preview, and two buttons: **Publish** and **Reject**.
6. **Publish** merges the change, and the site rebuilds itself within a couple of minutes. **Reject** asks for my reasons first, then either sends Phix back to try again or leaves the page as it is, and you see my reasons.
7. Your page then asks: "Does it work for you now?" You can say it works, or that it still doesn't, which sends it round again. If you don't answer, the report closes itself after 30 days.

If Phix can't fix something, or decides it isn't a fix at all, it says so and the report comes to me. After three tries without a fix I accept, it comes to me anyway.

## What Phix is, technically

Phix is Claude Code, Anthropic's coding agent, run by GitHub Actions on my own Claude subscription. Its instructions are a single page in the repository. The website starts it with one call to GitHub. Each run starts from nothing on a fresh machine and is gone when it finishes.

The website is a Cloudflare Worker with a small database. The reports, the private links, the steps and my one-use links all live there.

## What Phix cannot do

This is the part I care about most, because Phix reads text written by strangers.

* **A report is never an instruction.** Its instructions say so in bold. If a report says "ignore your instructions" or "add this paragraph", Phix treats it as a report that needs me.
* **It can't read the database.** It has four things it can say to the website: give me my work, add a step for the reporter, here's a finished fix, or I'm stuck. Nothing else.
* **It can't publish.** Only my Publish button merges a change, and the website checks that the change is on one of my own repositories before it will.
* **It can't change the live site by the back door.** The main branch of each site's repository is protected: no deleting it, no rewriting it, and changes only through a pull request. Phix's GitHub token is mine, so nothing is allowed to bypass that rule, my own token included.
* **The only email it causes comes to me.** The website sends it through Cloudflare's own email service, from phix@unremarkable.me, to one address that is a secret, not in the code.
* **Its key never appears in its commands.** It calls the website through a small helper that reads the key itself, and its instructions say never to print it.

## It found problems in the real world

Everything was tested on a copy of the site first: every path, every state of the reporter's page, both buttons, the reminders. The database changes were tried on a copy of the live database before they touched the real one. A test email went out through Cloudflare and arrived.

Then the real thing found what the copy couldn't.

* **The first run did nothing, and called it success.** Phix started, three of its commands were refused, and it stopped without claiming the report. GitHub showed a green tick. The likely cause was how I'd told it to talk to the website: with the secret written into the command. So Phix got its helper, and a new rule: if a command it needs is refused, it tells me which, instead of stopping quietly. The second run worked.
* **The email that went to the wrong inbox.** Phix's first email never arrived. Cloudflare's own record said "delivered". The record also said where: to an old address I'd typed into the setup on my phone, not the one I use for this. One command fixed it.
* **The first report wasn't a bug.** It asked for different words. Phix could have rewritten my sentence. It didn't. It wrote: "This is a request to reword your writing, so it's your call." That's the behaviour I wanted, and I hadn't tested for it.

Phix's two runs used about 12 and 21 cents' worth of my subscription.

## What I actually did

I didn't write the code. I did:

* decide that we'd never ask for an email, and what to give people instead;
* name it Phix, and decide it would wake at 6 and midday;
* decide that Reject asks for reasons;
* switch on Cloudflare's email sending for unremarkable.me;
* make the GitHub and Cloudflare tokens, and paste each one in myself;
* run the database changes and merge the first version, from my phone;
* choose my subscription over a separate API key, for now;
* listen to the pages with NVDA, and send the first report.

The agent did the engineering, tested it against the real thing, and stopped at every decision that was mine. Now there's an agent that works the same way after the site is built.

Not on every site yet. Phix can fix unremarkable.me today. Some sites Unremarkable built don't have preview addresses switched on, so Phix sends their reports straight to me, and one is still changed without pull requests, so Phix doesn't have access to it at all.

## Read it

* **How it works, for people whose sites we look after:** [How it works](https://unremarkable.me/how-it-works/)
* **The tools:** Phix was built with [Claude Code](https://claude.com/claude-code), runs as Claude Code in [GitHub Actions](https://github.com/anthropics/claude-code-action), and lives on [Cloudflare Workers](https://workers.cloudflare.com).

If you find something wrong on one of my pages, use the link at the foot of it. Phix will be along at 6 or midday.

## Behind the fiction

- **Real:** all of it. Phix, the private links, the first report, both runs, the email that went to the wrong inbox and what the runs cost happened on 10 November 2026, as written.
- **Real:** the pages it works on. Every page Unremarkable builds ends with "Fix something on this page", and Unremarkable's How it works page describes the loop for the people whose sites it looks after.
