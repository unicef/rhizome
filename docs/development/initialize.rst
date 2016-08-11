
Setting Up the Development Environment
------------------------------------

Back-end setup
++++++++++++++

There are two options to set up the developer environment for the backend, one is through a virtual machine. The second option would be to configure a virtualenv.

Set up with Vagrant(optional, recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Utilizing a virtual machine we can spin up a fresh, clean, and isolated developer environment. Visit the `Vagrant <https://www.vagrantup.com/>`_ website to download it. Another dependency might be required - `Virtualbox <https://www.virtualbox.org/wiki/Downloads>`_, any of these following steps fail.

Python/Django/Postgres configuration
####################################

Commands to follow(keep in mind this is the installation order for ubuntu operating system):

* In your terminal go to a new folder to keep your vagrant image and files within and start with the following:

::

  vagrant init ubuntu/trusty64

* In the 'Vagrantfile' add the following lines to your configuration(unless your vagrant config has other config!):

::

  Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.network "private_network", ip: "192.168.77.77"
    config.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "2048"]
    end
  end

This will allow you to connect to your python server and also upgrade the memory to allow properly installation of pandas.
::

  vagrant up --provider virtualbox
  vagrant ssh
  sudo apt-get update
  sudo apt-get install -y git-all

Note: You may already have python. you can check with the following command:
::

  which python

If this outputs a path you have python on your system.
* Let's download pip to install our dependencies for python: (as per python recommended download method)

::

  curl -O https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  sudo apt-get install -y python-pandas --fix-missing
  sudo apt-get install -y libpq-dev
  sudo apt-get install -y postgresql

Vagrant has synced folders so that you can use your computer's editor, while the files are on the VM instance.
The 'rhizome' folder will show in the directory of your vagrant image.
::

  cd /vagrant
  git clone https://github.com/unicef/rhizome.git
  // rhizome folder will now show in your Mac/Windows folder as well now where your Vagrant image is located/
  cd rhizome
  sudo pip install -r requirements.txt

This may take a few minutes when running for the first time. Vagrant has more configuration to be done to access the postgres database.
::

  sudo vi /etc/postgresql/9.3/main/pg_hba.conf

* Edit the line:

local   all             postgres                                peer

* To:

local   all             postgres                                trust
::

  sudo /etc/init.d/postgresql reload
  createdb rhizome -U postgres
  sudo -u postgres psql rhizome
  CREATE USER djangoapp WITH SUPERUSER PASSWORD 'w3b@p01i0';
  \q
  python manage.py syncdb

* Create a user name and password when prompted. dont forget it! Now we can run the server. This is the command for that:

::

  python manage.py runserver --nothreading 192.168.77.77:8000


Local setup with virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python/Django/Postgres configuration
####################################

We can also install locally rather than virtual machine, within a virtual environment.
* Download git to your local machine.

::

  cd /directory/of/yours
  git clone https://github.com/unicef/rhizome.git

Let's download pip install for python(as per python recommended download method):
::

  curl -O https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  cd rhizome
  sudo pip install virtualenv
  sudo apt-get install -y python-dev
  sudo apt-get install -y libpq-dev
  sudo apt-get install -y postgresql
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt

This may take a few minutes when running for the first time. Vagrant has more configuration to be done to access the postgres database.
::

  sudo vi /etc/postgresql/9.3/main/pg_hba.conf

* Edit the line:

::

  local   all             postgres                                peer

* To:

::

  local   all             postgres                                trust

::

  sudo /etc/init.d/postgresql reload
  createdb rhizome -U postgres
  sudo -u postgres psql rhizome
  CREATE USER djangoapp WITH SUPERUSER PASSWORD 'w3b@p01i0';
  \q
  python manage.py syncdb

* Create a user name and password when prompted. dont forget it! Now we can run the server! congrats! This is the command for that:

::

  python manage.py runserver --nothreading 192.168.77.77:8000

Front-end setup
^^^^^^^^^^^^^^^

Gulp configuration
##################

First install node
::

  cd ~/
  curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
  sudo apt-get install -y nodejs

Now install npm
::

  curl -L http://npmjs.org/install.sh | sudo sh
  cd /vagrant/rhizome/webapp

Run this command to avoid permissions issues with npm directories:
::

  sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}

  npm install -g npm@latest
  npm install -g babel-eslint@4.1.6

Note: npm installation are sometimes fragile. If you come across any errors please try to research them via npm resources.
::

  npm install -g gulp
  npm install

  npm rebuild node-sass

initiating the watch and building of the JavaScript for the front end:
::

  gulp dev

Now you need 2 terminals running for the VM. One runs python server`python manage.py runserver --nothreading`, the other runs `gulp dev`. You can have your text editor look at your local machine vagrant directory which syncs up to vagrant.

done!
