#! /usr/bin/env python3

import argparse, common, os, pathlib, platform, re, subprocess, sys

def checkout_and_chdir(url, path, branch, commit):
  print("> Adding", path)
  if os.path.exists(path):
    os.chdir(path)
    if subprocess.check_output(["git", "branch", "--list", branch]):
      print("> Advancing", branch)
      subprocess.check_call(["git", "checkout", "-B", branch])
      subprocess.check_call(["git", "fetch"])
      subprocess.check_call(["git", "reset", "--hard", "origin/" + branch])
    else:
      print("> Fetching", branch)
      subprocess.check_call(["git", "reset", "--hard"])
      subprocess.check_call(["git", "fetch", "origin", branch + ":remotes/origin/" + branch])
      subprocess.check_call(["git", "checkout", branch])
  else:
    print("> Cloning", branch)
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", url, "--quiet", "--single-branch", "--branch", branch, path])
    os.chdir(path)

  # Checkout commit
  print("> Checking out", commit)
  subprocess.check_call(["git", "-c", "advice.detachedHead=false", "checkout", commit])

def git_apply(file):
  print("> Applying", file)
  subprocess.check_call(["git", "apply", file])

def chdir_home():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))

def main():
  chdir_home()

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
  # iteration = match.group(3)

  checkout_and_chdir("https://skia.googlesource.com/skia", "skia", branch, commit)

  # Checkout commit
  print("> Checking out", commit)
  subprocess.check_call(["git", "-c", "advice.detachedHead=false", "checkout", commit])

  # Apply patches
  subprocess.check_call(["git", "reset", "--hard"])
  for x in pathlib.Path(os.pardir, 'patches').glob('*.patch'):
    git_apply(str(x))

  host = common.host()

  if 'mingw' == host:
    file = os.pardir + "/patches/mingw/0003-Don-t-download-prebuild-gn-and-emsdk.patch"
    git_apply(file)

  # git deps
  print("> Running tools/git-sync-deps")
  if common.windows():
    env = os.environ.copy()
    env['PYTHONHTTPSVERIFY']='0'
    subprocess.check_call(["python", "tools/git-sync-deps"], env=env)
  else:
    subprocess.check_call(["python", "tools/git-sync-deps"])

  return 0

if __name__ == '__main__':
  sys.exit(main())
