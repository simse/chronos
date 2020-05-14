if [ $CIRCLE_BRANCH = "master" ]
then
    echo 'export TAG=master' >> $BASH_ENV
else
    echo 'export TAG=$CIRCLE_BRANCH' >> $BASH_ENV
fi

echo $TAG