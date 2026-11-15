# ZIC v1.7 requirements, by section

Specification: https://zeroinformationcasualty.org/1.7/

"Must" binds. "Should" recommends and, where adopted and claimed, is checked. "May" permits. Silence means nothing (§1.17).

## Contents

- HTML (§3.1)
- CSS (§3.2)
- Metadata (§3.3)
- Content (§3.4)
- Delivery (§3.5)
- Agent surface (§3.6)
- What is ruled out (§2.2)
- What is left alone (§2.3)

## HTML (§3.1)

- The `html` element declares the page language with `lang`.
- Landmarks are real: `header`, `nav`, `main`, `footer`, with exactly one `main`.
- Exactly one `h1`. No skipped heading levels. Headings describe what follows them.
- The first focusable element is a skip link to `main`. It may be hidden until focused.
- Every `img` has `alt`. Decorative images use `alt=""`. Informative images carry the same information in text.
- Every link's text describes its destination out of context. No "click here" or "read more".
- The current page is marked `aria-current="page"` in navigation, and distinguished by more than colour.
- Every form input has an associated `label`. A placeholder is not a label.
- Tables are for tabular data only, with `th` and `scope`.
- Lists use `ul`, `ol` or `dl`, and only for things that are lists.

## CSS (§3.2)

- Font sizes in `rem`; spacing in `rem` or `em`. No fixed pixel sizes that override the visitor's text size.
- Text stays readable and complete at 200% with no sideways scrolling or lost content (§2.1).
- Contrast: AA by default (4.5:1 normal text, 3:1 large text). Under `prefers-contrast: more`, AAA (7:1 and 4.5:1).
- Respect `prefers-color-scheme`; implement dark mode if a dark variant exists.
- `:focus-visible` is clearly visible on every control. The browser default is acceptable; weakening it is not. Only a landmark focusable through `tabindex="-1"` may suppress its outline.
- Visual reading order matches DOM order. Do not use `order`, absolute positioning or floats to present content in a different sequence.
- Honour `prefers-reduced-motion: reduce`: no non-essential animation.
- Nothing else in CSS is governed.

## Metadata (§3.3)

- A unique, descriptive `title` on every page, in the form "Page Name — Site Name".
- A meta description that is true, useful and unique across the site. No character range.
- Open Graph: at least `og:title`, `og:description`, `og:url`, `og:type`.
- Schema.org JSON-LD on every page: at least `WebSite` on the home page, `WebPage` on content pages, `Person` or `Organization` on about pages.
- The content licence in machine-readable form: the `license` property in the JSON-LD on every page, a readable statement in the footer, and in llms.txt.
- `link rel="canonical"` on every page, pointing at the HTTPS address.
- A valid XML sitemap at `/sitemap.xml`.
- A valid RSS or Atom feed, declared with `link rel="alternate"`, where the site publishes serial content. Where it does not, the accessibility statement says so and commits to adding one if that changes.
- A valid `/robots.txt` as described under Agent surface.

## Content (§3.4)

- Meaning is recoverable from text and structure alone. ZIC does not govern register or vocabulary.
- The structure is evident from the headings alone.
- Dates are unambiguous: ISO 8601 (2026-07-12) or a written form such as 12 July 2026. Never 7/12/26.

## Delivery (§3.5)

- All content is available as static HTML without running JavaScript.
- CSS does not block rendering; JavaScript is deferred or async.
- No external request is needed to deliver content. External requests for presentation, such as a webfont, are the publisher's call.

## Agent surface (§3.6)

- **`/llms.txt` is required.** Markdown in the llmstxt.org form: an H1 with the site name first, a blockquote of one to three sentences, then sections of links with one-line descriptions. It states the site's purpose, author, content licence, sent-agent guarantee, and the separate search and training declarations. Descriptions are specific enough for an agent to route without fetching everything.
- **Markdown mirrors and `/llms-full.txt` are recommended.** Where mirrors exist, llms.txt links both the HTML page and its mirror, never the mirror alone.
- **Generated, not hand-maintained.** llms.txt, llms-full.txt and mirrors come from the same build as the HTML.
- **robots.txt** contains: a mandatory block allowing the named user-directed agents; a search block applied consistently to every known search indexer; a training block decided independently; a stated rule for mixed-use crawlers; and Content Signals stating all three values, with `ai-input=yes`. Comment lines are normative: a welcome says who is served and why, a refusal says what is declined and why.
- As of September 2026 the named agents are: user-directed, ChatGPT-User, Claude-User, Perplexity-User; search, OAI-SearchBot, Claude-SearchBot, PerplexityBot, plus the mixed-use Googlebot, Bingbot and Applebot; training, GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Meta-ExternalAgent. The list changes: check the specification and the vendors' current documentation, and review at least twice a year.
- **No bundled permission.** Changing search does not change training, and neither changes `ai-input`.
- **No contradiction between layers.** robots.txt, llms.txt, the licence, Content Signals, the sitemap, mirrors, any feed, host or CDN configuration and the served pages all agree.
- Agents that drive a real browser cannot be named, and must not be blocked by bot detection on public content.

## What is ruled out (§2.2)

- Information carried by colour, an image, typography, position or whitespace alone.
- Navigation cues that only work visually; unlabelled icons.
- Placeholder link text.
- More than one `h1`, or skipped heading levels.
- Content that needs JavaScript.
- Anti-agent measures on public content: challenges, CAPTCHA walls, blanket AI refusal, CDN or firewall rules blocking user-directed agents, discriminatory rate limits, cloaking. This includes an edge control that blocks an "agent" category, even on advertising pages only, and any rule that penalises a sent agent for delivering a page in full to the person who asked (§1.9).
- Hand-maintained agent surfaces.
- Conformance claims that cannot be checked.

## What is left alone (§2.3, §1.12)

Typeface, palette, imagery, ornament, layout, brand, taste, register, hosting, framework, and the publisher's search and training policy. ZIC also offers no ceiling for cognitive, motor or other access needs it is not qualified to specify (§1.14): it is necessary, not sufficient.
