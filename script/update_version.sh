#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/..
OLDVER=m94-975fcdd755
NEWVER=m94-fd7c5792ca
find -E $ROOT/script *.md .github  -regex '.*\.(py|md|yml)' -exec sed -i '' -e "s/$OLDVER/$NEWVER/g" {} \;
