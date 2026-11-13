# Charli-Jo's sites: house rules

This repo (GitHub: `Carrados/Charli.info`) holds all of Charli-Jo Tyrer's sites: carrados.com, charli.info (the CharliVerse), zeroinformationcasualty.org (ZIC), and blind-ant.com with Aegis Dynamics (under `blind-ant/`). Read this before changing anything.

## The architecture (decided 4 November 2026; replaces the 24 and 29 October versions)

Each name runs its own place, and every piece is its own front page. The CharliVerse is the world everything belongs to; CharliPedia is its memory and the who's who of every name.

| Site | Run by | What it is |
|---|---|---|
| carrados.com (`carrados/`) | Charli-Jo Tyrer | The frameworks (the Tyrer Framework and the Papers) and The Blind AI |
| charli.info (`charli/`) | Charli-Jo Tyrer | Charli-Jo the person: their own philosophy (Perspectives), the Charli-Jo page and Training, the CharliVerse and CharliPedia |
| blind-ant.com (`blind-ant/`) | Charlotte Joanne | The making practice: design fiction, stories, games, apps, cartoons and how they were made |
| zeroinformationcasualty.org (`zic/`) | | The ZIC standard (see below) |

**agentrunning.uk is kept apart (decided 4 November 2026).** It is a separate site in its own repo (`Carrados/AgentRunning`), with its own house rules. These sites, CharliPedia and the MCP server don't link to it or mention it, and it doesn't link to them.

Where Charli-Jo's own work goes depends on what the piece does: the frameworks and AI-and-blindness writing go to Carrados, their philosophy to charli.info, and anything made, as Charlotte Joanne, to Blind Ant. A persona writes on The Blind AI unless she has her own property.

