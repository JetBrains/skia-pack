#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/..
OLDVER=m99-f85ab491eb
NEWVER=m99-f85ab491eb-2
find -E $ROOT/script *.md .github  -regex '.*\.(py|md|yml)' -exec sed -i '' -e "s/$OLDVER/$NEWVER/g" {} \;
