if [[ $CIRCLE_BRANCH == "edge" ]]
then
    export TAG=edge
fi

if [[ $CIRCLE_BRANCH == "master" ]]
then
    export TAG=latest
fi

echo $TAG