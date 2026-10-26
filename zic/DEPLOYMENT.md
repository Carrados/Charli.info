# Publishing the ZIC migration

Phase one moves the published ZIC material as it stands. The homepage is the existing September 2026 v1.7 specification; its wording, section anchors and Word downloads are unchanged. No checker is included.

## Review and publish in this order

1. Review and merge the `codex/zic-own-site` pull request through the established Claude publishing workflow.
2. Run `npm ci`, `npm run build:zic`, `npm run build:carrados`, `npm run build:charli`, and `node --test tests/zic-migration.test.mjs`.
3. Run `npm run publish:zic` to create/update the `zic-site` branch. Deploy `zic/worker.js` as a new Worker, following the existing Carrados serving setup. It needs no storage, AI or browser bindings.
4. Add zeroinformationcasualty.org to the intended Cloudflare account and configure its DNS/nameservers at IONOS as necessary. Inspect and preserve every existing DNS record, especially mail records; registration stays at IONOS. Attach the apex and www custom domains to the ZIC Worker. Do not buy a separate IONOS hosting or SSL product for this setup.
5. Wait for Cloudflare's certificate and verify the exact HTTPS hostname from an independent client. Confirm `/`, `/index.md`, `/llms.txt`, `/llms-full.txt`, `/robots.txt`, `/sitemap.xml`, `/chunks.json`, both Word downloads, and the 404 response. Verify the www redirect, content negotiation and fragment links. Follow ZIC Part Four delivery checks as actual evidence, not an unqualified conformance claim. Do not switch the old sites until this passes.
6. Keep AI-crawler blocking, managed robots.txt and Browser Integrity Check off for the new zone, consistently with the existing public sites. Check effective responses as a browser, named sent agents, a search crawler, a training crawler, Googlebot and an unnamed client. Simulated user-agent requests are samples, not proof of every real provider's access.
7. Publish Carrados and Charli.info with their normal commands and redeploy their changed Workers. Old Carrados ZIC HTML/Markdown, both Word downloads and the old cover image redirect to the new host. Older charli.info ZIC paper/download paths go directly to the new host. URI fragments stay unchanged, so existing section citations still work. Check redirects before announcing completion.
8. Deploy the changed CharliPedia MCP Worker and existing indexer after `zic-site/chunks.json` is available. Both now read ZIC as a distinct real-world source; the indexer will move existing passages from Carrados to ZIC. Its existing scheduled embedding process is retained; do not add a new scheduled job. Verify semantic search finds the standard at its new URL.
9. Inspect the new homepage at mobile and desktop widths, with keyboard navigation and a screen reader. Styling is copied byte-for-byte from Carrados; no new images were made. Record what was actually checked.

The Tyrer Framework, essays and reports remain on Carrados. CharliPedia summaries remain in CharliPedia; only their source links change. Blind Ant is a separate repository: its existing citations continue working through the Carrados redirects, and can be updated there separately.

Do not run checker tests or create paid AI/browser services as part of this migration. Phase two will implement the agreed 99-attempt persistent allowance and manual owner reset.
