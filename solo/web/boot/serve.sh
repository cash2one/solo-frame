PREFIX=$(cd "$(dirname "$0")"; pwd)
BASE=$PREFIX/../../..


#$BASE/solo/web/boot/prepare.sh 

cd $PREFIX
exec python $BASE/solo/web/boot/serve.py $1

