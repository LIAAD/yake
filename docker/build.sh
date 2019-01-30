#!/usr/bin/env bash
if [ $# -eq 0 ]
  then
    tag='latest'
  else
    tag=$1
fi

INITIAL_DIR=$(pwd)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR/Dockerfiles/yake-server"
docker build -t feupinfolab/yake-server:$tag .
docker run -p 5000:5000 feupinfolab/yake-server:$tag

cd "$DIR/Dockerfiles/yake"
docker build -t feupinfolab/yake:$tag .
docker run -d feupinfolab/yake:$tag

docker ps -a

cd $INITIAL_DIR
