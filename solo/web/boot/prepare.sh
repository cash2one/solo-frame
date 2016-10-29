PREFIX=$(cd "$(dirname "$0")"; pwd)
PREFIX=$PREFIX/../../..
cd $PREFIX

WEB=$PREFIX/solo/web

python $WEB/boot/env_is_link.py
# python $WEB/boot/coffee_const.py
# python $WEB/boot/coffee_script.py -once
python $WEB/boot/css_js.py
# python $WEB/boot/js_requirejs.py
python $WEB/boot/signal.py
# ps x -u $USER|ack 'coffee_script.py'|xargs kill -9 > /dev/null 2>&1
