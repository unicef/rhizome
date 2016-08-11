Software Stack
==============

#### Overview

The rhizome software stack is based off of:

-	Python ( Django, Postgres, Tastypie, Pandas )
-	Javascript ( React, Webpack, Gulp,  loadash, Refux )

The front end and back end applications are lightly coupled, and we are working to a place where there are two applications, one front end, and one back end that can be deployed separately.  Currently, the javascript is built using Gulp, and served up via django templates.

#### Deployment Environment

-	The application runs on a single Amazon EC2 Instance that contains the front end, the backend API and the database
-	The EC2 server runs Linux and uses Apache and WSGI to process web requests
-	The Database is postgres 9.4
-	The deployment process uses gulp along with Fabric in order to compile files, push to the remote host, build the files and run any scripts needed to effect change in the app

#### Development Environment
-	The development envi can either be set up manually using the python virtualenv by installing postgres locally or via Vagrant
-	Vagrant allows a new developer to install all of the dependencies of the application on a virtual machine in order to get new developers up quickly and
-	We use gulp, and are moving over to webpack in order to track and update changes to the front end

#### Testing and Continuous Integration
-	The front end uses the test framework for django and tastypie in order to validate requests and data man
-	The back end uses Mocha and chai to run tests and validate the javascript
-	The Both the front end and the back end have decent test coverage and are run with every push to every branch on travis
-	We use github for version control
