#!/bin/bash
set -o errexit -o nounset -o pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install binutils build-essential -y
apt-get install python3 -y
apt-get install --fix-broken python-pycurl python-apt python3-software-properties -y
apt-get install software-properties-common -y
add-apt-repository ppa:git-core/ppa -y
apt-get install git fontconfig libfontconfig1-dev libgl-dev curl wget -y
apt-get install clang -y
