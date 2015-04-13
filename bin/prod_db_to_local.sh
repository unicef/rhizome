#!/bin/bash

DB=polio
HOST=polio_prod
USER=djangoapp

# FIXME: It would be nice to have command-line switches for skipping back-up and
# skipping the sync

## FIXME: It would be better to prompt for the password upfront, not midway
# through syncing

echo
echo Downloading data from $HOST:$DB...
ssh $HOST 'sudo -u postgres pg_dump polio' > db.sql

echo done.

echo
echo "killing all connections..."

# Kill All Connections to DB #
psql -c"select pg_terminate_backend(pid)
   from pg_stat_activity
   where datname = '$DB';"

echo "just terminated all of your psql connections.. dropping the database in 5..4.."

sleep 5
psql -c "DROP DATABASE IF EXISTS $DB;"


echo "...CREATING DATABASE..."

psql -c "CREATE DATABASE $DB
  WITH OWNER = djangoapp
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;" postgres > /dev/null


echo Loading production data...
psql -f db.sql $DB $USER
echo done.
