cd /var/www/apps/rhizome/
find . -name \*.pyc -exec rm -rf {}\;
pip install -r requirements.txt
python manage.py syncdb --settings=settings
# python manage.py migrate --settings=settings
python manage.py collectstatic --noinput --settings=settings