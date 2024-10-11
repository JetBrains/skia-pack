#! /usr/bin/env python3

import common, os, re, subprocess, sys

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))

  # Clone depot_tools
  if not os.path.exists("depot_tools"):
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", "depot_tools"])

  os.chdir("../skia")

  # git deps
  print("> Running tools/git-sync-deps")
  if 'windows' == common.host():
    env = os.environ.copy()
    env['PYTHONHTTPSVERIFY']='0'
    subprocess.check_call(["python3", "tools/git-sync-deps"], env=env)
  else:
    subprocess.check_call(["python3", "tools/git-sync-deps"])

  # fetch ninja
  print("> Fetching ninja")
  subprocess.check_call(["python3", "bin/fetch-ninja"])

  return 0

if __name__ == '__main__':
  sys.exit(main())
