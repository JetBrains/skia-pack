[![internal JetBrains project](https://jb.gg/badges/internal.svg)](https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub)
# Automated Skia builds

This repo is dedicated to building Skia binaries for use in [Skiko](https://github.com/JetBrains/skiko).

## Prebuilt binaries

Prebuilt binaries can be found [in releases](https://github.com/JetBrains/skia-pack/releases).

## Building next version of Skia

1. Find the release commit in [Skia repository](https://github.com/google/skia) (look for chrome/mXXX branch)
2. Rebase `skiko` branch in [Skia fork repository](https://github.com/JetBrains/skia) on this commit and force push
3. Update `version` in [.github/workflows/build.yml](https://github.com/JetBrains/skia-pack/blob/master/.github/workflows/build.yml).

## Building locally

Note: Better check build.yml for the detailed command for your machine

```sh
python3 script/checkout.py --version m138-9e6b5bff162
python3 script/build.py
python3 script/archive.py --version m138-9e6b5bff162
```

To build a debug build:

```sh
python3 script/checkout.py --version m138-9e6b5bff162
python3 script/build.py --build-type Debug
python3 script/archive.py --version m138-9e6b5bff162 --build-type Debug
```

### Windows-specific

On Windows, skia-pack requires Clang-cl to be installed. Clang-cl is a part of LLVM and can be downloaded from the [LLVM project's website](https://releases.llvm.org/). Please also make sure that Clang-cl.exe is available on %PATH%.
