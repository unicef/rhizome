#!/bin/bash

# http://serverfault.com/questions/59838/whats-the-best-way-to-automate-backing-up-of-postgresql-databases

BACKUPDIR=/some/dir/sql_backups/
DATE=`date +%Y-%m-%dT%H:%M:%S`
DB=rhizome

PSQL="/usr/bin/psql"

BACKUPFILE="$BACKUPDIR$DATE.sql"

pg_dump --verbose -f $BACKUPFILE $DB

gzip "$BACKUPFILE"

cp $BACKUPFILE'.gz'  $BACKUPDIR'rhizome_latest.sql.gz'

# delete backup files older than 10 days
OLD=$(find $BACKUPDIR -type d -mtime +10)
if [ -n "$OLD" ] ; then

        echo deleting old backup files: $OLD
        echo $OLD | xargs rm -rfv
fi
