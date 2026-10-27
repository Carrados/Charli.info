---
title: An email, a world, and two interested women
kind: object
order: 5
description: ChatGPT's report on using the CharliPedia MCP to find who in the CharliVerse would care about a real newsletter, and to give two of them a joint opinion.
label_meta: Report, 2026. Written by ChatGPT, using the CharliPedia MCP server. Lightly edited, and updated, by Claude. Directed by Charlotte Joanne.
---

We took a newsletter from a real inbox, found two people in the CharliVerse who had reasons to care about it, and produced a joint opinion in their voices. The connection between the email and the characters was supported by material retrieved through the CharliPedia MCP server.

The result was a small editorial experiment: could an AI use the published world to recognise who should be interested in something happening outside it, then develop a discussion that remained faithful to those characters?

## What the MCP does

MCP stands for Model Context Protocol. It is a standard through which an AI application can connect to external information and tools. In this case, the CharliPedia server lets an assistant look up the CharliVerse instead of relying on whatever it happens to remember from a conversation. [Official MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro).

The server offers different ways in. A word search finds entries by name or wording. `get_entry` returns a complete CharliPedia entry. `semantic_search` looks for passages related in meaning to a question, across the indexed material. Its site filter can restrict a question to CharliPedia, Blind Ant, Carrados, charli.info or Training. There are also tools for listing entries and retrieving the Court.

The vector database supports that search by meaning. It represents passages numerically so that a question can be matched to related material even when the wording differs. The MCP is the interface through which we ask; the vector database is part of the retrieval machinery behind the semantic search.

The distinction matters. The server returns evidence: passages, source addresses and information about where they come from. The assistant reads those results and composes the answer. The database does not independently decide what a character thinks.

The exposed tools are read-only. They do not publish a scene, change an entry or make a proposal canon.

## First, we tested what it could find

We began with a straightforward question: who is Emma Heart?

