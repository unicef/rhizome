#!/bin/bash

# http://serverfault.com/questions/59838/whats-the-best-way-to-automate-backing-up-of-postgresql-databases

BACKUPDIR=/some/dir/sql_backups/
DATE=`date +%Y-%m-%dT%H:%M:%S`
DB=rhizome

PSQL="/usr/bin/psql"

echo Backing up $DB database to $BACKUPDIR$DATE-$DB.sql.gz ...

pg_dump --verbose -f "$BACKUPDIR$DATE.sql" $DB

echo back up complete... zipping file

gzip "$BACKUPDIR$DATE.sql"

# delete backup files older than 10 days
OLD=$(find $BACKUPDIR -type d -mtime +10)
if [ -n "$OLD" ] ; then

        echo deleting old backup files: $OLD
        echo $OLD | xargs rm -rfv
fi
