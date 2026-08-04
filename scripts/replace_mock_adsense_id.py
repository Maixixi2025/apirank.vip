#!/usr/bin/env python3
"""Replace mock ca-pub-xxxxxxxxxxxxxx with real ca-pub-2134598094429002 in all .astro files.
Scope: ONLY data-ad-client attribute value, NO other change.

Verified 2026-08-04 — supports apirank AdSense application (Jazfox applied 8-04 PM).
Run once. If 0 files changed, mock was already replaced."""
import os, sys

MOCK = "ca-pub-xxxxxxxxxxxxxx"
REAL = "ca-pub-2134598094429002"
ROOT = "/root/apirank/src/pages"

count_files = 0
count_replacements = 0
for dirpath, _, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".astro"):
            continue
        path = os.path.join(dirpath, f)
        with open(path) as fh:
            content = fh.read()
        if MOCK not in content:
            continue
        new = content.replace(MOCK, REAL)
        diff_lines = sum(1 for a, b in zip(content.split('\n'), new.split('\n')) if a != b)
        with open(path, 'w') as fh:
            fh.write(new)
        count_files += 1
        count_replacements += diff_lines
        rel = path.replace(ROOT + '/', '')
        print(f"  {rel}: {diff_lines} line(s) changed")

print(f"\nDone: {count_files} files, {count_replacements} line(s) replaced")
