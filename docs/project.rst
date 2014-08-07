*******
Project
*******

Functionality:
=============================================

    - GET and POST api methods that allow for retrieval, and insert of
      datapoints
    - Basic CRUD (create, read , update, delete) front end interface
    - Basic Search functionality which allows users to find datapoints with
      a region, indicator, campaign and / or created by attributes
    - Permissioning for Create, Update, Delete
    - Audit Functionality using django-simple-history
      (https://github.com/treyhunner/django-simple-history)

Dependencies:
=============================================

    - coverage (3.7.1)
    - Django (1.6.5)
    - django-guardian (1.2.4)
    - django-simple-history (1.4.0)
    - django-stronghold (0.2.6)
    - django-tastypie (0.11.1)
    - psycopg2 (2.5.3)
    - South (1.0)
    - Sphinx (1.2.2)


Permissions
====================
    - The permissioning system is based mainly on django's authentication
      system with an extension using django-gaurdian that allows for object
      level permissions.
    - Django has no built in resources for creating "view" permissions,
      currently "view" permissions are handled by django gaurdian.

    PERMISSIONS SCHEMA
        - auth_permissions
        - auth_user
        - auth_group
        - auth_user_permission
        - auth_group_permission
