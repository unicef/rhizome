#!/bin/bash

sleep 5

python ./manage.py syncdb --noinput
python ./manage.py migrate --noinput

python ./manage.py runserver 0.0.0.0:8000
