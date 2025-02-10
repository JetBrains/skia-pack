#! /usr/bin/env python3

import common, os, re, subprocess, sys

def checkout_skia(commit):
  # Clone Skia

  if os.path.exists("skia"):
    print("> Fetching {}".format(commit))
    os.chdir("skia")
    subprocess.check_call(["git", "reset", "--hard"])
    subprocess.check_call(["git", "clean", "-d", "-f"])
    subprocess.check_call(["git", "fetch", "origin"])
  else:
    print("> Cloning")
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://github.com/JetBrains/skia.git", "--quiet"])
    os.chdir("skia")
    subprocess.check_call(["git", "fetch", "origin"])

  # Checkout commit
  print("> Checking out", commit)
  subprocess.check_call(["git", "-c", "advice.detachedHead=false", "checkout", commit])

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir))

  parser = common.create_parser(True)
  args = parser.parse_args()

  # Clone depot_tools
  if not os.path.exists("depot_tools"):
    subprocess.check_call(["git", "clone", "--config", "core.autocrlf=input", "https://chromium.googlesource.com/chromium/tools/depot_tools.git", "depot_tools"])

  match = re.match('(m\\d+)(?:-([0-9a-f]+)(?:-([1-9][0-9]*))?)?', args.version)
  if not match:
    raise Exception('Expected --version "m<ver>-<sha>", got "' + args.version + '"')

  commit = match.group(2)
  checkout_skia(commit)

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

  # Patch an issue in Windows toolchain:
  # Enable delayed environment variable expansion for CMD to make GitHub Actions happy
  # https://issues.skia.org/issues/393402169
  with open("gn/toolchain/BUILD.gn", "r") as toolchain_file:
    toolchain_file_contents = toolchain_file.read()

  toolchain_file_contents = toolchain_file_contents.replace(
    'shell = "cmd.exe /c',
    'shell = "cmd.exe /v:on /c',
  ).replace(
    r'env_setup = "$shell set \"PATH=%PATH%',
    r'env_setup = "$shell set \"PATH=!PATH!',
  )

  with open("gn/toolchain/BUILD.gn", "w") as toolchain_file:
    toolchain_file.write(toolchain_file_contents)

  return 0

if __name__ == '__main__':
  sys.exit(main())
