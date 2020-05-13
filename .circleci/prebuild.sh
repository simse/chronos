if [[ $CIRCLE_BRANCH = "edge" ]]
    export $TAG=edge
fi

if [[ $CIRCLE_BRANCH = "master" ]]
    export $TAG=latest
fi