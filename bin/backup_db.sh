#!/bin/bash

# http://serverfault.com/questions/59838/whats-the-best-way-to-automate-backing-up-of-postgresql-databases

BACKUPDIR=/var/lib/postgresql/sql_backups/
DATE=`date +%Y-%m-%dT%H:%M:%S`
DB=polio
USER=djangoapp

DUMPALL="/usr/bin/pg_dumpall"
PGDUMP="/usr/bin/pg_dump"
PSQL="/usr/bin/psql"

echo Backing up $DB database to $BACKUPDIR$DATE-$DB.sql.tgz ...

DUMPALL$ --verbose --format=t -f "$BACKUPDIR$DATE.sql.tar" $DB -U $USER

# delete backup files older than 30 days
OLD=$(find $BACKUPDIR -type d -mtime +30)
if [ -n "$OLD" ] ; then
        echo deleting old backup files: $OLD
        echo $OLD | xargs rm -rfv
fi
