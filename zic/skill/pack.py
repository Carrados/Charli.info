#!/usr/bin/env python3
"""Pack the ZIC skill folder into the download on zeroinformationcasualty.org.

  python3 zic/skill/pack.py           writes zic/content/documents/zic-1-7-skill.zip
  python3 zic/skill/pack.py --check   exits 1 if the download is out of date with the folder

The zip is deterministic (sorted names, fixed dates), so the same folder always gives the same file.
Run it after any change to zic/skill/zic-1-7/ and commit the result: the site serves the committed zip.
"""
import io, sys, zipfile
from pathlib import Path

here = Path(__file__).resolve().parent
src = here / 'zic-1-7'
out = here.parent / 'content' / 'documents' / 'zic-1-7-skill.zip'

def build() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in src.rglob('*') if p.is_file()):
            info = zipfile.ZipInfo('zic-1-7/' + f.relative_to(src).as_posix(), date_time=(2026, 11, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, f.read_bytes())
    return buf.getvalue()

data = build()
if '--check' in sys.argv:
    ok = out.exists() and out.read_bytes() == data
    print('zic-1-7-skill.zip is up to date' if ok else 'zic-1-7-skill.zip is OUT OF DATE: run python3 zic/skill/pack.py')
    sys.exit(0 if ok else 1)
out.write_bytes(data)
print(f'wrote {out.relative_to(here.parent.parent)} ({len(data)} bytes)')
