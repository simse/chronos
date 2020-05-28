#!/bin/bash
if [ $TRAVIS_BRANCH = "master" ]
then
    export TAG=latest
else
    export TAG=$TRAVIS_BRANCH
fi

echo $TAG

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build . -t simsemand/chronos:$TAG
docker push simsemand/chronos:$TAG