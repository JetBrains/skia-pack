#! /usr/bin/env python3

import argparse, common, os, pathlib, platform, re, subprocess, sys

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))

  parser = common.create_parser(True)
  args = parser.parse_args()

  # Clone depot_tools
  if not os.path.exists("depot_tools"):
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", "depot_tools"])

  # Clone Skia
  match = re.match('(m\\d+)(?:-([0-9a-f]+)(?:-([1-9][0-9]*))?)?', args.version)
  if not match:
    raise Exception('Expected --version "m<ver>-<sha>", got "' + args.version + '"')
  branch = "chrome/" + match.group(1)
  commit = match.group(2)
  iteration = match.group(3)

  if os.path.exists("skia"):
    os.chdir("skia")
    if subprocess.check_output(["git", "branch", "--list", branch]):
      print("> Advancing", branch)
      subprocess.check_call(["git", "checkout", "-B", branch])
      subprocess.check_call(["git", "fetch"])
      subprocess.check_call(["git", "reset", "--hard", "origin/" + branch])
      subprocess.check_call(["git", "clean", "-d", "-f"])
    else:
      print("> Fetching", branch)
      subprocess.check_call(["git", "reset", "--hard"])
      subprocess.check_call(["git", "clean", "-d", "-f"])
      subprocess.check_call(["git", "fetch", "origin", branch + ":remotes/origin/" + branch])
      subprocess.check_call(["git", "checkout", branch])
  else:
    print("> Cloning", branch)
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://skia.googlesource.com/skia", "--quiet", "--branch", branch, "skia"])
    os.chdir("skia")

  # Checkout commit
  print("> Checking out", commit)
  subprocess.check_call(["git", "-c", "advice.detachedHead=false", "checkout", commit])

  # Apply patches
  patches = ["11081_SkLoadICU.cpp.patch",
             "11132_SkParse.patch",
             "11794_SkString.patch",
             "12965_TextIndent.patch",
             "13519_AtlasPathRenderer.patch",
             "13646_Skip_activate-emsdk_for_arm_linux.patch",
             "Fix_glyph_position_and_rects_for_chars_inside_ligatures.patch",
             "13649_fix_assert_when_we're_getting_line_metrics.patch",
             "10666_allow_to_configure_font_rasterisation_settings_in_paragraph.patch",
             "Workaround_glyph_position_at_eol.patch"]

  subprocess.check_call(["git", "reset", "--hard"])
  for patch_name in patches:
    patch = pathlib.Path(os.pardir, "patches", patch_name)
    print("> Applying", patch)
    subprocess.check_call(["git", "apply", str(patch)])

  # git deps
  print("> Running tools/git-sync-deps")
  if 'windows' == common.host():
    env = os.environ.copy()
    env['PYTHONHTTPSVERIFY']='0'
    subprocess.check_call(["python3", "tools/git-sync-deps"], env=env)
  else:
    subprocess.check_call(["python3", "tools/git-sync-deps"])

  return 0

if __name__ == '__main__':
  sys.exit(main())
