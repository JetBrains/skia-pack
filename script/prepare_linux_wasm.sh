#!/bin/bash
set -o errexit -o nounset -o pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install binutils build-essential -y
apt-get install software-properties-common -y
apt-get install python git curl wget -y

if [ -d ./emsdk ]; then
  cd ./emsdk
  git pull
else
  git clone https://github.com/emscripten-core/emsdk.git
  cd ./emsdk
fi
./emsdk install 2.0.29
./emsdk activate 2.0.29
source ./emsdk_env.sh
