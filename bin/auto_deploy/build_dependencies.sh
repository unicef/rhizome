cd webapp &&
npm install &&
npm run package &&
mkdir -p ~/deploy/rhizome-work &&
mv dist/rhizome.zip ~/deploy/rhizome-work/rhizome.zip &&
cd ~/deploy/rhizome-work &&
unzip -o rhizome.zip -d /var/www/apps/rhizome/ &&
cd /var/www/apps/rhizome/ &&
sudo rm -rf `find . -name "*.pyc*"`