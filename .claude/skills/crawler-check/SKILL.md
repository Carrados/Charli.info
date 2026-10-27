---
name: crawler-check
description: After any change to robots.txt, Cloudflare bot settings or a zone, fetch each site as a sent agent, a search crawler, a training crawler, Googlebot and an unnamed agent (ZIC section 4.7) and report the responses. Use after such a change or when an agent reports Error 1010.
---

# Crawler check

Rules from `CLAUDE.md`: `engine/robots.txt` allows all five crawler classes with `Content-Signal: search=yes, ai-input=yes, ai-train=yes`. Cloudflare's AI-crawler blocking, managed robots.txt and Browser Integrity Check stay OFF on every zone (Browser Integrity Check causes Error 1010 for non-browser agents). `mcp.charli.info` has a configuration rule that turns off Browser Integrity Check and the security level; keep it.

For each of https://charli.info/, https://carrados.com/, https://zeroinformationcasualty.org/, https://blind-ant.com/ and https://mcp.charli.info/ fetch `/`, `/robots.txt`, `/llms.txt` and `/sitemap.xml` with these User-Agents and report status code and any Cloudflare error code:

- a sent agent (for example `ChatGPT-User`, `Claude-User`)
- a search crawler (`OAI-SearchBot`, `Claude-SearchBot`)
- a training crawler (`GPTBot`, `ClaudeBot`)
- Googlebot (`Googlebot/2.1`)
- an unnamed agent (`curl/8`, no User-Agent)

All should return 200, with robots.txt matching `engine/robots.txt`. A 403 or Error 1010 means a Cloudflare setting has been switched back on: say which zone, and do not change zone settings without Charli-Jo's approval. If this environment cannot reach the live sites (it often cannot), say so and give Charli-Jo the list of URLs and agents to try, rather than claiming a pass.
