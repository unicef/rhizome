mkdir -p /home/ubuntu/deploy/rhizome-work &&
cd /home/ubuntu/deploy/rhizome-work &&
mkdir -p /var/www/apps/rhizome/ &&
unzip -o rhizome.zip -d /var/www/apps/rhizome/ &&
cd /var/www/apps/rhizome/ &&
sudo rm -rf `find . -name "*.pyc*"`