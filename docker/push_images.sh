#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# get constants
source "$DIR/constants.sh"

docker push "$YAKE_IMAGE:$TAG"
docker push "$YAKE_SERVER_IMAGE:$TAG"
