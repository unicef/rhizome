#!/bin/bash

BACKUPDIR=sql_backups/
COMPRESSION=4
DATE=`date +%Y-%m-%dT%H:%M:%S`
DB=polio
HOST=50.57.77.252
USER=djangoapp

# # FIXME: It would be nice to have command-line switches for skipping back-up and
# # skipping the sync
#
# echo Backing up $DB database to $BACKUPDIR$DATE-$DB.sql.tgz ...
#
# if [ ! -d $BACKUPDIR ]; then
#   mkdir $BACKUPDIR
# fi
#
# pg_dump --verbose --format=t -f "$BACKUPDIR$DATE.sql.tar" $DB
#
# echo done.
#
# # FIXME: It would be better to prompt for the password upfront, not midway
# # through syncing
# echo
# echo Downloading data from $HOST:$DB...
# pg_dump --verbose -C -h $HOST -U $USER -f db.sql $DB
# echo done.
#
# echo
# echo Deleting data from $DB database...
#
# FIXME: Should exit with an error status if we fail to drop the database
psql -c"select pg_terminate_backend(pid)
   from pg_stat_activity
   where datname = '$DB';"

echo "just terminated all of your psql connections.. dropping the database in 5..4.."

sleep 5
psql -c "DROP DATABASE IF EXISTS $DB;"

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
