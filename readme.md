# Set up

## Prerequisites

1. [Python][] 2.7
2. [PIP][]
3. [Node][] >= 0.10.0
5. [PostgreSQL][]

## Building technical documentation

1. cd docs
2. make clean
3. make html
4. Docs files now available here: docs/_build/html

## Setting up the development environment

### Docker

Prerequisites

1. VirtualBox

Install Docker Machine. In Mac OS X you could install via `brew`

```
$ brew install docker-machine
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
$ docker build -t polio .
```
Run Docker instance

```
$ docker run -it -p 8000:8000 -v $PWD:/etc/polio polio /bin/bash
```

Set up database
```
$ python manage.py syncdb
$ python manage.py migrate
$ bash bin/build_db.sh
```

Start Django server
```
$ python manage.py runserver 0.0.0.0:8000
```

### Installing frontend dependencies

    $ npm install -g gulp 
    $ npm install

## running test ##

 - backend:
   $ python manage.py test --settings=polio.settings_test

- frontend:
   coming soon...


## Setting up the database

Our backend is built off of postgres.  In order to quickly install postgres and
get started on building the application, either install postgres with homebrew
or with http://postgresapp.com/.

The current settings file ( which you should edit especially if deploying to
a a remote server ;-) ) has the password for the django login to: w3b@p01i0
so feel free to set the djangoapp password to that when getting started!

    $ createuser --no-createdb --no-createrole --no-superuser --password djangoapp
    Password:
    $ createdb polio --owner djangoapp
    $ python manage.py migrate auth
    $ python manage.py syncdb
    $ python manage.py migrate

The password for the djangoapp user can be found in `settings.py`.

## Building the Front End

    $ gulp build

## Your Development Environment

In development you will need to run two operations *
     $ python manage.py runserver
     $ webpack --config webpack.config.dev.js --watch

After running these two commands in two separate terminals visit:

    http://localhost:8000

To see the application.

Note - Currently webpack only re-compiles javascript.. not css. If you make a
change to a css file you will nee to run 'gulp build' in order to see those
changes in your development envi.

We are moving towards a de-coupled application in which node will serve
all static pages, scripts and assets, but for now, this set up along with the
configurations provided by the [Django Webpack Loader
Package](https://github.com/owais/django-webpack-loader/) allows us to create
edits to our javascript and have the front end automatically rebuild them.

## Deploying ##

see fabfile.py for more info


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

# Gulp tasks

The default task runs `clean`, `copy`, `sass` and `browserify`, so that if
you simply execute

## dev

```
$ gulp dev
```

from the command line it will build the entire frontend for development.

## build

Compile the SASS, pack the JavaScript, and copy both, along with any fonts into
`static/`.

## package

Create `dist/rhizome.zip` which contains `requirements.txt` and all files


[Django]: https://djangoproject.com/
[Node]: http://nodejs.org/
[PIP]: https://pip.pypa.io/en/latest/
[PostgreSQL]: http://www.postgresql.org/
[Python]: http://python.org
[Virtualenv]: https://virtualenv.pypa.io/en/latest/
[Virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/
