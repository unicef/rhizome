#############
Running Tests
#############

Back-end
~~~~~~~~

::

  python manage.py test --settings=rhizome.settings_test

And if you want to see the test coverage in pretty html form run:

::

  coverage run manage.py test --settings=rhizome.settings.test
  coverage html --omit='*venv/*,*migrations/*,*admin*,*manage*,*wsgi*,*__init__*,*test*,*settings*,*url*' -i

the check the `<repo_dir>/htmlcov/index.html` for the html version of the code coverage report

Front-end
~~~~~~~~~
::

  cd webapp && gulp mocha
