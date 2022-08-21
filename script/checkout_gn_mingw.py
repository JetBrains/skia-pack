#! /usr/bin/env python3

import argparse, common, os, pathlib, platform, re, subprocess, sys
from checkout import checkout_and_chdir, git_apply, chdir_home


def main():
  chdir_home()

  print("> Downloading gn source")
  checkout_and_chdir("https://gn.googlesource.com/gn", "gn", "main", "d62642c920e6a0d1756316d225a90fd6faa9e21e")

  # Apply patches
  patches = [
      "0002-gn-ninja-deletes-objs-workaround.patch",
      "0006-add-missing-limits.patch",
      "0009-remove-as-needed-from-ldflags.patch",
      "0010-git-call-must-not-use-shell-in-mingw.patch",
  ]
  for x in patches:
    git_apply(os.pardir + "/patches/mingw/" + x)

  print("> Downloading chromium build source")
  chdir_home()
  checkout_and_chdir("https://chromium.googlesource.com/chromium/src/build.git", "build", "main", "fd86d60f33cbc794537c4da2ef7e298d7f81138e")
  git_apply(os.pardir + "/patches/mingw/0007-add-mingw-toolchain-build.patch")

  print("> Linking gn to skia build")
  chdir_home()
  subprocess.check_call(["rm", "-rf", "skia/build"])
  subprocess.check_call(["ln", "-sf", os.path.abspath('build'), 'skia'])
  pathlib.Path("skia/build/config/gclient_args.gni").write_text("checkout_google_benchmark = false")

  print("> Patching skia")
  os.chdir("skia")
  git_apply(os.pardir + "/patches/mingw/0001-fixes-to-compile.patch")



if __name__ == '__main__':
  main()