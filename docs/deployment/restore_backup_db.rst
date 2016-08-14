Restoring and backing up a database
===================================


On the production server you can run

::

  sudo -u postgres bash backup_db.sh

which will save the latest database version to the /home/ubuntu/sql_backups/rhizome_latest.sql


Copying a database from prod to your local
------------------------------------------

After running the backup db script above...

::

  $ scp prod_server:/home/ubuntu/sql_backups/rhizome_latest.sql.gz ~/
  $ gunzip ~/rhizome_latest.sql.gz
  $ psql postgres
  psql (9.4.5)
  Type "help" for help.

  postgres=# DROP DATABASE rhizome;
  postgres=# CREATE DATABASE rhizome WITH OWNER djangapp;

  $ psql rhizome -f ~/rhizome_latest.sql

Now your local server has the same database as production!


backup db script
----------------

see here https://github.com/unicef/rhizome/blob/master/bin/backup_db.sh

and here  http://serverfault.com/questions/59838/whats-the-best-way-to-automate-backing-up-of-postgresql-databases

.. code-block:: bash

    #!/bin/bash

    #
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
