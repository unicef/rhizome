#!/bin/bash

# docker run -i -d -p 8000:8000 -v $PWD:/etc/polio polio /bin/bash /etc/polio/initial.sh

cd /etc/polio

/etc/init.d/postgresql start

python ./manage.py syncdb
python ./manage.py migrate

sh ./bin/build_db.sh

python ./manage.py runserver 0.0.0.0:8000