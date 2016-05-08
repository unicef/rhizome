# Setting up the developer environment

### Set up with Vagrant(optional, recommended)
Utilizing a virtual machine we can spin up a fresh, clean, and isolated developer environment. Visit the [Vargant](https://www.vagrantup.com/) website to download it. Another dependency might be required - [Virtualbox](https://www.virtualbox.org/wiki/Downloads), any of these following steps fail.
* Commands to follow(keep in mind this is the installation order for ubuntu operating system):
  - Python/Django/Postgres configuration
  ```bash
  vagrant init ubuntu/trusty64
  ```
  In the 'Vagrantfile' add the following lines to your configuration:
  ```
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end
  ```
  This will allow you to connect to your python server and also upgrade the memory to allow properly installation of pandas.
  ```
  vagrant up --provider virtualbox
  vagrant ssh
  sudo apt-get update
  sudo apt-get install -y
  sudo apt-get install git-all
  ```
  You may already have python. you can check with the following command:
  ```
  which python
  ```
  If this outputs a path you have python on your system.
  let's download pip install for python: (as per python recommended download method)
  ```
  curl -O https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  sudo apt-get install python-pandas --fix-missing
  sudo apt-get install libpq-dev
  sudo apt-get install postgresql
  ```
  vagrant has synced folders so that you can use your computer's editor, while the files are on the VM instance.
  the 'rhizome' folder will show in the directory of your vagrant image.
  ```
  cd /vagrant
  git clone https://github.com/unicef/rhizome.git
  cd rhizome
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
  CREATE USER djangoapp WITH SUPERUSER PASSWORD 'w3b@p01i0';
  \q
  python manage.py syncdb
  ```
  Create a user name and password when prompted. dont forget it! Now we can run the server! congrats! This is the command for that:
  ```
  python manage.py runserver --nothreading
  ```

### Local setup with virtualenv
We can also install locally.
- Download git to your local machine.
  ```
  cd /directory/of/yours
  git clone https://github.com/unicef/rhizome.git
  ```
  let's download pip install for python: (as per python recommended download method)
  ```
  curl -O https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  cd rhizome
  sudo pip install virtualenv
  sudo apt-get install python-dev
  sudo apt-get install libpq-dev
  sudo apt-get install postgresql
  virtualenv venv
  source venv/bin/activate

  pip install -r requirements.txt
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
  CREATE USER djangoapp WITH SUPERUSER PASSWORD 'w3b@p01i0';
  \q
  python manage.py syncdb
  ```
  Create a user name and password when prompted. dont forget it! Now we can run the server! congrats! This is the command for that:
  ```
  python manage.py runserver --nothreading
  ```

#### Node/Gulp configuration
  ```
  cd ~/
  curl -L http://npmjs.org/install.sh | sudo sh
  cd /vagrant/rhizome/webapp
  ```
  If you come across any permission issues trying running this command:
  ```
  sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}
  ```
  ```
  npm install -g npm@latest
  npm install -g babel-eslint@4.1.6
  npm install
  npm install -g gulp
  ```
  ```
  npm rebuild node-sass
  ```
  Initiate javascript serving
  ```
  gulp dev
  ```

  Now you need 2 terminals running for the VM. One runs python server, the other runs gulp dev. You can have your text editor look at your local machine vagrant directory which syncs up to vagrant.

  done!