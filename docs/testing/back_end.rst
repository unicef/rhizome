Backend Testing
================


Running Tests
-------------

::

  python manage.py test --settings=rhizome.settings_test

And if you want to see the test coverage in pretty html form run:

::

  coverage run manage.py test --settings=rhizome.settings.test
  coverage html --omit='*venv/*,*migrations/*,*admin*,*manage*,*wsgi*,*__init__*,*test*,*settings*,*url*' -i

the check the `<repo_dir>/htmlcov/index.html` for the html version of the code coverage report


Writing Tests
-------------

The idea here is that, we use the unit tests to ensure that the functionality we have built works appropriately.

So for instance, if you want to POST to an indicator, we have a test post to the indicator API with a particular data set.

If later, we change the data model for indicators, such that we remove a field, if we don't fix the test, or the API, then the tests will break and we will not be able to push code to any servers!

See more below

Backend Test Source Code
------------------------

.. automodule:: rhizome.tests
    :members:
