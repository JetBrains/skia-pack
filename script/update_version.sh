#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/..
OLDVER=m92-81ce29695f
NEWVER=m92-a77a4620d2
find -E $ROOT/script *.md .github  -regex '.*\.(py|md|yml)' -exec sed -i '' -e "s/$OLDVER/$NEWVER/g" {} \;
