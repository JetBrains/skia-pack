#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/..
OLDVER=m91-71fcb16fc2
NEWVER=m91-1a01201b77
find -E $ROOT/script *.md .github  -regex '.*\.(py|md|yml)' -exec sed -i '' -e "s/$OLDVER/$NEWVER/g" {} \;
