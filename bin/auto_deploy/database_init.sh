cd /var/www/apps/rhizome/
sudo find . -name \*.pyc -type f -exec rm -f {} \;
cp /var/www/apps/settings.py /var/www/apps/rhizome/settings.py
pip install -r requirements.txt
python manage.py syncdb --settings=settings
# python manage.py migrate --settings=settings
python manage.py collectstatic --noinput --settings=settings