#!/bin/bash

/etc/init.d/postgresql start

python ./manage.py syncdb
python ./manage.py migrate

bash ./bin/build_db.sh

python ./manage.py runserver 0.0.0.0:8000
