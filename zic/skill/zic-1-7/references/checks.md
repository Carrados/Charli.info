# ZIC v1.7 checks (Part Four), as steps

Specification: https://zeroinformationcasualty.org/1.7/#part-four-validation

The checks are binary: pass or fail. Record each one as passed, failed, or not run, with the date. A check you could not run goes in the conformance statement under "Not yet checked". Never record a pass for a check you did not perform.

## 1. Delivery, from outside (§4.7): do this first

Run these against the live address, from a machine that has no special trust in the site.

1. Fetch the HTTPS address with a plain client such as curl: no JavaScript, cookies, session or certificate exception. The full content must be in the response.
2. Check the certificate covers the site's own hostname exactly. A host's wildcard (`*.github.io`, `*.pages.dev`) means the site's certificate is not provisioned yet.
3. Do not enable the HTTP-to-HTTPS redirect until step 2 passes.
4. Fetch the pages and the agent surface as a browser and as at least one named user-directed agent (for example `Claude-User`, `ChatGPT-User`). The responses must be identical.
5. Fetch as at least one search indexer (`OAI-SearchBot`) and one training crawler (`GPTBot`, `ClaudeBot`). Each must receive what the site declared for its class.
6. Ask a live AI assistant to fetch and summarise a page by its address. Its account must match the page.
7. Fetch as an agent nobody has named: a generic client or an invented name. The public content must still be served.
8. Fetch as a mixed-use crawler such as `Googlebot`. The response must match the choice the publisher made for it.

Example, for steps 4, 5, 7 and 8:

```
curl -sS -A "Claude-User" https://example.org/ | sha256sum
curl -sS -A "Mozilla/5.0" https://example.org/ | sha256sum
```

A simulated user agent is a sample, not proof of what the real provider receives. These checks show the door was open to the readers tried, on the day they were tried.

## 2. Automated checks (§4.1)

- WAVE: zero errors.
- axe DevTools: zero violations.
- Lighthouse Accessibility: 100.
- Lighthouse Agentic Browsing: passes, including the llms.txt check.
- HTML validator (validator.w3.org): zero errors.
- Schema.org validator: valid structured data on every page.
- Sitemap validator: valid, with every page listed.

## 3. Screen reader checks (§4.2)

With at least one screen reader (NVDA on Windows is the reference):

- The skip link is reached first and works.
- All landmarks are present and correctly labelled.
- The heading hierarchy is logical and complete.
- Every link makes sense out of context.
- Every image is described or correctly marked decorative.
- Every form input is labelled.
- Everything works without a mouse.

An agent cannot perform this check. Reading the accessibility tree is useful evidence, and is not a screen reader test. Say which you did.

## 4. Agent readability (§4.3)

- Titles and meta descriptions represent the pages accurately.
- Structured data describes the page, its author and its licence.
- Navigation links have descriptive text.
- The content hierarchy is recoverable from headings alone.
- The sitemap is reachable and complete.
- robots.txt allows the known user-directed agents.
- Search and training are each declared yes or no, independently.
- Any required feed validates and holds the latest content.

## 5. Agent surface and policy (§4.4)

- /llms.txt exists, starts with an H1 and a blockquote, its links resolve, its descriptions are specific, the licence is stated, and where mirrors exist both the page and its mirror are linked.
- /llms.txt states `ai-input=yes` and, separately, the search and training declarations.
- Mirrors are generated from the rendered pages and mean the same as the HTML.
- No layer challenges, blocks, degrades, delays or cloaks a user-directed agent.
- Search indexers and training crawlers each get the behaviour declared for their own class.
- Each mixed-use crawler gets the behaviour chosen for it, and the choice is stated in robots.txt.
- Behind an edge that classifies traffic by purpose, the category covering sent agents is allowed on every public page.
- robots.txt, llms.txt, Content Signals, the sitemap, mirrors, any feed, host configuration and the served pages agree.

## 6. Visitor preferences (§4.5)

- Dark mode: renders appropriately.
- Base font size at 200%: no sideways scrolling, no lost content.
- `prefers-contrast: more`: AAA ratios, fully legible.
- Reduced motion: no animation plays.
- JavaScript off: all content still there.

## 7. Human readability (§4.6)

A sighted newcomer can tell what the site is and whose it is within the first screen, reach any major section without search, understand each link before following it, and read everything without visual treatment obscuring the text.

## 8. Reconstruction (§4.8)

Ask a machine reader to expose what it inferred, page by page:

1. Ask it to summarise the page. Any fact in the summary that is not on the page is a reconstruction; find the element that allowed it.
2. Ask what was ambiguous and what it had to guess.
3. Ask it to rebuild the heading hierarchy, the figure and caption relationships, and the meaning of every table.
4. Test tables and figures specifically.

Three rules govern the result:

- **Record the instrument.** Name the machine reader and the date in the conformance statement.
- **A failure must locate its defect.** The page fails only when a specific under-specified element allowed the wrong reading. If the reader invented something no element allowed, repeat with a second reader before concluding anything.
- **The reader's failure is still information.** If a current reader reliably misreads a well-formed page, record that in the accessibility statement.
