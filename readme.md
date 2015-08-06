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

If you don't want to install `gulp` or `bower` globally (with the `-g` flag),
you can run them from the copies installed in `node_modules` by running

    $ ./node_modules/.bin/gulp
    $ ./node_modules/.bin/bower

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

## Building

    $ npm run build

This will compile the SASS, pack the JavaScript, and place both in the `static/`
directory along with all the fonts. If you have `gulp` in your `PATH`, you can
also run:

    $ gulp build

## Deploying

    $ npm run dist

This will build the frontend, collect all of Django's static files, and then
create zip files for the frontend and backend in the `dist/` directory:

1. uf04-backend.zip
2. uf04-frontend.zip

Each contains the source necessary to deploy the backend and frontend,
respectively. These can be copied to whatever server is hosting each of those
components.

The JavaScript and CSS in the frontend zip file is minimized.

If you have `gulp` in your `PATH`, you can also run:

    $ gulp dist

### Deploying the backend

You'll need to configure Apache and WSGI on whatever server you're deploying to,
and set up a PostgreSQL database for the application first. Make sure that
Apache is configured to use the
[prefork MPM](https://httpd.apache.org/docs/2.4/mpm.html); the worker and event
MPMs result in incorrect responses returned for requests when multiple requests
are made to the server.

For more information on deploying [Django][] applications, see the
[Django documentation](https://docs.djangoproject.com/en/1.7/howto/deployment/).

#### Build the application and copy it to the server

    $ npm run dist
    $ scp dist/*.zip <server>

#### Unzip the application files

    $ ssh <server>
    $ unzip -o uf04-backend.zip -d <path/to/python/docroot>
    $ unzip -o uf04-frontend.zip -d <path/to/static/files/docroot>
    $ chown -R <apache user> <path/to/python/docroot>
    $ chown -R <apache user> <path/to/static/files/docroot>

#### Update Python dependencies

    $ cd <path/to/python/docroot>
    $ pip install -r requirements.txt

#### Update the database

    $ python manage.py syncdb --migrate

You may need to use the `--settings` option for `manage.py` if your
`settings.py` is not in `PYTHONPATH`.

    $ bash bin/build_db.sh

You will need to make sure that whatever user you are executing `build_db.sh` as
is recognized by the PostgreSQL database and is the owner of the views being
modified by the script.

Finally, you'll need to restart Apache.

### Deploying the frontend

The frontend files can be served statically by any webserver. Make sure that
the `STATIC_URL` setting in the backend's `settings.py` is set to wherever you
deploy the static files. ([Read more about static files in Django.][static-files])

[static-files]: https://docs.djangoproject.com/en/1.7/howto/static-files/)

# Gulp tasks

The default task runs `clean`, `fonts`, `browserify`, and `styles` so that if
you simply execute

    $ gulp

from the command line it will build the entire frontend for development.

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

## watch

Start a livereload server and watch SASS and JavaScript files for changes. Run
`gulp styles` whenever SASS changes, and `gulp browserify` whenever JavaScript
changes.

[Django]: https://djangoproject.com/
[Node]: http://nodejs.org/
[PIP]: https://pip.pypa.io/en/latest/
[PostgreSQL]: http://www.postgresql.org/
[Python]: http://python.org
[Ruby]: https://www.ruby-lang.org/en/
[Virtualenv]: https://virtualenv.pypa.io/en/latest/
[Virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/
