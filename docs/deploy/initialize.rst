#########
Deploying
#########

Installing Dependencies on the Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When spinning up a new ubuntu instance nstall the following dependencies:
::

  sudo apt-get update
  sudo apt-get install apache2 --fix-missing
  sudo apt-get install unzip --fix-missing
  sudo apt-get install python-pip --fix-missing
  sudo apt-get install python-pandas --fix-missing
  sudo apt-get install python-dev
  sudo apt-get install libpq-dev
  sudo apt-get install postgresql-9.3
  sudo apt-get install python-psycopg2
  sudo apt-get install libapache2-mod-wsgi
  sudo apt-get install apache2 apache2 apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

To set up the database:
::

  CREATE USER djangoapp WITH PASSWORD 'somepassword' SUPERUSER LOGIN;

Then create the directory for the rhizome django app, and static files:
::

  sudo mkdir /var/www/apps/
  sudo mkdir /var/www/apps/rhizome/


Serving the Django Application with Apache.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You'll need to configure Apache and WSGI on whatever server you're deploying to, and set up a PostgreSQL database for the application first. Make sure that Apache is configured to use the `prefork MPM <https://httpd.apache.org/docs/2.4/mpm.html>`_; the worker and event MPMs result in incorrect responses returned for requests when multiple requests are made to the server.

For more information on deploying applications, see the `Django documentation <https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/>`_.

You will also want to set up apache to server the files in the /static and /media directories.

Serving Static files
++++++++++++++++++++

The frontend files can be served statically by any webserver. Make sure that
the `STATIC_URL` setting in the backend's `settings.py` is set to wherever you
deploy the static files. ([Read more about static files in Django.][static-files])

`static-files <https://docs.djangoproject.com/en/1.7/howto/static-files/>`_

Packaging Files for Server
~~~~~~~~~~~~~~~~~~~~~~~~~~
We now gather all the files required for the apache server to send out to the users:
::

  cd webapp
  npm run package

This will create a new file under the dist/ folder `rhizome.zip`. Now we move this file to the server and unzip. into the /var/www/apps/rhizome/ folder. To install all of the required dependencies we run:
::

  pip install -r requirements.txt