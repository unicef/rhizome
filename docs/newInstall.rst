***********
New Install
***********


Creating a New Server on AWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Launching new EC2 Instance
===========================

  - Go to AWS -- Click "Ec2"
  - Launch Instance
      -> Ubuntu Server 14.04 LTS (HVM), SSD Volume Type
      -> type m4.large
    click "Configure Instance Details" -- NOT review and launch
    use the default selected here.. and click add storage
  - Storage Screen - Select 64-g, only one volumne needed, next click "tag Instance"
  - Tag Instance * whatever you want *
  - Configure Security Group
      -> Choose "Rhizome Prod Secuity Group"
  - Click "review and launch"

At this point your server should spin up .. now lets set up an Elastic IP

Elastic I.P.
===========

the point of an elastic I.P. is that you can assign mutliple machines to this address so that if you have to swap out the server, or spin up a new one, and it has a different i.p. you can simply associate the old instance to the elastic IP.

Once the server is "running" * ( see console.aws.amazon.com/ec2  ) go to "elastic IPS"
  - Allocate New Address -> this creates a publc I.P. that can be used via a domain name router like go datddy or network solutions.
  - Select the new instance by clicking the check box at the left
  - click actions >> asscoiate addres
      - choose the instance that you just created and click "associate"
  - For conveninve you will want to add the new "public IP" along wiht your ssh information to your ~/.ssh/config

  for instance

Host myServer
    User john
    HostName my.ip.adr.01
    IdentityFile ~/.ssh/some_key.pem

Once that it set up, you should be able to .ssh into the machine simply by running:

ssh myServer


Security Groups and Firewall
============================


Base System Packages
~~~~~~~

Basic Linux Packages
=====================

unzip -- `sudo apt-get install unzip`
pip -- `sudo apt-get install python-pip`
python-dev -- sudo apt-get install python-dev
  -> used by pandas installer

Apache
======

1. ssh into your machine and run:
  `sudo apt-get install apache2`

We will know that this task is complete, by hitting the server URL ( elastic IP for AWS ) in our brower and seeing the apache startup page.

Postgres
========

Installing
++++++++++

`sudo apt-get update`
`sudo apt-get install postgresql postgresql-contrib`

you shoudl see somethign like this:


Removing obsolete dictionary files:
 * No PostgreSQL clusters exist; see "man pg_createcluster"
Processing triggers for ureadahead (0.100.0-16) ...
Setting up postgresql-9.3 (9.3.11-0ubuntu0.14.04) ...
Creating new cluster 9.3/main ...
  config /etc/postgresql/9.3/main
  data   /var/lib/postgresql/9.3/main
  locale en_US.UTF-8
  port   5432

Now login to the postgres user with this command:

`sudo -i -u postgres`

then enter the psql shell by running:

`psql postgres`

now you should be able to create datases and roles.

Adding additional Linux Helper Packages
+++++++++++++++++++++++++++++++++++++

`sudo apt-get install python-psycopg2`
`sudo apt-get install libpq-dev`


Setting up Users and Creating the DB
++++++++++++++++++++++++++++++++++++

In the settings.py file that will be used by the application to handle sensitive information, branding and the management of packages, we will have a database host and user cofiguration.  So whatever you decide to call your database here, will be the information that is used by the application to access the Database.

1. Create a User:
  WHile in the postgres shell run:

  `CREATE ROLE djangoapp WITH PASSWORD 'mySecurePassword' LOGIN SUPERUSER;`

Make sure your password is secure and uses numbers, letters and special characaters

after exiting the psql shell with postgres user, Make sure this user was created by logging in like so :

`pql postgres -U djangoapp`

and follow the prompt for password.


If you see this error:
  -> psql: FATAL:  Peer authentication failed for user "djangoapp"

You likely will have to go to your pg_hba.conf file and make sure  local requests are handled with "md5" and NOT peer authentication.

see more here:
http://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge

you will want to reload postgres by running:
  --> sudo /etc/init.d/postgresql reload


For more on postgres, installing and debugging see here:
https://help.ubuntu.com/community/PostgreSQL


2. Create the database

CREATE DATABASE afg_eoc WITH OWNER djangoapp;

now make sure you can login to the database with:

psql afg_eoc -U djangoapp


NOTE:
- the config for postgres is /etc/postgresql/9.3/main
- the data for postgres is /var/lib/postgresql/9.3/main


3. create all of the necessary application files and diretories.
Create App Directory and File System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you look at fabfile.py at the root of the directory, it relies on a few directories to be in place in order to deploy and serve up the applicaion.

remote_work_path = '~/deploy/rhizome-work'
remote_backend_path = '/var/www/apps/rhizome/'
remote_frontend_path = '/var/www/apps/rhizome/webapp/public/static/'


Give ownership to the user that deploys your system.. so if your ssh config for the new remote server is

myUser

execute on your machine:

`sudo chown -R myUser /var/www/apps/rhizome/`

To make sure that you are able to create and access the above directores.

Finally create the "venv" path which is where we store all of the packages of application.

`mkdir /var/www/apps/rhizome/venv`




4. push up the code using the fabfile.

If you have the .ssh/config set up like above you can deploy by

1. entering the virtualenv with:
  source/venv/bin/activate

2. fab -H mySshConfig deploy


Check for failiures.. the execution should tell you at the bottom exactly what line failed.. so ssh into the server, run that command and see if you can track down the issue.
