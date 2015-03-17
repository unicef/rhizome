#!/bin/bash

git pull origin development
pip install -r requirements.txt
python manage.py syncdb --settings=polio.prod_settings
python manage.py migrate --settings=polio.prod_settings
bash bin/build_db.sh
echo '== BUILDING DOCUMENTATION ==" 
make clean -C docs
