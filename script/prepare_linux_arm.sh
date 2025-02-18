#!/bin/bash
set -o errexit -o nounset -o pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install python3 -y
apt-get install git fontconfig libfontconfig1-dev libgl-dev -y
apt-get install clang -y