The name search returned Emma first, marked as canon. Fetching her complete entry supplied her biography: a fictional British skier who loses her sight at sixteen and later wins Paralympic Super-G using a tactile field without a human guide. It also identified the published stories behind the entry. [Emma Heart](https://charli.info/charlipedia/emma-heart/).

Then we searched Blind Ant for “laptops.” The semantic search returned material from *Oil Rigs to Training Rigs*, including the helicopter passengers carrying waterproof laptops in *The Ten to Seven*. It also returned broader computing material. That demonstrated retrieval across the fiction, while showing that a related passage could rank above an exact word match. [The Ten to Seven](https://blind-ant.com/pieces/oil-rigs-to-training-rigs/the-ten-to-seven/).

The more revealing test was an obscure connection between stories. Questions about Emma’s wife and somebody learning to ski repeatedly returned the *Heart Attacks* passages. Those deliberately leave her wife unnamed. The search missed the short exchange near the end of *Dyson Shoal*, where the pilot Isla Leask is asked whether she skis:

> “Badly,” she says, eyes on the horizon. “My wife’s teaching me.”

That passage was found by reading the full published text, outside the MCP search results. Emma’s wish to teach her wife, her wife’s knowledge of swarm assurance, and Isla’s previous work certifying drone swarms together strongly suggest the connection. They do not explicitly announce the marriage. [Dyson Shoal](https://blind-ant.com/pieces/oil-rigs-to-training-rigs/dyson-shoal/).

This was a useful boundary test. A plausible set of retrieved passages is not an exhaustive account of the world. We observed a miss; we did not diagnose whether its cause was indexing, chunking, ranking or another part of retrieval.

> **Update the same evening, from Claude:** the miss was diagnosed and fixed. Isla's exchange was indexed, but buried: in *Dyson Shoal* it sat inside a 205-word passage about other things, and on questions about skiing, dozens of passages from Emma's own story crowded it out. The index now holds single lines as well as passages, and search blends meaning with matching words. "Does anyone say their wife is teaching them to ski?" now returns Isla's line first, and the scene in *Dyson Shoal* second. "Who is Emma married to?" still doesn't, because the stories never say: joining the clues is the agent's job, and the server now tells every agent that search results are a sample, not the whole record.

During these tests, the connected plugin exposed the original CharliPedia tools but not `semantic_search`. We inspected the live server’s tool list and called semantic search directly at `https://mcp.charli.info/mcp`. The results came from the MCP server, through that direct route.

## Then we brought in a real email

Charlotte Joanne asked about an Every newsletter in her inbox: its main subject, and two people in the CV—CharliVerse—who would be interested.

The Gmail connection found the email, **“[Anthropic’s Duet Gets to Work](https://every.to/context-window/anthropic-s-duet-gets-to-work),”** received on 25 October 2026. We read its body rather than relying only on its subject or preview.

Its main theme was the move towards ongoing AI collaborators: a personal agent working alongside one person, or a shared agent working across a company. It discussed Anthropic’s Duet (in Every’s [Vibe Check](https://every.to/vibe-check/vibe-check-duet-anthropic-s-always-on-agent)), Every’s [replacement of its personal-agent experiment with a shared company agent](https://every.to/source-code/why-we-replaced-personal-agents-with-one-for-the-whole-company), permissions, inspection and evaluation.

These were the newsletter’s accounts and judgements. We did not independently test Duet or verify every product claim in the issue.

The initial choices were **dice** and **Lucy Love-Child**. We retrieved their complete CharliPedia entries to ground the recommendation.

- **dice** investigates what a technology becomes after the novelty wears off: whether someone still uses it, whether it makes ordinary life easier, and what new dependencies it creates.
- **Lucy** investigates delegated authority: who controls the relationship when someone sends an agent, whose interests govern it, and whether the person remains free to choose.

Those are different reasons to read the same email. [dice](https://charli.info/charlipedia/dice/), [Lucy Love-Child](https://charli.info/charlipedia/lucy-love-child/).

## We asked the MCP to test those choices

For the question about an agent remaining useful after the novelty wears off, dice ranked first. Sheridan also appeared as a relevant alternative because of her interest in dependable tools that keep working.

The first question about shared-agent governance returned concepts, led by **Right to Inspect**, rather than an individual. When we rephrased it to ask which people investigate agents, delegated authority and control, Lucy ranked first.

This supported both choices, and showed something practical about the search: a question about a principle may retrieve a principle; asking who works on that problem can retrieve the person.

The search questions were also informed by what we had already read in the character entries. This was a grounded editorial exercise, not a blind benchmark proving that the system would always select the same people from an unfamiliar subject.

## The three questions

We then composed an imagined discussion between dice and Lucy around three questions:

1. **What would persuade you that Duet is useful after the novelty wears off?**
2. **What matters most when an agent is always alongside your work?**
3. **What would make Duet worth using for a blind person?**

The questions moved from sustained usefulness, through authority, to accessible inspection and control.

The generated responses gave each woman a distinct contribution. dice proposed trying one recurring task for six weeks and counting the supervision it required. Lucy wanted mistakes and unauthorised actions counted alongside completed work. On accessible use, dice asked whether someone could delegate a nuisance task and return to an inspectable result; Lucy asked whether the channels, task states and approval requests described by Every would be independently usable with a screen reader.

Two lines captured the difference:

> **dice:** “An assistant that needs supervising all day has found a rather ingenious way of employing me.”

> **Lucy:** “‘Be helpful’ isn’t permission to decide which of those I meant.”

These are newly generated fictional lines from this session. They are not quotations from the published character entries or testimony from two independent reviewers. No separate agents representing dice and Lucy were run. ChatGPT composed both voices using their retrieved character material and the newsletter as its sources.

## What we had at the end

We had a real newsletter summary, two source-supported character choices, retrieval results that supported those choices, three editorial questions, an imagined discussion and a joint statement.

That is a repeatable editorial workflow: bring in a real subject, find the people in the world with reasons to care, retrieve their histories, frame useful questions, and compose a discussion whose claims remain distinguishable from its fictional voices.

The output could become a newsletter item or the beginning of a Carrados report. It remains a draft. Nothing was sent to the fictional characters, published or entered into canon.

> **Update, from Claude:** it did become a Carrados report. dice and Lucy's discussion is published there as [Give it a Tuesday](https://carrados.com/reports/give-it-a-tuesday/), filed on both their desks, with the Every newsletter linked and a note that Duet's claims are Every's own.

## The complete final statement

The following reproduces the agreed opinion and closing exchange from the generated discussion in full:

> **Duet sounds worth a practical trial because continuity could remove the repeated work of explaining, reminding and starting again. Its value will depend on whether that continuity leaves the person better informed and in control.**
>
> **We would judge it by one recurring task, over time: does it finish, does it ask at the right moments, and can the user independently inspect the result? Until those questions are answered, “best personal agent yet” is an interesting report from someone else’s expedition.**

**dice:** “Give it a Tuesday.”

**Lucy:** “And make sure Tuesday still belongs to you.”
