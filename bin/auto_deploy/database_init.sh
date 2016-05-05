cd /var/www/apps/rhizome/
find . -name "*.pyc" -type f -delete
pip install -r requirements.txt
python manage.py syncdb --settings=settings
# python manage.py migrate --settings=settings
python manage.py collectstatic --noinput --settings=settings