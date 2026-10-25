---
title: Declaration is not compliance
description: Declaration is not compliance is the ZIC rule that a robots file only states a policy, and conformance is proved by fetching the site as the agent.
status: real
---

**Declaration is not compliance** is a rule of the [Zero Information Casualty](/charlipedia/zero-information-casualty/) standard. "robots.txt is where you declare. The stack is where you comply." A site proves it serves machine readers by fetching itself from outside, as each kind of agent, never by reading its own file.

A declaration can be sincere and false. A security layer or edge network in front of a site can refuse an agent the file welcomes. And a declaration is true of a whole stack at a moment: when an edge network began enforcing by category in September 2026, a site that had truthfully declared search=yes in July could start refusing Googlebot overnight "without a byte of its own files changing". That is why ZIC conformance statements carry a date, and why the outside fetch is repeated.

A conformance claim must name its version, link the standard, state its declarations, and say what was checked and what wasn't. "Under-claiming is permitted and is a virtue."

## Behind the scenes

A real idea, from [Zero Information Casualty v1.7](https://carrados.com/papers/zic-design-standard/), the design standard by Charli-Jo Tyrer and Claude, §3.6, §4.7 and Part Seven. This entry summarises it; the standard is the authority. The sites built to ZIC are checked this way, fetched as a browser, as sent agents, as search and training crawlers, as Googlebot, and as an agent nobody has named, and each receives the same page. See also the [Delivery Casualty](/charlipedia/delivery-casualty/).
