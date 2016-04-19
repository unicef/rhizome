mkdir -p ~/deploy/rhizome-work &&
cd ~/deploy/rhizome-work &&
mkdir -p /var/www/apps/rhizome/ &&
unzip -o rhizome.zip -d /var/www/apps/rhizome/ &&
cd /var/www/apps/rhizome/ &&
cd webapp && npm install && cd ..
sudo rm -rf `find . -name "*.pyc*"`