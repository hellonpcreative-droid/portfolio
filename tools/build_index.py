#!/usr/bin/env python3
"""Regenerates the project tiles + gallery data of index.html from the photos/ folder.

Usage (from the repo root):   python tools/build_index.py
Rules:
  photos/<category>/<group>/<series>/*.webp   ->  one tile per <series>, gallery = its photos
  photos/<category>/<series>/*.webp           ->  same, without a <group>
  Sub-folders inside a series are flattened into that series.
  Optional: a file named cover.webp in a series folder is used as the tile cover
  (otherwise the first photo, in natural order).
Category folder names: architecture / fashion / wedding (add more in CATEGORIES below).
"""
import html, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# folder name -> (type shown in header nav, order)
CATEGORIES = {'architecture': 'personal', 'fashion': 'commercial', 'wedding': 'commercial'}

def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def clean(name):
    name = re.sub(r'^(EXPORT|MARIAGE)\s+', '', name, flags=re.I)
    name = re.sub(r'^D[ée]fil[ée]\s+', '', name, flags=re.I)
    return name.strip()

series = []
photos_dir = os.path.join(ROOT, 'photos')
for cat, typ in CATEGORIES.items():
    cdir = os.path.join(photos_dir, cat)
    if not os.path.isdir(cdir):
        continue
    def walk_series(path, labels):
        subdirs = sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))], key=natural)
        direct = [f for f in os.listdir(path) if f.lower().endswith('.webp')]
        return subdirs, direct
    for first in sorted(os.listdir(cdir), key=natural):
        p1 = os.path.join(cdir, first)
        if not os.path.isdir(p1):
            continue
        subdirs, direct = walk_series(p1, [first])
        # a "group" folder (EUROTRIP, LAB DESIGN WEEK) holds series whose own folders hold photos
        is_group = bool(subdirs) and not direct and any(
            any(f.lower().endswith('.webp') for _, _, fs in os.walk(os.path.join(p1, d)) for f in fs) for d in subdirs)
        # a group whose children are each a series -> children are series; otherwise `first` is the series
        if is_group:
            candidates = [(first, d, os.path.join(p1, d)) for d in subdirs]
        else:
            candidates = [(None, first, p1)]
        for group, name, spath in candidates:
            files = []
            for dp, _, fs in os.walk(spath):
                for f in fs:
                    if f.lower().endswith('.webp'):
                        rel = os.path.relpath(os.path.join(dp, f), spath).replace(os.sep, '/')
                        files.append(rel[:-5])
            files.sort(key=natural)
            if not files:
                continue
            title = (group.title() + ' — ' if group else '') + clean(name).title()
            if group:
                title = group.title() + ' — ' + clean(name).title()
            title = title.replace(' & ', ' & ')
            cover = 'cover' if 'cover' in files else files[0]
            if cover != files[0]:
                files.remove(cover); files.insert(0, cover)
            d = '/'.join(['photos', cat] + ([group] if group else []) + [name])
            series.append({'t': title, 'c': cat, 'ty': typ, 'd': d, 'f': files})

def url(s, f):
    from urllib.parse import quote
    return '/'.join(quote(seg, safe='') for seg in (s['d'] + '/' + f).split('/')) + '.webp'

tiles = []
for i, s in enumerate(series):
    tiles.append(
        f'      <article class="proj" data-idx="{i}" data-type="{s["ty"]}" data-category="{s["c"]}" tabindex="0">\n'
        f'        <div class="proj__frame"><img src="{url(s, s["f"][0])}" alt="{html.escape(s["t"])}" loading="lazy" decoding="async">'
        f'<div class="proj__title">{html.escape(s["t"])}<span class="proj__count">{len(s["f"])}</span></div></div>\n'
        f'      </article>\n')

n = len(series)
pick = sorted({round(k * (n - 1) / 5) for k in range(6)}) if n > 6 else range(n)
intro = [url(series[k], series[k]['f'][0]) for k in pick]
data = json.dumps([{'t': s['t'], 'd': s['d'], 'f': s['f']} for s in series], ensure_ascii=False, separators=(',', ':'))

path = os.path.join(ROOT, 'index.html')
src = open(path, encoding='utf-8').read()
src = re.sub(r'(<!-- BEGIN TILES[^\n]*-->\n).*?(<!-- END TILES -->)',
             lambda m: m.group(1) + ''.join(tiles) + m.group(2), src, flags=re.S)
src = re.sub(r'(/\* BEGIN SERIES \*/\n).*?(  /\* END SERIES \*/)',
             lambda m: m.group(1) + '  const SERIES = ' + data + ';\n  const INTRO = ' + json.dumps(intro) + ';\n' + m.group(2),
             src, flags=re.S)
open(path, 'w', encoding='utf-8').write(src)
print(f'{n} series, {sum(len(s["f"]) for s in series)} photos')
for s in series:
    print(f'  [{s["c"]}] {s["t"]}  ({len(s["f"])})')
