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

If you don't want to install `gulp` or `bower` globally (with the `-g` flag),
you can run them from the copies installed in `node_modules` by running

  $ ./node_modules/.bin/gulp
  $ ./node_modules/.bin/bower

## Setting up the database

  $ createuser --no-createdb --no-createrole --no-superuser --password "w3b@p01i0" djangoapp
  $ createdb --owner djangoapp polio
  $ python manage.py syncdb
  $ python manage.py migrate

## Building

  $ gulp

## Deploying

  $ gulp dist

`gulp dist` will create two zip files in the `dist/` directory:

1. uf04-backend.zip
2. uf04-frontend.zip

Each contains the source necessary to deploy the backend and frontend,
respectively. These can be copied to whatever server is hosting each of those
components.

The JavaScript and CSS in the frontend zip file is minimized.

### Deploying the backend

For more information on deploying [Django][] applications, see the [Django
documentation](https://docs.djangoproject.com/en/1.7/howto/deployment/).

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

## browserify

Lint the JavaScript (by running `scripts`), then pack all of the project's code
into a single `main.js` file in the `static` directory

## build

Execute `fonts`, `browserify`, and `styles`.

## clean

Delete the `build/`, `dist/`, and `static/` directories.

## collectstatic

Execute `build` and then run `python manage.py collectstatic` to place all the
project static files into a `build/` directory for building the frontend zip
file.

## dist

Build the backend and frontend zip files. (Executes `dist-py` and `dist-ui`.)

## dist-py

Create `dist/uf04-backend.zip` which contains `requirements.txt` and all of the
Python and SQL files.

## dist-ui

Execute `collectstatic` and then zip up all of the files contained in `build/`.
The zip file is `dist/uf04-frontend.zip`.

## fonts

Collect all font files found in `bower_components`, flatten the directory
structure, and place them in `static/fonts`.

## livereload

Start a [livereload][] server listening on port 35729. The task watches all
files in the `static/` for changes to update connected browsers for easier
development.

[livereload]: http://livereload.com/

## scripts

Lint all of the JavaScript.

## styles

Compile the SASS and place the files in `static/css`.

## test

Execute unit tests on the JavaScript.

There are currently no unit tests

## watch

Start a livereload server and watch SASS and JavaScript files for changes. Run
`gulp styles` whenever SASS changes, and `gulp browserify` whenever JavaScript
changes.

# PERMISSIONS
user can be in multiple groups

## GROUPS
- general data entry (add datapoints)
- advanced data entry (update and delete data points)
- regional view (view all data points in your regional office)
- advanced view ( view all data points in all regions )
- superuser (everything under the sun)

[Django]: https://djangoproject.com/
[Node]: http://nodejs.org/
[PIP]: https://pip.pypa.io/en/latest/
[PostgreSQL]: http://www.postgresql.org/
[Python]: http://python.org
[Ruby]: https://www.ruby-lang.org/en/
[Virtualenv]: https://virtualenv.pypa.io/en/latest/
[Virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/
