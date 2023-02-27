#!/usr/bin/env bash
if [ $# -eq 0 ]; then
  tag='latest'
else
  tag=$1
fi

INITIAL_DIR=$(pwd)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# get constants
source "$DIR/constants.sh"

cd "$DIR/Dockerfiles/yake-server"
docker build -t "$YAKE_SERVER_IMAGE:$TAG" .
docker run -d -p $YAKE_PORT:$YAKE_PORT "$YAKE_SERVER_IMAGE:$TAG"

cd "$DIR/Dockerfiles/yake"
docker build -t "$YAKE_IMAGE:$TAG" .
docker run -d "$YAKE_IMAGE:$TAG"

docker ps -a

cd $INITIAL_DIR
