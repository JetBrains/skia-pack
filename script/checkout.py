#! /usr/bin/env python3

import common, os, re, subprocess, sys, time

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

def git_sync_with_retries(max_retries=3, backoff_seconds=5):
    attempt = 0
    while True:
        try:
            print("> Running tools/git-sync-deps (attempt {}/{})".format(attempt+1, max_retries+1))
            # On Windows we need to disable HTTPS verify
            if common.host() == 'windows':
                env = os.environ.copy()
                env['PYTHONHTTPSVERIFY'] = '0'
                subprocess.check_call([sys.executable, "tools/git-sync-deps"], env=env)
            else:
                subprocess.check_call([sys.executable, "tools/git-sync-deps"])
            print("✔ Success")
            break
        except subprocess.CalledProcessError as e:
            attempt += 1
            if attempt > max_retries:
                print("✖ All {} retries failed. Giving up.".format(max_retries))
                raise
            else:
                wait = backoff_seconds * attempt
                print(f"⚠️  Failed (exit {e.returncode}), retrying in {wait}s…")
                time.sleep(wait)

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
  # Trying to avoid 429 HTTP Error from Google repos
  git_sync_with_retries()

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
