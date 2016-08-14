##########################
Creating the Documentation
##########################

To build this documentation, we will utilize Sphinx library for Python. Once the repository is cloned:

Building back-end documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When writing documentation for python code, edit the .rst files in the ``docs`` directory and follow the instructions

* cd docs
* make clean
* make html
* Docs files now available here: docs/_build/html

Building front-end documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* cd webapp
* gulp doc
* Docs files now available here: docs/_build/front-end/index.html


To push the documentation online and make them available publicly, merge all of your changes into the `gh-pages` branch, run `make clean && make html`` in the docs directory, then run

::

  git push origin gh-pages

After the push finishes, the updated documentation will be available at:

http://unicef.github.io/rhizome/

: )
