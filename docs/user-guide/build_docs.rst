##########################
Creating the Documentation
##########################

To build this documentation, we will utilize Sphinx library for Python. Once the repository is cloned:

Building back-end documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* cd docs
* make clean
* make html
* Docs files now available here: docs/_build/html

Building front-end documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* cd webapp
* gulp doc
* Docs files now available here: docs/_build/front-end/index.html