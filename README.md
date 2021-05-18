# Automated Skia builds

This repo is dedicated to building Skia binaries for use in [Skiko](https://github.com/JetBrains/skiko).

## Prebuilt binaries

Prebuilt binaries can be found [in releases](https://github.com/JetBrains/skia-pack/releases).

## Building next version of Skia

Update `version` in [.github/workflows/build.yml](https://github.com/JetBrains/skia-pack/blob/master/.github/workflows/build.yml).

## Building locally

```sh
python3 script/checkout.py --version m91-d18efa37cb
python3 script/build.py
python3 script/archive.py
```

To build a debug build:

```sh
python3 script/checkout.py --version m91-d18efa37cb
python3 script/build.py --build-type Debug
python3 script/archive.py --build-type Debug
```
