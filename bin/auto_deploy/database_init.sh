cd /var/www/apps/rhizome/
find . -name \*.pyc -exec rm -rf {}\;
source venv/bin/activate
sudo pip install --upgrade -r requirements.txt
export PYTHONPATH="/var/www/apps/rhizome/rhizome"
python manage.py syncdb --settings=settings
source ../environment_seed.env
# python manage.py migrate --settings=settings
python manage.py collectstatic --noinput --settings=settings