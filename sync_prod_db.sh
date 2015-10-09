!/bin/bash

DB=polio
USER=djangoapp

echo "pulling zipped .sql file"

wget https://s3.amazonaws.com/rhizome-backup/rhizome_latest.sql.gz -P ~/
#
# echo "killing all connections..."
#
# # Kill All Connections to DB #
# psql -c"select pg_terminate_backend(pid)
#    from pg_stat_activity
#    where datname = '$DB';"
#
# echo "just terminated all of your psql connections.. dropping the database in 5..4.."
#
# sleep 5
# psql -c "DROP DATABASE IF EXISTS $DB;"
#
#
# echo "...CREATING DATABASE..."
#
# psql -c "CREATE DATABASE $DB
#   WITH OWNER = djangoapp
#        ENCODING = 'UTF8'
#        TABLESPACE = pg_default
#        LC_COLLATE = 'en_US.UTF-8'
#        LC_CTYPE = 'en_US.UTF-8'
#        CONNECTION LIMIT = -1;" postgres > /dev/null
#
# echo Loading production data...
# psql -f db.sql $DB $USER
echo done.
