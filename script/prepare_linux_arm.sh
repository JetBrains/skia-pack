#!/bin/bash
set -o errexit -o nounset -o pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install binutils build-essential -y
apt-get install software-properties-common -y
apt-get install python git fontconfig libfontconfig1-dev libglu1-mesa-dev curl wget -y
apt-get install openjdk-11-jdk -y
apt-get install clang-11 -y && \
apt-get remove g++ -y && \
update-alternatives --install /usr/bin/clang clang /usr/bin/clang-11 100 && \
update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-11 100
