psql -c 'CREATE DATABASE test_polio_test';
bash bin/build_db.sh
python manage.py test datapoints.tests.test_cache --settings=polio.settings_test
psql -c 'DROP DATABASE test_polio_test';
