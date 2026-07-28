#!/usr/bin/env python3
"""
relativize_paths.py - convert absolute root paths (href="/x", src="/x") to
relative ones on the site's root-level (depth-0) pages.

Why: the ATS site is served from the domain root, so "/styles/x.css" and
"styles/x.css" resolve to the identical URL in production. But "/styles/x.css"
breaks when a page is opened directly with a file:// URL (the leading slash
points at the filesystem root). Making the paths relative works in BOTH the
file:// preview and when served at the domain root.

Only run this on files that live at the content root (depth 0). All current
site pages that reference assets are depth 0; logbuilder has none.

USAGE
    ./source/relativize_paths.py content/*.html source/templates/*.html

Idempotent: files with no absolute refs are left unchanged.
Stdlib-only.
"""
from __future__ import annotations

import re
import sys

# href="/"  ->  href="index.html"   (bare home link; file:// has no dir index)
HOME = re.compile(r'href="/"')
# (href|src)="/path"  ->  (href|src)="path"   (strip one leading slash;
# the negative lookahead leaves protocol-relative //host untouched).
ROOT = re.compile(r'\b(href|src)="/(?!/)')


def relativize(html: str) -> str:
    html = HOME.sub('href="index.html"', html)
    html = ROOT.sub(r'\1="', html)
    return html


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    changed = 0
    for path in argv:
        with open(path) as f:
            src = f.read()
        out = relativize(src)
        if out != src:
            with open(path, "w") as f:
                f.write(out)
            changed += 1
            print(f"relativized: {path}")
        else:
            print(f"unchanged:   {path}")
    print(f"\n{changed} file(s) changed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        raise SystemExit(130)
