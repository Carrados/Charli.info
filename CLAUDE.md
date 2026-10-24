# Charli-Jo's sites: house rules

This repo holds Charli-Jo Tyrer's sites outside Blind Ant: carrados.com and charli.info (the CharliVerse). Read this before changing anything.

## The architecture (decided 24 October 2026)

The CharliVerse is the world. Carrados and Blind Ant are practices. CharliPedia is the memory of the world. "I create worlds to inhabit, where a thing happens." This is a decision about the nature of the work, not just the websites: the CharliVerse can grow without everything having to become a research project or an artwork.

- **charli.info: the CharliVerse** (`charli/`). The front door of a shared, evolving world of fictional people, companies, fashion houses, technologies, products, places and histories. Some of it is entirely fictional; some produces real artefacts (websites, Blender models, films, research). It is a world, not an editorial practice, and needn't announce what happens in it. It also holds Charli-Jo's real-world work (the Charli-Jo page and Training, including the Confident with AI course with TAVIP), always labelled as real so nobody mistakes fiction for fact or fact for fiction.
- **carrados.com: design non-fiction** (`carrados/`). The real-world exploration, investigation and research practice: emerging AI, accessibility, agentic systems, human-AI collaboration. Its work makes claims about reality, uses evidence and is accountable for them. Sections: Reports (the posts of The Blind AI), Papers, Perspectives.
- **blind-ant.com: design fiction** (repo CharliJoTyrer/Blind-Ant). An independent artistic practice authored and operated by Charlotte Joanne: speculative worlds, artworks, stories, animations, fictional documents, and how they were made (Pieces and Objects).
- **CharliPedia: the memory of the CharliVerse** (charli.info/charlipedia/, `charli/content/charlipedia/`). A living encyclopaedia and continuity record (people, companies, products, places, relationships, canon, ideas not yet canon, real artefacts of fictional entities), for humans and agents. A source of continuity, not an authority. Entries are written from inside the world and end with `## Behind the scenes`, written from outside: where the subject appears, who made it, what real artefacts it has. Frontmatter `status: canon | idea | stub` puts the status and the "written from inside" note under the title automatically. Only write what Charli-Jo has published or approved: her canon documents are private until she says otherwise, and public material can be out of date (the old House Bible v1 is), so newer canon wins. Charli, the one who assembles the pieces, never has an entry. A chat desk at charli.io is parked (see `charli/parked/`).
- **Being fictional does not make something Blind Ant.** Iceberg (intentionwear hosiery), Seamiotics (the cultural language of stockings) and LULU TOM (Ludovica Tommasi's fashion house, with TOMMI and LT Beneath) belong to the CharliVerse, and may get their own sites. They don't have to justify every collection as research or art.
- **One creation, several treatments.** Iceberg AW27: the collection exists in the CharliVerse; Blind Ant publishes *The Making of Iceberg AW27*; a Carrados correspondent asks how you sell fashion in a world of agents; CharliPedia records it. The fashion is fashion. The art is art. The research is research.

## Identities and pronouns

- **Charli-Jo Tyrer, they/them.** Carrados's founder and principal practitioner: real, publicly reachable, accountable. Carrados always uses they/them for Charli-Jo. Charli-Jo speaks as Carrados.
- **Charlotte Joanne, she/her.** The female authorial identity who writes and runs Blind Ant: Charli-Jo's Robert Galbraith, a pseudonym with her own voice and body of work. Present her as Blind Ant's author and operator, not as a fictional character or an assistant. Blind Ant pieces needn't explain the link to Charli-Jo.
- **The correspondents** speak for Carrados, character comedy in the Mrs Merton sense: fictional people doing real work, and their fictional nature stays transparent.
  - dice (always lower case, as in the Found Girls canon): the unevenly distributed future, reporting from places where it has already arrived. dice.carrados.com
  - Lucy Love-Child: the Agent Wars, agentic accessibility and the emerging agent economy, for The Blind AI. lucy.carrados.com
  - Madison McDonnell, Access Provocateur: fashion, desire, persuasion and accessibility. madison.carrados.com
- Each desk is a page at `carrados/content/desks/<name>.md`, headed by the Blind AI logo and listing every report with `desk: <name>`. carrados.com itself carries the Carrados logo, never the Blind AI one. To add a desk: write its page with a `canonical:` address, add the name to `DESKS` in `carrados/worker.js`, redeploy the Worker, and attach the subdomain.
- The characters don't know Charli-Jo. When they mention the person behind an experiment, they talk about Charlotte Joanne, the Blind Ant woman (she/her), and may call her Charli for short. Leave those mentions as written.
- Identities have boundaries: keep Charli-Jo's public identity and Charlotte Joanne's authorial identity distinct; don't collapse them.
- Real people in Carrados pieces appear only as they really were: what they published, said or did, attributed and linked. Characters can meet each other in made-up scenes, never real people. Others are named only as the source names them. When Charli-Jo has read the source themself, their account stands: don't second-guess it, but do link the source.
- Every report with a `desk` ends, automatically, with a line saying its writer is a character who speaks for Carrados (names come from `desks` in `site.config.mjs`).
- Blind Ant's own companies and characters (Aegis Dynamics, Jessica Martinez) get blind-ant.com subdomains; correspondents get carrados.com subdomains; CharliVerse entities (fashion houses, personas like Big Charli) get charli.info subdomains when they need sites.

## Principles

The world is not a portfolio. The practices are distinct: Carrados investigates reality; Blind Ant creates design fiction. Fiction is not deception. Real artefacts can exist within fictional contexts. The world can develop without being publicised. CharliPedia records continuity, distinguishing canon from ideas and fictional facts from real artefacts. Crossovers are opportunities, not obligations. Newsletters belong to the practices (Carrados, Blind Ant), not the world; fictional businesses may have their own as in-world artefacts. No newsletter software or dates are decided.

Carrados investigates the future. Blind Ant makes the future imaginable. The CharliVerse gives that future somewhere to happen. CharliPedia remembers what happened.

## How a site is built

- `engine/build.mjs <site>` builds `<site>/content` into `dist/<site>/`. Every Markdown file is a page plus a Markdown mirror, with llms.txt, llms-full.txt, robots.txt and a sitemap. robots.txt comes from `engine/robots.txt`: written to ZIC v1.7 §3.6, with named blocks for sent agents, search, training and mixed-use crawlers, all allowed, and Content-Signal: search=yes, ai-input=yes, ai-train=yes. Keep Cloudflare's AI-crawler blocking and managed robots.txt switched off on every zone, and after any change fetch from outside as a sent agent, a search crawler, a training crawler, Googlebot and an unnamed agent (§4.7).
- Frontmatter: `title`, `description` (one sentence), and optionally `date`, `order`, `byline`. `<!-- list -->` in a folder's index lists that folder's pages (by order, then newest first).
- Pictures and documents sit beside pages in `content/` and are published at the same path. Site settings (name, address, navigation, footer) are in `<site>/site.config.mjs`; styles in `<site>/public/styles.css`.
- A Report's `date` is the date its file was last saved (a Word document's modified date, or the file's date on their computer). If there's no file, as with pasted text, use the date it's sent, and say so.
- To add a Report: a Markdown file in `carrados/content/reports/` with a `date`, and `desk: <name>` and a `byline` if a character filed it.

## Parked work

- Anything that can't be placed, has a fact that can't be checked, or needs an editorial decision only Charli-Jo can make goes in `<site>/parked/`, with a line in its README saying what it is waiting for. Nothing in `parked/` is built or published.

## Rules for every page

- Links: link the first mention of a person, product or source (not every mention); the link text is the name itself, never "click here" or a bare address; link to the most official page (the person's own site, the app's store page, the original post); always link what a piece quotes or summarises; link earlier pieces on the site by name; never force links to open in a new tab.

- Built to the Zero Information Casualty (ZIC) standard: exactly one H1 per page (from the title; page text starts at `##`; the build refuses a `#` heading outside code), real headings, AAA contrast for body text, alt text on every picture, no sideways scroll at phone width.
- Keep Charli-Jo's words as they wrote them. Fix obvious typos and say which ones you fixed.
- Everything is CC BY-SA 4.0.

## Publishing

- `npm install`, then `npm run publish:carrados` builds and pushes `dist/carrados/` to the `carrados-site` branch. The Cloudflare Worker `carrados` (`carrados/worker.js`) serves that branch. Commit the source to `main` too.
- The Worker reads the branch from raw.githubusercontent.com, which only works while this repo is public.
- `carrados/worker.js` only needs redeploying to Cloudflare if the serving rules change.
- Before publishing, check every page builds, has one H1, has no sideways scroll at phone width, and keeps its layout at desktop width (the main column stays about 44rem wide, with the header rule in place). After any change to `styles.css`, look at a page, don't just measure it.

- charli.info: `npm run publish:charli` builds and pushes `dist/charli/` to the `charli-site` branch, served by the Worker `charli` (`charli/worker.js`). That Worker also forwards the old Astro site's addresses (/carrados, /perspectives, /documents, /blind-ant, /pieces, /collections, /people, /charliverse, /accessibility-statement); keep those forwards.

## Domains

- carrados.com is a Cloudflare zone on Lottie's account (registered at IONOS). carrados.com and www.carrados.com are custom domains of the `carrados` Worker, which sends www to the plain address. Preview: carrados.charlijotyrer.workers.dev.
- Its email stays with IONOS: never touch the MX, SPF, DKIM, DMARC, autodiscover or domainconnect records.
- charli.info is a Cloudflare zone on Lottie's account. Since 24 October 2026, charli.info and www.charli.info are custom domains of the `charli` Worker, which sends www to the plain address. dev.charli.info serves the same site. They replaced GitHub Pages, whose records were A 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, plus CNAME www → charliverse.github.io.
- charli.info's email is Google: never touch its MX, SPF, google-site-verification or _dmarc records. The iceberg and seamiotics subdomains (A, AAAA, MX and DKIM at IONOS) are separate and stay as they are. The old GitHub Pages site (charliverse/charli.info) is still there: retiring it is Charli-Jo's call.

## Where the old site came from

The pages were carried over from the old Astro site (GitHub org `charliverse`, repo `charli.info`, served by GitHub Pages at charli.info until the new charli.info replaces it). Paths changed: `charli.info/carrados/<paper>/` is now `carrados.com/papers/<paper>/`, and `charli.info/perspectives/<essay>/` is now `carrados.com/perspectives/<essay>/`.
