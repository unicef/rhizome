Debugging the API
=================

When in the development environment, and you want to figure out what code, and or database queries are being executed on request, append the API call int eh browser with ``api_debug``.

This will open up the django debug toolbar and is a great place to start when trying to evaluate and tune performance

::

  http://localhost:8000/api_debug/api/v1/campaign/1/
