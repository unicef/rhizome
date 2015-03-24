#!/bin/bash

BACKUPDIR=/var/lib/postgresql/sql_backups/
COMPRESSION=4
DATE=`date +%Y-%m-%dT%H:%M:%S`
DB=polio
USER=djangoapp

echo Backing up $DB database to $BACKUPDIR$DATE-$DB.sql.tgz ...

pg_dump --verbose --format=t -f "$BACKUPDIR$DATE.sql.tar" $DB -U $USER
