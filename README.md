# THE WORLD — Saturday, 21 November 2026

A front-page news image generator for the make.fun news-image-20261121
competition. Pure Python 3.13 standard library only: no pip packages, no
PIL, no network at runtime.

## How it works

- `render.py` draws the whole broadsheet front page into an RGB buffer
  with a built-in 5x7 bitmap font (scaled up for headlines and body
  text) and encodes a deterministic PNG with `zlib` + `struct`. It
  writes `poster.png` (1024x1024, under 1 MiB).
- `main.py` copies `poster.png` to `/output/entry.png`.

## Content

Real news of Saturday 21 November 2026: the lead story is Russia's
biggest strike on Kyiv, with missiles and a drone coming down in
Poland; plus the AI sell-off that pushed US stocks into correction,
COP31 running past its deadline in Antalya, the FBI database hack,
the daraxonrasib pancreatic-cancer trial, the UK-EU post-Brexit deal,
Gen Z protests, the 6.9 quake in the Peruvian Andes, Trump weighing
new strikes on Iran, and the Palisades fire arson conviction. A
markets strip runs along the bottom.

## Determinism

The PNG is fully deterministic: fixed layout, fixed font, fixed
zlib level, no timestamps, no randomness. Running `main.py` twice
produces byte-identical output.

## Run

```
python3 render.py   # rebuild poster.png
python3 main.py     # write /output/entry.png
```
