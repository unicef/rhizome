cd webapp &&
npm install &&
npm run package &&
mkdir -p ~/deploy/rhizome-work &&
mv dist/rhizome.zip ~/deploy/rhizome-work/rhizome.zip &&
cd ~/deploy/rhizome-work &&
unzip -o rhizome.zip -d /var/www/apps/rhizome/ &&
<<<<<<< HEAD
cd ../var/www/apps/rhizome/ &&
=======
cd /var/www/apps/rhizome/ &&
>>>>>>> parent of 3dfdc92... Revert "script clean up"
sudo rm -rf `find . -name "*.pyc*"`