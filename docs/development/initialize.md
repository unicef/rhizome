# Setting up the developer environment

### Set up with Vagrant(optional, recommended)
Utilizing a virtual machine we can spin up a fresh, clean, and isolated developer environment. Visit the [Vargant](https://www.vagrantup.com/) website to download it. Another dependency might be required - [Virtualbox](https://www.virtualbox.org/wiki/Downloads), any of these following steps fail.
* Commands to follow:
  ```bash
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
  sudo apt-get update python
  sudo apt-get install python-pip --fix-missing
  sudo apt-get install python-dev
  sudo apt-get install python-pandas --fix-missing
  sudo apt-get install libpq-dev
  sudo apt-get install postgresql-9.3
  sudo apt-get install python-psycopg2
  sudo pip install django
  //cd to your code/repo related folder.
  git clone https://github.com/unicef/rhizome.git
  cd rhizome
  sudo pip install -r requirements.txt
  // this may take a few minutes when running for the first time.
  ```