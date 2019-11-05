#/bin/bash
pip install -U sphinx
pip install -e ../.
make -C ../docs html
npm install
brunch build --production
mkdir public
mkdir public/docs
cp -r ../docs/_build/html/* public/docs