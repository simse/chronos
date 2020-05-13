if [ $CIRCLE_BRANCH = "edge" ]
then
    echo 'export TAG=edge' >> $BASH_ENV
fi

if [ $CIRCLE_BRANCH = "master" ]
then
    echo 'export TAG=master' >> $BASH_ENV
fi

echo $TAG