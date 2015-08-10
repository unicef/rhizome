# Set up

## Prerequisites

1. [Python][] 2.7
2. [PIP][]
3. [Node][] >= 0.10.0
4. [Ruby][] 2.0
5. [PostgreSQL][]

## Recommended

1. [Virtualenv][]
2. [Virtualenvwrapper][]

## Building technical documentation

1. cd docs
2. make clean
3. make html
4. Docs files now available here: docs/_build/html

## Setting up the development environment

### Virtual Environment (optional)

It is recommended that you create a virtual environment for Python. For more
information see the documentation on [virtualenv][] and [virtualenvwrapper][].

### Installing backend dependencies

    $ pip install -r requirements.txt

If you are not installing in a virtual environment, you may require root
privileges, so you'll need to `sudo` the above command.

### Installing frontend dependencies

    $ npm install
    $ npm install -g gulp bower
    $ bower install
    $ sudo gem install sass compass

You will also need to copy the sample webpack config to make the FE build work"

    $ cp webpack.config.dev.sample.js webpack.config.dev.js


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
    $ python manage.py syncdb
    $ python manage.py migrate

The password for the djangoapp user can be found in `settings.py`.

## Building the Front End

    $ gulp build

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

The default task runs `clean`, `fonts`, `browserify`, and `styles` so that if
you simply execute

    $ gulp

from the command line it will build the entire frontend for development.

## watch

Start a livereload server and watch SASS and JavaScript files for changes. Run
`gulp styles` whenever SASS changes, and `gulp browserify` whenever JavaScript
changes.

* In development you will need to run two operations *
   $ python manage.py runserver
   $ gulp watch

## build

Compile the SASS, pack the JavaScript, and copy both, along with any fonts into
`static/`.

## clean

Delete the `build/`, `dist/`, and `static/` directories.

## dist

Build the backend and frontend zip files. (Executes `dist-py` and `dist-ui`.)

## dist-py

Create `dist/uf04-backend.zip` which contains `requirements.txt` and all of the
Python and SQL files.

## dist-ui

Execute `collectstatic` and then zip up all of the files contained in `build/`.
The zip file is `dist/uf04-frontend.zip`.


[Django]: https://djangoproject.com/
[Node]: http://nodejs.org/
[PIP]: https://pip.pypa.io/en/latest/
[PostgreSQL]: http://www.postgresql.org/
[Python]: http://python.org
[Ruby]: https://www.ruby-lang.org/en/
[Virtualenv]: https://virtualenv.pypa.io/en/latest/
[Virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/
