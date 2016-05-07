# Setting up the developer environment

### Set up with Vagrant(optional, recommended)
Utilizing a virtual machine we can spin up a fresh, clean, and isolated developer environment. Visit the [Vargant](https://www.vagrantup.com/) website to download it. Another dependency might be required - [Virtualbox](https://www.virtualbox.org/wiki/Downloads), any of these following steps fail.
* Commands to follow(keep in mind this is the installation order for ubuntu operating system):
  - Python/Django/Postgres configuration
  ```bash
  vagrant init ubuntu/trusty64
  vagrant up --provider virtualbox
  vagrant ssh
  sudo apt-get update
  sudo apt-get install -y
  sudo apt-get install unzip --fix-missing
  sudo apt-get install git-all
  ```
  You may already have python. you can check with the following command:
  ```
  which python
  ```
  If this outputs a path you have python on your system.
  ```
  sudo apt-get install python-pip --fix-missing
  sudo apt-get install python-dev
  sudo apt-get install python-pandas --fix-missing
  sudo apt-get install libpq-dev
  sudo apt-get install postgresql
  sudo apt-get install python-psycopg2
  sudo pip install django
  ```
  vagrant has synced folders so that you can use your computer's editor, while the files are on the VM instance.
  the 'rhizome' folder will show in the directory of your vagrant image.
  ```
  cd /vagrant
  git clone https://github.com/unicef/rhizome.git
  cd rhizome
  ```
  ===WARNING=== if you come across and error at this stage, it is due to the lack of memory on the virtual machine. The following commands will create a temporary swapfile to handle this installation in the meantime.
  ```
  - sudo dd if=/dev/zero of=/swapfile bs=1024 count=524288
  - sudo chmod 600 /swapfile
  - sudo mkswap /swapfile
  - sudo swapon /swapfile
  sudo pip install -r requirements.txt
  ```
  This may take a few minutes when running for the first time. Vagrant has more configuration to be done to access the postgres database.
  ```
  sudo vi /etc/postgresql/9.3/main/pg_hba.conf
  ```
  Edit the line:
  - local   all             postgres                                peer
  To:
  - local   all             postgres                                trust
  ```
  sudo /etc/init.d/postgresql reload
  createdb rhizome -U postgres
  sudo -u postgres psql rhizome
  CREATE USER djangoapp WITH SUPERUSER;
  ALTER USER djangoapp password 'w3b@p01i0';
  \q
  python manage.py syncdb
  ```
  Create a user name and password when prompted. dont forget it! Now we can run the server! congrats! This is the command for that:
  ```
  python manage.py runserver --nothreading
  ```
  - Node/Gulp configuration

  There is a version 6 but currently we are using:
  ```
  curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
  sudo apt-get install -y nodejs
  cd webapp/
  ```
  I had some permissions issues with the npm paths, run this command to set owner to current user
  ```
  sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}
  npm install
  npm install -g gulp
  npm install babel-register
  ```
  ```
  npm rebuild node-sass
  ```
  Initiate javascript serving
  //not functioning just yet.
  ```
  gulp dev
  ```

  Now you need 2 terminals running for the VM. One runs python server, the other runs gulp dev. You can have your text editor look at your local machine vagrant directory which syncs up to vagrant.

  done!

