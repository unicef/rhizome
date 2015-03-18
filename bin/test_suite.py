psql -c 'CREATE DATABASE polio_test';

# build stored procedures #
python manage.py syncdb --settings=polio.settings_test
python manage.py migrate --settings=polio.settings_test

psql -f datapoints/sql/functions/fn_calc_datapoint.sql -h localhost polio_test
psql -f datapoints/sql/functions/fn_agg_datapoint_by_region_type.sql -h localhost polio_test
psql -f datapoints/sql/functions/fn_init_agg_datapoint.sql -h localhost polio_test
psql -f datapoints/sql/functions/fn_test_data_accuracy.sql -h localhost polio_test 

# run tests #
#python manage.py test datapoints.tests.test_cache --settings=polio.settings_test
psql -c 'DROP DATABASE polio_test';
