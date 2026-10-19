# NP — Photography portfolio

Single-file site (`index.html`), no external requests, published with GitHub Pages.

## Structure of `photos/`
    photos/<category>/<group>/<series>/*.webp     e.g. photos/fashion/NANTES FASHION WEEK/EXPORT CUZIN/IMG_1.webp
    photos/<category>/<series>/*.webp             e.g. photos/wedding/MARIAGE KEMEL & FERDI/IMG_1.webp
Categories: `architecture` (personal), `fashion` and `wedding` (commercial).
One series folder = one tile in the grid; clicking it opens the gallery.

## After adding / renaming photos
Run `python tools/build_index.py` at the repo root (needs Python 3), then commit `index.html`.
- Tile cover = first photo (natural order). To force another one, name it `cover.webp` inside the series folder.
- Tile title = folder name (prefixes `EXPORT`, `MARIAGE`, `Défilé` are dropped).

## To fill in
- Contact email: search `hello@np-photo.com` in `index.html` (placeholder).
- Instagram link in the footer (`href="#"`).

## Cleanup
The `archivo-*.woff2` files at the repo root are no longer used (font is embedded in `index.html`) and can be deleted.
