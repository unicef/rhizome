# Set up ?//

## Prerequisites

1. [Node][] >= 0.10.0
2. VirtualBox

## Building technical documentation

1. cd docs
2. make clean
3. make html
4. Docs files now available here: docs/_build/html

## Coding Standards

##### Python
[PEP8](https://www.python.org/dev/peps/pep-0008/)

##### JavaScript
[Standard](http://standardjs.com/rules.html)

run `$ standard` from `webapp` folder to lint once, or `$ npm run standard` from the same folder to watch for changes.

## Setting up the development environment

### Docker

Prerequisites

  1. VirtualBox

for OSX:
```
$ brew update
$ brew tap phinze/homebrew-cask
$ brew install brew-cask
$ brew cask install virtualbox
```


[static-files]: https://docs.djangoproject.com/en/1.7/howto/static-files/)


Install Docker Machine. In Mac OS X you could install via `brew`

```
$ brew install docker-machine docker-compose
```
Initialise Docker environment

```
$ docker-machine create -d virtualbox dev
$ docker-machine start dev
```
Add `eval "$(docker-machine env dev)"` into .bashrc file

In Mac OS X, forward the port to host

```
$ VBoxManage controlvm dev natpf1 "django,tcp,127.0.0.1,8000,,8000"
```
Navigate to repository directory, de-comment Line.8 `ENV CHINESE_LOCAL_PIP_CONFIG="--index-url http://pypi.douban.com/simple --trusted-host pypi.douban.com"` to use Chinese pip mirror.

Run

```
$ docker-compose build && docker-compose up
```
Entry Docker instance

```
$ docker exec -it rhizome_rhizome_1 bash
```

The app is hosted at http://localhost:8000

### Installing frontend dependencies

Note - in order to do development on the front end within docker, you will need to install npm outside over your docker, ( see below ) and run `gulp dev` in order to for the front end build to watch and build new code.

Go to `webapp/` folder

```
$ npm install -g gulp
$ npm install
```

## Populating Data ##
Use the following script to pull the production database and sync it with your local

```
$ ./bin/sync_prod_data.sh
```


## Frontend development

The default `dev` task runs `clean`, `copy`, `sass` and `browserify`, so that if you simply execute:
```
$ gulp dev```
from the command line within the `webapp` folder it will build the entire frontend for development and watch for any changes.


## Running Tests ##

##### backend:
```
$ python manage.py test --settings=rhizome.settings_test
```

##### frontend:
```
$ cd webapp && gulp mocha
```

## Deploying ##

when spinning up a new ubuntu instance nstall the following dependencies :

```
$ sudo apt-get update
$ sudo apt-get install apache2 --fix-missing
$ sudo apt-get install unzip --fix-missing
$ sudo apt-get install python-pip --fix-missing
$ sudo apt-get install python-pandas --fix-missing
$ sudo apt-get install python-dev
$ sudo apt-get install libpq-dev
$ sudo apt-get install postgresql-9.3
$ sudo apt-get install python-psycopg2
$ sudo apt-get install libapache2-mod-wsgi
sudo apt-get install apache2 apache2 apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
```

to set up the db..

```
$ CREATE USER djangoapp WITH PASSWORD 'somepassword' SUPERUSER LOGIN;
```

then create the directory for the rhizome django app, and static files
```
$ sudo mkdir /var/www/apps/
$ sudo mkdir /var/www/apps/rhizome/
```

# Serving the Django Application with Apache.

You'll need to configure Apache and WSGI on whatever server you're deploying to,
and set up a PostgreSQL database for the application first. Make sure that
Apache is configured to use the
[prefork MPM](https://httpd.apache.org/docs/2.4/mpm.html); the worker and event
MPMs result in incorrect responses returned for requests when multiple requests
are made to the server.

For more information on deploying [Django][] applications, see the
[Django documentation](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/).

You will also want to set up apache to server the files in the /static and
/media directories.

### Serving Static files

The frontend files can be served statically by any webserver. Make sure that
the `STATIC_URL` setting in the backend's `settings.py` is set to wherever you
deploy the static files. ([Read more about static files in Django.][static-files])

[static-files]: https://docs.djangoproject.com/en/1.7/howto/static-files/)

## package

Create `dist/rhizome.zip` which contains `requirements.txt` and all files


[Django]: https://djangoproject.com/
[Node]: http://nodejs.org/
[PIP]: https://pip.pypa.io/en/latest/
[PostgreSQL]: http://www.postgresql.org/
[Python]: http://python.org
[Virtualenv]: https://virtualenv.pypa.io/en/latest/
[Virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/


## test slack integration
