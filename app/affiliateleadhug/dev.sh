#!/usr/bin/env bash

PREFIX=$(cd "$(dirname "$0")"; pwd)
BASE=$PREFIX/../..

while [ 1 ] 
do
$BASE/solo/web/boot/prepare.sh $1
ps x -u $USER|ack $BASE|ack 'solo/web/boot/serve'|awk  '{print $1}'|xargs kill -9 > /dev/null 2>&1

cd $PREFIX
echo "import _env;import app.$(basename $PREFIX).misc.config"
echo $BASE/solo/_app_config_.py
echo "import _env;import app.$(basename $PREFIX).misc.config" > $BASE/solo/_app_config_.py
python $BASE/solo/web/boot/css_js.py
python $BASE/solo/web/boot/serve.py

echo ""
for((i=1;i<=4;i++));do echo -n "$i ";sleep 1;done
done
