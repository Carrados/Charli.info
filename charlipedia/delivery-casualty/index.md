# Delivery Casualty

> A Delivery Casualty happens when the document exists and the observer is welcome, but it never arrives.

**Real.** This entry is about something real, written from outside the CharliVerse.

A **Delivery Casualty** is the third of the four classes of [information casualty](https://charli.info/charlipedia/information-casualty/) in the [Zero Information Casualty](https://charli.info/charlipedia/zero-information-casualty/) standard. The document existed, the observer was welcome, and it never arrived. Its question is *did it actually arrive?*

It deserves its own name because every usual check is blind to it. WAVE, axe, Lighthouse, the HTML validator and a screen reader test will all pass a page nobody on earth can fetch, because each begins by loading the page successfully. "A tool that has the document cannot tell you the document is unreachable."

It wasn't hypothetical. The first ZIC site, charli.info, spent several days with immaculate HTML, AAA contrast and a robots file welcoming named agents, served behind a security certificate for a domain it didn't own. The certificate was valid, trusted, and for somebody else. Every agent checking the hostname failed, couldn't read the robots file, and reported the site as closed. It was "perfect and unreachable". It was found by one check: a person asked a live AI assistant to fetch the site, and it couldn't.

The core test: "does the document arrive at a plain client that does not already trust you? If you cannot answer that from outside your own machine, you do not know whether your site works." That is why [declaration is not compliance](https://charli.info/charlipedia/declaration-is-not-compliance/).

## Behind the scenes

A real idea, from [Zero Information Casualty v1.7](https://carrados.com/papers/zic-design-standard/), the design standard by Charli-Jo Tyrer and Claude, §1.8 and §4.7. This entry summarises it; the standard is the authority.
