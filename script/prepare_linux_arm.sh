#!/bin/bash
set -o errexit -o nounset -o pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install binutils build-essential -y
apt-get install software-properties-common -y
apt-get install python git fontconfig libfontconfig1-dev libglu1-mesa-dev curl wget -y
apt-get install clang -y
