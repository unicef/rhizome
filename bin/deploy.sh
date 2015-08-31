#!/bin/bash

echo "== PULLING DEV BRANC=="
git pull origin development

echo "== INSTALL PYTHON REQUIREMENTS =="
pip install -r requirements.txt

echo "== SYNCDB / MIGRATE =="
python manage.py syncdb --settings=polio.prod_settings
python manage.py migrate --settings=polio.prod_settings

echo "== BUILDING DATABASE =="
bash bin/build_db.sh

echo "== BUILDING DOCUMENTATION =="
make clean -C docs
make html -C docs

echo "== RUNNING TESTS =="
python manage.py test datapoints.tests.test_cache --settings=polio.settings_test
