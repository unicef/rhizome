#!/bin/bash

git pull origin development
pip install -r requirements.txt
python manage.py syncdb
python manage.py migrate
bash bin/build_db.sh
