#!/bin/bash

DB=rhizome
DB_USER=djangoapp
DB_PASS="w3b@p01i0"
PORT=5432
OPTS="-U $DB_USER -h 127.0.0.1 -p $PORT"
export PGPASSWORD=$DB_PASS

# echo "Pulling zipped .sql file"
# curl https://s3.amazonaws.com/rhizome-backup/rhizome_latest.sql.gz -o ~/rhizome_latest.sql.gz

echo "Unzipping sql file"
gunzip -f ~/Desktop/rhizome_latest.sql.gz

echo "Killing all connections..."

# Kill All Connections to DB #
psql $OPTS -d wazir -c "select pg_terminate_backend(pid)
   from pg_stat_activity
   where datname = '$DB';"
#
echo "Terminated all of your psql connections.. Dropping the database in 5..4.."

sleep 5
echo "Drop database $DB"
psql $OPTS -d wazir -c "DROP DATABASE IF EXISTS $DB;"

echo "...CREATING DATABASE..."
#
psql $OPTS -c "CREATE DATABASE $DB
  WITH OWNER = djangoapp
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       CONNECTION LIMIT = -1;" wazir > /dev/null

# echo Loading production data...
psql $OPTS -d $DB -f ~/Desktop/rhizome_latest.sql

echo "Cleaning temporary SQL files"
rm ~/Desktop/rhizome_latest.sql
unset PGPASSWORD

echo "Done"