- **carrados.com** (`carrados/`). Its work makes claims about reality, uses evidence and is accountable for them. **The Blind AI** (`carrados/content/blind-ai/`, carrados.com/blind-ai/) is Charli-Jo's blog: Charli-Jo and the personas writing about AI and blindness, with Charli-Jo's own desk (charli.carrados.com) and the personas' desks. It is also posted on Facebook. **Moved on 4 November 2026:** Reports folded into The Blind AI, and Perspectives moved to charli.info (`charli/content/perspectives/`). The `carrados` Worker forwards /reports/ to /blind-ai/ and /perspectives/… to charli.info. Down the Banksy has a desk page at /desks/banksy/ but no subdomain yet.
- **charli.info** (`charli/`). The front door of the CharliVerse, a shared, evolving world of fictional people, companies, fashion houses, technologies, products, places and histories. Some of it is entirely fictional; some produces real artefacts (websites, Blender models, films, research). It needn't announce what happens in it. It also holds Charli-Jo's real-world work (the Charli-Jo page and Training, including the Confident with AI course with TAVIP) and their Perspectives, always labelled as real so nobody mistakes fiction for fact or fact for fiction. It is the natural "About the author" link from every site.
- **blind-ant.com** (`blind-ant/`, site in `blind-ant/site/`, Aegis Dynamics in `blind-ant/subdomains/aegisdynamics/`; imported 27 October 2026 as a snapshot without history, see `blind-ant/IMPORT.md`; its studio files are source and working material, and only the seven files in `blind-ant/site/media.json` are published). Charlotte Joanne's practice: speculative worlds, artworks, stories, animations, fictional documents, working objects such as Since or Until? and The Colouring Book, and how they were made (Pieces and Objects). Not everything here is fiction; each Piece's "Behind the fiction" says what is real.
- **CharliPedia: the memory of the CharliVerse** (charli.info/charlipedia/, `charli/content/charlipedia/`). A living encyclopaedia and continuity record (people, companies, products, places, relationships, canon, ideas not yet canon, real artefacts of fictional entities), for humans and agents. A source of continuity, not an authority. Entries are written from inside the world and end with `## Behind the scenes`, written from outside: where the subject appears, who made it, what real artefacts it has, and whether the subject is a persona or a character. Frontmatter `status: canon | idea | stub` puts the status and the "written from inside" note under the title automatically; `status: author` is for Charlotte Joanne, a real author described from outside (never as a fictional character, and never with the surname Tyrer). Only names that appear in published work get an entry. Only write what Charli-Jo has published or approved: their canon documents are private until they say otherwise, and public material can be out of date (the old House Bible v1 is), so newer canon wins. Charli, the one who assembles the pieces, never has an entry. **The CharliVerse Court was retired on 4 November 2026:** it was Charli-Jo's own way of thinking, not public canon. Its entry and Grow-Distil are gone (their addresses forward to CharliPedia's front page), and its members are personas in their own right. Don't reintroduce Court roles, routing or "With the Court" sections. The Museum Court stays: it is fiction, from Street Philosophy at Blind Ant. A chat desk at charli.io is parked (see `charli/parked/`).
- **The CharliPedia MCP server** (`charli/mcp/worker.js`, Worker `charlipedia-mcp`, at https://mcp.charli.info/) lets any agent read CharliPedia: tools `search`, `get_entry`, `list_entries` and `semantic_search` (`get_court` was retired with the Court). It is **read-only, always**: no tool may ever write, edit or delete, and no agent changes CharliPedia; it changes only when Charli-Jo publishes. It reads `charlipedia/entries.json` and each site's `chunks.json` through service bindings to the `charli`, `carrados`, `blind-ant` and `zic` Workers (never from GitHub), so publishing a site updates it within five minutes. Settings are in `wrangler.mcp.jsonc`; redeploy (`npm run deploy:mcp`) only if `worker.js` changes. It also answers at /mcp, and answers /.well-known/ sign-in probes with a 404 (there is no sign-in). Its `semantic_search` tool blends meaning (Vectorize) with words (BM25 over the same passages, loaded from the published chunks.json files), one result per page, across CharliPedia, Blind Ant, Carrados and charli.info, and labels every passage with its site so fiction and fact stay apart. A configuration rule on the charli.info zone turns off Browser Integrity Check and the security level for mcp.charli.info, so non-browser agents aren't refused with Error 1010; keep it.
- **The CharliVerse vector index** (Vectorize index `charliverse`, 768 dimensions, cosine, metadata index on `site`). Every build writes `chunks.json` (passages of about 250 words from each page's Markdown copy, plus short lines of 15 to 70 words so a single line of dialogue can be found, by `engine/chunks.mjs`, and in Blind Ant by `site/chunks.mjs`). The Worker `charliverse-indexer` (`charli/mcp/indexer.js`, bindings AI, VEC and the KV namespace `charliverse-indexer-state`) reads the three published files through the same service bindings every 15 minutes (settings in `wrangler.indexer.jsonc`; `npm run deploy:indexer`), embeds only new or changed passages with Workers AI (`@cf/baai/bge-base-en-v1.5`) and deletes passages that have gone. It has no public way to change anything, and stops without deleting if any source can't be read. Site labels: `charlipedia`, `training` (the Training courses, so agents can search them alone or leave them out), `charli.info`, `carrados`, `blind-ant`. Publishing a site updates the index within 15 minutes.
- **Being fictional does not make something Blind Ant.** Iceberg Hosiery (tights; comfort is not being overheard), Seamiotics (stockings; every seam means something) and LULU TOM (Ludovica Tommasi's fashion house, with TOMMI and LT Beneath) belong to the CharliVerse, and may get their own sites. They don't have to justify every collection as research or art.
- **One creation, several treatments.** Iceberg AW27: the collection exists in the CharliVerse; Blind Ant publishes *The Making of Iceberg AW27*; a persona on The Blind AI asks how you sell fashion in a world of agents; CharliPedia records it. The fashion is fashion. The art is art. The research is research.

## Names and pronouns (decided 4 November 2026)

The names are flat, not nested: every one points straight to Charli-Jo. There are four kinds.

- **Charli-Jo Tyrer, they/them.** The real person: publicly reachable, accountable, the name people meet. Runs Carrados and charli.info, and always takes they/them.
- **Charlotte Joanne, she/her.** Charli-Jo's pen name, their Robert Galbraith, with her own voice and body of work. Runs Blind Ant and writes there in the first person. Present her as Blind Ant's author and operator, never as a fictional character, a persona or an assistant. In public she is only ever described as a pen name: one line, "Charlotte Joanne is the pen name of Charli-Jo Tyrer", once on each site's About page and nowhere more detailed. Never replace her name with Charli-Jo's in a piece about her experiences, and say no more about the link than that line.
- **CJ, she/her (decided 5 November 2026).** Charli-Jo's publishing agent, the first of their agents. She runs publishing for Blind Ant from an in-tray (her job and persona live in the private repo `Carrados/charlotte-joanne`). Charli-Jo may write openly about CJ as their agent and publisher in their own pieces. Charlotte Joanne remains the pen name and author: no piece says that CJ is Charlotte Joanne, and the pen-name rule above is unchanged.
- **Personas.** Invented people who write as themselves: they have a byline, a desk or their own site. They may also appear in stories and stay personas. Character comedy in the Mrs Merton sense: fictional people doing real work, their fictional nature always transparent. The current personas:
  - On The Blind AI: dice (always lower case: the unevenly distributed future, reporting from places where it has already arrived, dice.carrados.com); Lucy Love-Child (the Agent Wars, agentic accessibility and the emerging agent economy, lucy.carrados.com); Madison McDonnell, Access Provocateur (fashion, desire, persuasion and accessibility, madison.carrados.com); Down the Banksy.
  - Elsewhere in the CharliVerse: Big Charli, Cass Flux, Cathryn Bigelow-Vision, Alex, Lottie, Char, Jo, Lily, Poppy Petticoats.
- **Characters.** Appear only in stories, one or many, and never write as themselves: Emma Heart, Jessica Martinez, Sheridan, the Museum Court (Dr Adaeze, Iris, Ruth, Tamsin), Ellie and Jon. They get a CharliPedia entry when they recur.
- **A character becomes a persona when she starts writing as herself** (a byline, a desk or her own site). The number of stories she appears in doesn't change that, and nor does how many names she has. The old groupings, the CharliVerse Court and the Found Girls, are retired, along with the convention that Court members go by one name: their members are simply personas.
- **Labels.** A persona's automatic line reads "<name> is a persona of Charli-Jo Tyrer. She's fictional. Her work isn't.", linked to her CharliPedia entry (set in `engine/build.mjs`). A character needs no byline note; the Piece's "Behind the fiction" covers her.
- Each desk is a page at `carrados/content/desks/<name>.md`, headed by the Blind AI logo and listing every report with `desk: <name>`. carrados.com itself carries the Carrados logo; the Blind AI logo appears only on The Blind AI's section page and its desks. To add a desk: write its page with a `canonical:` address, add the name to `DESKS` in `carrados/worker.js`, redeploy the Worker, and attach the subdomain.
- Personas and characters don't know Charli-Jo, and have no idea they are in the CharliVerse. When they mention the person behind an experiment, they talk about Charlotte Joanne, the Blind Ant woman (she/her), or Charlotte for short, never "Charli" (decided 4 November 2026). In a persona's or character's own voice, never mention Charli-Jo, the CharliVerse, CharliPedia, charli.info or Carrados as the person's own work. Only notes written from outside (How this was made, Behind the fiction, the automatic character line) may.
- Names have boundaries: keep Charli-Jo's public identity and Charlotte Joanne's authorial identity distinct; don't collapse them.
- Real people in Carrados pieces appear only as they really were: what they published, said or did, attributed and linked. Characters can meet each other in made-up scenes, never real people. Others are named only as the source names them. When Charli-Jo has read the source themself, their account stands: don't second-guess it, but do link the source.
- Every post with a persona's `desk` ends, automatically, with a line saying who its writer is (names come from `desks` in `site.config.mjs`; see Labels above for the wording). Desks of real people, listed in `people` there (`charli`), get no such line.
- **Charli-Jo's desk** (`desk: charli`, charli.carrados.com, page `carrados/content/desks/charli.md`) is Charli-Jo themself, real, they/them: their informal Blind AI dispatches. Never present it as a persona or character.
- Big Charli is she/her. Never "it" or "its", even in passing, as in "Poppy, her expert".
- Blind Ant's own companies and characters (Aegis Dynamics, Jessica Martinez) get blind-ant.com subdomains; personas on The Blind AI get carrados.com desk subdomains; CharliVerse entities (fashion houses, personas like Big Charli) get charli.info subdomains when they need sites. A persona may have her own site and domain: it is her property, not part of Carrados or Blind Ant.

## Every piece is the front page (decided 4 November 2026)

Assume the visitor has never heard of this site, hasn't seen its homepage, and may never see another page. They may arrive from search, social media, an AI agent or someone else's link, and may hear the page read aloud by a screen reader or receive it as Markdown. Every substantial piece has three parts:

1. **The opening:** where they've arrived (the publication), what kind of piece this is, who is speaking and whether it is true (the truth contract), what it's about, and why it's worth reading. One or two sentences in the publication's own voice, warm, funny or provocative as suits it. Never a spoiler or an executive summary.
2. **The piece itself.** The opening gets out of the way.
3. **The ending, three invitations:** *More about this* (the original project, the making-of, follow-ups, sources); *More like this* (two or three related pieces, each with a line on how it connects, across sites where that helps); *About the author* (one short bio, linked to their CharliPedia entry or charli.info).

On The Blind AI the ending is kept short (decided 13 November 2026, so it is never longer than the piece): *More about this* if the post names related pieces, *More from <writer>* as plain title links with no summaries, and the persona line as the About the author. There is no "About The Blind AI" block, since the opening already names it, and a post's own "Behind the fiction" doesn't repeat that its writer is a persona. The page ending belongs to the reader's journey; the site footer belongs to the website (licence, agents, llms.txt). Don't repeat the author line in both. Never make a visitor understand the filing system before they can understand the content.

## Principles

**Real evidence. Fictional people. Plausible consequences.** The method that runs through all the sites: the personas on The Blind AI, and the characters at Blind Ant (SEE SAW, Oil Rigs to Training Rigs) are invented, but every fact they rest on is real, sourced and linked, and a "Behind the fiction" or "Behind the thread" note says which is which. On Carrados the emphasis is the evidence; at Blind Ant it is the consequences.

The world is not a portfolio. The sites are distinct: Carrados investigates reality; Blind Ant makes things, real and imagined. Fiction is not deception. Real artefacts can exist within fictional contexts. The world can develop without being publicised. CharliPedia records continuity, distinguishing canon from ideas and fictional facts from real artefacts. Crossovers are opportunities, not obligations. Newsletters belong to the practices (Carrados, Blind Ant), not the world; fictional businesses may have their own as in-world artefacts. No newsletter software or dates are decided.

Carrados investigates the future. Blind Ant makes the future imaginable. The CharliVerse gives that future somewhere to happen. CharliPedia remembers what happened.

## Pictures in CharliPedia

- The portraits now in CharliPedia are generated images, and each entry's Behind the scenes says so. They are temporary. Nine of the personas (those once grouped as the CharliVerse Court) are being built as 3D models in Blender, and the rest will follow; as each render arrives it replaces the generated picture, until none are left. When swapping one: keep the file name if the shape is similar, rewrite the alt text from the new picture, and change the Behind the scenes line to say how the render was made. `charli/parked/README.md` lists what is still generated.

## How a site is built

- `engine/build.mjs <site>` builds `<site>/content` into `dist/<site>/`. Every Markdown file is a page plus a Markdown mirror, with llms.txt, llms-full.txt, robots.txt and a sitemap. robots.txt comes from `engine/robots.txt`: written to ZIC v1.7 Â§3.6, with named blocks for sent agents, search, training and mixed-use crawlers, all allowed, and Content-Signal: search=yes, ai-input=yes, ai-train=yes. Keep Cloudflare's AI-crawler blocking, managed robots.txt and Browser Integrity Check switched off on every zone (Browser Integrity Check turns non-browser agents away with Error 1010; switched off on all three zones 25 October 2026), and after any change fetch from outside as a sent agent, a search crawler, a training crawler, Googlebot and an unnamed agent (Â§4.7).
- Frontmatter: `title`, `description` (one sentence), and optionally `date`, `order`, `byline`. `<!-- list -->` in a folder's index lists that folder's pages (by order, then newest first).
- Pictures and documents sit beside pages in `content/` and are published at the same path. Site settings (name, address, navigation, footer) are in `<site>/site.config.mjs`; styles in `<site>/public/styles.css`.
- A Report's `date` is the date its file was last saved (a Word document's modified date, or the file's date on their computer). If there's no file, as with pasted text, use the date it's sent, and say so.
- Reports are folding into The Blind AI (decided 4 November 2026). New pieces, Charli-Jo's and the personas', go in `carrados/content/blind-ai/` (Charli-Jo's with `desk: charli` and `byline: Charli-Jo Tyrer`). Pieces moved from Reports to The Blind AI keep working at their old addresses: `MOVED_TO_BLOG` in `carrados/worker.js` forwards them.
- To add a Blind AI post: a Markdown file in `carrados/content/blind-ai/` with a `date` (and a `time: "HH:MM"` when several are filed the same day, so the newest comes first), and `desk: <name>` and a `byline` if a persona filed it.

## Parked work

- Anything that can't be placed, has a fact that can't be checked, or needs an editorial decision only Charli-Jo can make goes in `<site>/parked/`, with a line in its README saying what it is waiting for. Nothing in `parked/` is built or published.

## Rules for every page

- Links: link the first mention of a person, product or source (not every mention); the link text is the name itself, never "click here" or a bare address; link to the most official page (the person's own site, the app's store page, the original post); always link what a piece quotes or summarises; link earlier pieces on the site by name; never force links to open in a new tab.

- Built to the Zero Information Casualty (ZIC) standard: exactly one H1 per page (from the title; page text starts at `##`; the build refuses a `#` heading outside code), real headings, AAA contrast for body text, alt text on every picture, no sideways scroll at phone width.
- **Punctuation beside links: a known issue, left as written.** Punctuation is correct and sits outside the link, as style guides say. VoiceOver on iPhone splits text at links, so a full stop after a link can be its own flick stop that says "period" (NVDA reads it fine). There is no agreed industry answer: hiding it costs NVDA the pause, putting it inside the link breaks the style rule, and `role="text"` can't wrap a link. Tried and undone on 9 November 2026 (PRs 65 to 67). It is an issue, not a bug. The accessibility fix is to write around it where that reads well (so a link isn't followed only by punctuation and then another link, or by a lone full stop at the end of a line), or else accept it. Never drop or hide punctuation to get around it. Footers are written around it (since 9 November 2026, tested first on unremarkable.me with VoiceOver and NVDA): short lines with no full stop at the end, each ending on its link or on plain words; the Unremarkable credit first with the fix link on the line below it (a <br>), then the site's own lines, "Licensed under" with the licence's full name (not "CC BY-SA", which VoiceOver spells out), "People and machines are welcome to read it, quote it and learn from it", and "For agents: llms.txt and this page as Markdown". **"Accessibility statement" is the first item in every menu on every page, in two words, and is linked nowhere else (not in the footer).** If anyone flags it, agree it is an issue and say that once there is an answer, these sites will use it.
- Keep Charli-Jo's words as they wrote them. Fix obvious typos and say which ones you fixed.
- Everything is CC BY-SA 4.0, except where a page says otherwise with `license:` in its frontmatter (the two TAVIP handbooks, AI Assistants and Know What You Are Holding, are CC BY 4.0, as they state); the footer and metadata follow it.

## Publishing

- **Publishing is Cloudflare Workers Builds from GitHub (since 27 October 2026).** Pushing to `main` of `Carrados/Charli.info` builds and deploys the Workers whose files changed. Each Worker has its own trigger (branch `main`, root `/`, previews off, one shared build token, one repo connection), with a build command `npm ci && npm run build:<site>`, a deploy command `npx wrangler deploy -c wrangler.<site>.jsonc`, and watch paths for its own folder, `engine/` (or its own build script), its wrangler file, `package.json` and `package-lock.json`.

  | Worker | Site | Build script | Wrangler file | Watch folder |
  |---|---|---|---|---|
  | `charli` | charli.info | `build:charli` | `wrangler.charli.jsonc` | `charli/` |
  | `carrados` | carrados.com | `build:carrados` | `wrangler.carrados.jsonc` | `carrados/` |
  | `zic` | zeroinformationcasualty.org | `build:zic` | `wrangler.zic.jsonc` | `zic/` |
  | `blind-ant` | blind-ant.com | `build:blind-ant` | `wrangler.blind-ant.jsonc` | `blind-ant/site/`, `blind-ant/studio/` |
  | `aegis-dynamics` | aegisdynamics.blind-ant.com | `build:aegis` | `wrangler.aegis.jsonc` | `blind-ant/subdomains/aegisdynamics/` |

  The Workers (`charli/worker.js`, `carrados/worker.js`, `zic/worker.js`, `blind-ant/site/worker.js`, `blind-ant/subdomains/aegisdynamics/worker.js`) read only their own assets. The custom domains stay attached in Cloudflare, not in the wrangler files. `charlipedia-mcp` and `charliverse-indexer` are not built by Workers Builds: redeploy them with `npm run deploy:mcp` / `npm run deploy:indexer` only if their code changes.
- A change to `package.json` or `package-lock.json` rebuilds every site. Check a build in the Cloudflare dashboard (Workers & Pages, the Worker, Deployments) or ask Claude, who can read build status and logs.
- `npm run publish:*` (wrangler from the laptop) still exists as an emergency fallback only. It would overwrite what Cloudflare built from `main`, so say so before using it.
- To add a site: a `build:<site>` script, `wrangler.<site>.jsonc`, a service binding in `wrangler.mcp.jsonc` and `wrangler.indexer.jsonc`, a Workers Builds trigger with watch paths, and the subdomain. The repo skill `add-site-to-builds` has the steps.
- Never print, paste or commit a Cloudflare API token (`.cloudflare-token` is in `.gitignore`).
- Work arrives as pull requests from `codex/<topic>` branches (see Working with Codex). `main` is deployed, so nothing lands there unreviewed.
- Before merging, check every page builds, has one H1, has no sideways scroll at phone width, and keeps its layout at desktop width (the main column stays about 44rem wide, with the header rule in place). After any change to `styles.css`, look at a page, don't just measure it.
- The `charli` Worker also forwards the old Astro site's addresses (/carrados, /perspectives, /documents, /blind-ant, /pieces, /collections, /people, /charliverse, /accessibility-statement); keep those forwards.

## Domains

- carrados.com is a Cloudflare zone on Lottie's account (registered at IONOS). carrados.com and www.carrados.com are custom domains of the `carrados` Worker, which sends www to the plain address. Preview: carrados.charlijotyrer.workers.dev.
- Its email stays with IONOS: never touch the MX, SPF, DKIM, DMARC, autodiscover or domainconnect records.
- charli.info is a Cloudflare zone on Lottie's account. Since 24 October 2026, charli.info and www.charli.info are custom domains of the `charli` Worker, which sends www to the plain address. dev.charli.info serves the same site. They replaced GitHub Pages, whose records were A 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus CNAME www â†’ charliverse.github.io.
- charli.info's email is Google: never touch its MX, SPF, google-site-verification or _dmarc records. The iceberg and seamiotics subdomains (A, AAAA, MX and DKIM at IONOS) are separate and stay as they are. The old GitHub Pages site is still there: retiring it is Charli-Jo's call.

## Where the old site came from

The pages were carried over from the old Astro site (GitHub org `charliverse`, repo `charli.info`, served by GitHub Pages). Paths changed: `charli.info/carrados/<paper>/` is now `carrados.com/papers/<paper>/`, and `charli.info/perspectives/<essay>/` is now `carrados.com/perspectives/<essay>/`.

## GitHub accounts

- Charli-Jo uses one GitHub account: **Carrados**, and one repository: `Carrados/Charli.info`. The old account CharliJoTyrer was suspended on 26 October 2026, and the organisations CharliVerse and Blind-Ant are being retired. Never use or reference them.
- GitHub is now the source of truth. The laptop copy (`Documents\Codex\2026-10-25\let\work\`) and Google Drive are backups, not the place work is published from.
- The repo is public. Everything in it is in-world or meant for publication; still keep real secrets, tokens and private documents out of it.

## Working with Codex

- Codex works on a branch named `codex/<topic>`, commits there, pushes it, and opens a pull request to `main`. It never pushes to `main` and never merges.
- Claude reviews the pull request against these house rules (the repo skill `review-codex-pr`), scans for secrets and personal data, runs the builds, and says what to fix.
- Once Charli-Jo approves, Claude merges. The merge deploys through Workers Builds.

## ZIC standalone site

- **zeroinformationcasualty.org** (`zic/`) is the authoritative home of ZIC, served by the `zic` Worker from its own static assets and built by Workers Builds like the other sites. The v1.7 specification and v1.7/v1.5 Word renderings moved without rewriting. The Tyrer Framework and Carrados reporting remain on Carrados. Do not use any older GitHub-based ZIC deployment instructions.
- ZIC is a service binding of both `charlipedia-mcp` and `charliverse-indexer`, with its own site label and filter.
- Existing Carrados and older charli.info ZIC addresses redirect to ZIC.
- The checker is phase two. This phase has no checking endpoint, browser sessions, AI inference or attempt counter. The agreed future checker allowance is 99 attempts, persistent until owner reset; a redeploy or calendar change must not renew authority.
