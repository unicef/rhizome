cd /var/www/apps/rhizome/ &&
python manage.py syncdb --settings=settings &&
python manage.py migrate --settings=settings &&
source ../environment_seed.env &&
python manage.py collectstatic --noinput --settings=settings