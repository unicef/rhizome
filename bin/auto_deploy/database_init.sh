cd /var/www/apps/rhizome/
rm -rf `find . -name "*.pyc*"`
python manage.py syncdb --settings=settings
python manage.py migrate --settings=settings
source ../environment_seed.env
python manage.py collectstatic --noinput --settings=settings