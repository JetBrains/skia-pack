[![internal JetBrains project](https://jb.gg/badges/internal.svg)](https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub)
# Automated Skia builds

This repo is dedicated to building Skia binaries for use in [Skiko](https://github.com/JetBrains/skiko).

## Prebuilt binaries

Prebuilt binaries can be found [in releases](https://github.com/JetBrains/skia-pack/releases).

## Building next version of Skia

1. Find the release commit in [Skia repository](https://github.com/google/skia) (look for chrome/mXXX branch)
2. Rebase `skiko` branch in [Skia fork repository](https://github.com/JetBrains/skia) on this commit
3. Update `version` in [.github/workflows/build.yml](https://github.com/JetBrains/skia-pack/blob/master/.github/workflows/build.yml).

## Building locally

```sh
python3 script/checkout.py --version m116-51072f3-1
python3 script/build.py
python3 script/archive.py --version m116-51072f3-1
```

To build a debug build:

```sh
python3 script/checkout.py --version m116-51072f3-1
python3 script/build.py --build-type Debug
python3 script/archive.py --version m116-51072f3-1 --build-type Debug
```
