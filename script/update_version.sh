#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/..
OLDVER=m105-f204b137b9-5
NEWVER=m105-305b7c02
find -E $ROOT/script *.md .github  -regex '.*\.(py|md|yml)' -exec sed -i '' -e "s/$OLDVER/$NEWVER/g" {} \;
