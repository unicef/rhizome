# Setting up the developer environment

### Set up with Vagrant(optional, recommended)
Utilizing a virtual machine we can spin up a fresh, clean, and isolated developer environment. Visit the [Vargant](https://www.vagrantup.com/) website to download it. Another dependency might be required - [Virtualbox](https://www.virtualbox.org/wiki/Downloads), any of these following steps fail.
* Commands to follow(keep in mind this is the installation order for ubuntu operating system):
  ```bash
  // - Python/Django/Postgres configuration
  vagrant init ubuntu/trusty64
  vagrant up --provider virtualbox
  vagrant ssh
  sudo apt-get update
  sudo apt-get install -y
  sudo apt-get install unzip --fix-missing
  sudo apt-get install git-all
  //you may already have python. you can check with the following command:
  which python
  //if this outputs a path you have python on your system.
  sudo apt-get install python-pip --fix-missing
  sudo apt-get install python-dev
  sudo apt-get install python-pandas --fix-missing
  sudo apt-get install libpq-dev
  sudo apt-get install postgresql-9.3 //if you have database creation issues I recommend 'sudo apt-get install postgresql-9.3'
  sudo apt-get install postgres-xc-client
  sudo apt-get install postgres-xc
  sudo apt-get install python-psycopg2
  sudo pip install django
  //cd to your code/repo related folder.
  git clone https://github.com/unicef/rhizome.git
  cd rhizome
  //----WARNING---- if you come across and error at this stage, it is due to the lack of memory on the virtual machine. The following commands will create a temporary swapfile to handle this installation in the meantime.
  - sudo dd if=/dev/zero of=/swapfile bs=1024 count=524288
  - sudo chmod 600 /swapfile
  - sudo mkswap /swapfile
  - sudo swapon /swapfile
  - sudo pip install -r requirements.txt
  // this may take a few minutes when running for the first time.
  // Vagrant has more configuration to be done to access the postgres database.
  sudo vi /etc/postgresql/9.3/main/pg_hba.conf
  // edit the line:
  - local   all             postgres                                peer
  // to:
  - local   all             postgres                                trust
  sudo /etc/init.d/postgresql reload
  createdb rhizome -U postgres
  sudo -u postgres psql rhizome
  CREATE USER something WITH SUPERUSER;
  ALTER USER rhizome password 'w3b@p01i0';
  \q
  python manage.py syncdb
  //create a user name and password when prompted. dont forget it!
  //now we can run the server! congrats! this is the command for that:
  python manage.py runserver --nothreading
  // - NodeJS configuration
  // there is a version 6 but currently we are using:
  curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
  sudo apt-get install -y nodejs
  cd webapp/
  sudo npm install -g gulp
  npm install
  // this will take a few minutes.
  // if you encounter an error run when attempting to run 'gulp dev' run this:
  npm rebuild node-sass
  // initiate javascript serving
  gulp dev
  ```