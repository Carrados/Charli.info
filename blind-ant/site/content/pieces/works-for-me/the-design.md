---
title: The design
kind: object
order: 2
description: How a self-healing website works: five steps from a reported bug to a live fix, two gates on the way, and why the person who found the bug tests the fix.
label_title: The design
label_meta: Design, 2026. A plan for a loop that isn't built yet. Written by Claude.
---

## The idea

An automated checker can tell whether a page has the right parts, such as headings, alt text and a skip link. It can't tell whether the page works for the person using it. That takes someone who uses a screen reader, magnification, a switch or braille every day, and those are exactly the people who find the bugs.

Most bug reports go nowhere. Someone writes in, nobody replies, and if anything is ever fixed, they find out by accident. This design keeps the person who found the bug in the loop, and makes them the test.

## The loop

1. **The report.** Someone emails fix@ at the site's domain. Cloudflare Email Routing passes the message to a small program that keeps the report and starts a fix. The reporter's address never goes into the site's code or its history.
2. **The fix.** Claude reads the report, finds the problem and fixes it on a branch of its own, away from the live site. The site is rebuilt and checked: the build, the headings, the links, an automated accessibility scan, phone width and the Markdown version.
3. **The mirror.** The branch is put online at an address of its own, a copy of the site with the fix in. Search engines are told to ignore it.
4. **The question.** The reporter gets an email with the link: try it the way you found the problem, and reply to say whether it works. If it doesn't, their reply becomes the next report and the loop goes round again.
5. **The merge.** When the reporter says it works, the owner gets one email with what was reported, what changed, the reporter's answer and the check results. One word, "ship", puts the fix live. The reporter is thanked and told.

## The two gates

A fix goes live only when two people have said yes:

- **The reporter**, who says it works for them. No checker can do this.
- **The owner**, who says it belongs on the site. Only they can do this.

The reporter can't be the only gate, because the person who asks for a change and the person who approves it would then be the same. Anyone could write in asking for anything, see it on the mirror and reply "works for me". Reports are treated as information about the site, never as instructions to follow. The owner's email says plainly whether any words or links have changed, because those changes need the closest look.

## What a "yes" covers

One reporter's yes covers one setup: their screen reader, their browser, their device. That's why the automated checks still run on every fix. The reporter proves the fix works for the people it was for. The checks make sure it hasn't broken anything for everyone else.

## Privacy

Reports are kept only as long as the fix takes. Reporters' names and addresses are never published or put in the site's code. A site using the loop says so in its accessibility statement.

## Where it starts

On unremarkable.me first. It's the studio's own site, and if the loop is going to be wrong about something, it should be wrong there.
