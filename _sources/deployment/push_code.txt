Pushing Code
============

Deploying
---------

When pushign code to a server, use the ``fabfile``

Set up an ssh configuration in ~/.ssh/config

::
  host target-server
    HostName 12.3.45.6
    user myUser
    IdentityFile ~/.ssh/myKey.pem

and run

::
  fab -H target-server deploy


Releasing to Master
-------------------

All development work should be done on the ``dev`` branch.

When the code and functionality on the test server has been properlly vetted, and we are ready for a production release, follow these steps.

::
  $ git checkout master
  $ git merge dev
  $ git tag -a vx.y.z
  $ git push origin master
  $ git push origin tags
  $ fab -H prod_server deploy

note that there is a hook in github that will not allow you to push to master until the commit that you are trying to push has passed continuous integration 
