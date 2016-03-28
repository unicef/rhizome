cd webapp &&
npm install &&
cd webapp &&
npm run package &&
mkdir -p ~/deploy/rhizome-work &&
mv dist/rhizome.zip ~/deploy/rhizome-work/rhizome.zip &&
cd ~/deploy/rhizome-work &&
unzip -o rhizome.zip -d /var/www/apps/rhizome/ &&
cd ../var/www/apps/rhizome/ &&
sudo rm -rf `find . -name "*.pyc*"` &&
cd .. &&
python manage.py syncdb --settings=settings &&
python manage.py migrate --settings=settings &&
source ../environment_seed.env &&
python manage.py collectstatic --noinput --settings=settings