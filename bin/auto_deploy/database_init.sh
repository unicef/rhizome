cd /var/www/apps/rhizome/
find . -name \*.pyc -exec rm -rf {}\;
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="/var/www/apps/rhizome/rhizome"
source ../environment_seed.env
python manage.py syncdb --settings=settings
# python manage.py migrate --settings=settings
python manage.py collectstatic --noinput --settings=settings
deactivate