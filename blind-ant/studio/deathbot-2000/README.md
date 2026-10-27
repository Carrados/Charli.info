# DeathBot 2000: studio files

- `originals/`: Charlotte Joanne's Word documents. `06` and `08` have v2 versions (the passed revisions, used on the site); `07` is the continuity-fixed version.
- `cover/cover.py`: draws the cover as SVG (`python3 cover.py OUTDIR`). It turns text into paths using fonts from npm @fontsource (bebas-neue, oswald, ibm-plex-mono, permanent-marker) and EB Garamond; edit the paths in `FONTS` to where they're unpacked.
- `cover/render.js`: renders an SVG to PNG at 2x with Playwright (`node render.js in.svg out.png 1600 2400`).

The old Gemini cover is deliberately not kept here: the site uses no generated images.
