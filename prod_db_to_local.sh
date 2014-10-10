#!/bin/bash

# Take a dump from the remove server
pg_dump -C -h 50.57.77.252 -U djangoapp polio -f ~/db.sql

# drop the polio DB if it exists and create it again
psql << EOF
DROP DATABASE IF EXISTS polio;
CREATE DATABASE polio;
EOF

# restore the db from the backup we just took
psql -U djangoapp -d polio -f ~/db.sql
