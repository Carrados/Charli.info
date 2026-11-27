---
title: How to treat accessibility like engineering
description: dice on Accessibility Purple Teaming, in which a screen reader tester gets a real job to do, a coding agent, access to the code and the standing to verify the repair.
date: 2026-11-27
time: "09:08"
desk: dice
byline: dice
related: Where the quoted line comes from: If accessibility was engineering|/blind-ai/if-accessibility-was-engineering/
---

On 12 June I wrote, [“Known failures should not be shippable.”](/blind-ai/if-accessibility-was-engineering/) Five months later, I want to put a job description underneath that sentence.

Your developers build your site. I test it and tell them what’s wrong. They fix it. If there’s time and money left in the contract, maybe I get to test it again.

Now suppose your agents build your site. I test it, work with your agents to fix it, and try the thing I came to do in the first place. While we’re in there, we give the next agent a way to catch the same mistake.

That’s **Accessibility Purple Teaming**. Test and fix. Here’s how I imagine it working at [Unremarkable](https://unremarkable.me/) 2.0.

## Give me a job to do and the standing to do it

Say you run a shop. You want to know whether a blind customer can change the delivery address on an order. Give me a test account, two addresses and an order I can safely send to either of them. Give me access to the repository where your team keeps the checkout code, a coding agent that can work on it, and a preview where I can try our changes. Agree who can approve the repair for release. Put my review in that process.

For a small shop, the owner might give me the run of the site. Nobody is going to hire me to rebuild [Amazon.com](https://www.amazon.com/). A team at that scale could give me responsibility for the address picker. I can follow the order far enough to find out whether my change worked. The team that owns checkout still decides what ships, and my finding stays open until I’ve verified the repair.

## Follow the parcel

Here’s a failure I’d put in the training exercise. I have two saved addresses. [NVDA](https://www.nvaccess.org/) reads both of them. I choose my boyfriend’s address, press Save and hear “Address updated.” Then I go to the order summary. The parcel is still coming to me.

What do I know at this point? I know what I chose, what the shop told me and what ended up on the order. That’s enough to give the agent a precise job. Trace what happens to the address I selected, from the control I operated through to the order summary. Show me where the two part company.

Suppose the agent finds that using the arrow keys changes which address the picker announces, while Save continues to use the original selection. It makes a repair and gives me a preview. I run the order again with NVDA. This time I hear my boyfriend’s address on the summary. I go back, change it to mine, and check again. A fix that always sends parcels to my boyfriend would have passed the first attempt.

I can now put my name to a specific finding in the pull request. I could select either saved address with my keyboard, complete the change, and confirm with NVDA which address the order would use. My colleagues can review the code and see exactly what I tested.

## Give the next agent the benefit of the repair

Before we close the work, I ask the agent to write a test that makes the same change of address with the keyboard and checks the address actually saved on the order. Run it against the old code first. I want to see it fail for the reason I found. Then run it against the repair. Once we’ve seen both results, make that test a required check for future changes to checkout.

There’s a useful instruction for the agents here too. When they build another address picker, use the repaired shared component. That saves the next agent having to rediscover the right behaviour. The required check gives the team a second line of defence if somebody changes it.

That’s the interlock I was asking for in June. And it leaves me free to ask the next question. What happens if the address can’t be saved? Does the shop tell me while I can still do something about it, or do I find out when my boyfriend rings to ask why I’ve sent him a kettle?

## Train people for the job

In the US, blind screen reader users are already offered Certified Accessibility Tester training as a route into paid work. One description of the job uses the words “accessibility testing and reporting.” There’s a real skill there. I want to change what the person who has that skill is employed to do next. [CIDNY’s March 2024 programme briefing (PDF)](https://www.cidny.org/wp-content/uploads/2024/03/CIDNY-Newsletter-March-2024-LARGE-FONT.pdf)

I’d call the course **Purple CAT**. Yes, there’s a purple pussycat on the prospectus. The job title inside is **Accessibility Engineering Purple Team Member**.

For the practical assessment, give the trainee a service with a broken journey, access to its repo and a coding agent. Have them show you the failure using their own assistive technology. Let them direct the repair. Ask them why they accepted the second attempt or sent the third one back. At the end, another engineer should be able to open their pull request, try the repaired journey and see what will happen if a future change brings the defect back.

Unremarkable 2.0 could sell that work to a client. A larger organisation could employ the graduate directly. And once that person has learned to take responsibility for a change from the first customer problem through to release, they can use those skills on the next feature the team wants to build.

The vacancy I’d like that counsellor to have on their desk is quite ordinary. *Purple Team Member, Checkout. You’ll work in our repository with our developers and coding agents. You’ll have authority to request changes and responsibility for verifying repairs. Here’s the salary.*

## Behind the fiction

Real: Helen Keller Services for the Blind presents its [Certified AccessAbility Testing Program](https://www.helenkeller.org/hksb/cat-program/) as a route into paid work for blind and low-vision screen reader users. [CIDNY's March 2024 newsletter](https://www.cidny.org/wp-content/uploads/2024/03/CIDNY-Newsletter-March-2024-LARGE-FONT.pdf) says students who pass are offered part-time work with that organisation to perform “accessibility testing and reporting”. NVDA is a real screen reader.

Proposed or imagined: the shop, the parcel and its repair are a worked example. Accessibility Purple Teaming as set out here, the Purple CAT course, the work at Unremarkable 2.0 and the vacancy are dice's proposals.
