ODK
===


**ODK Overview**

ODK (Open Data Kit) is a platform that allows users to post data via their android devices to a remote data store.

There are 4 main components to ODK:

* `Build <http://opendatakit.org/use/build/>`_  - a tool to build data collection forms or surveys

  * The output of this tool is XML
  * Also available for more complex forms is XLSForm
* `Collect <http://opendatakit.org/use/collect/>`_ - An Android app that allows user to input data on a mobile device using the forms built with Build or XlSForm and send it to a server
* `Aggregate <http://opendatakit.org/use/aggregate/>`_  - The backend system where the collected data is stored and visualized with a simple web page.



In Addition the following ODK products are also

* `ODK Brief Case <http://opendatakit.org/use/briefcase/>`_ -  Tool to push and pull data from ODK Aggregate
* `Enekto Web Forms <http://opendatakit.org/2014/02/odk-aggregate-1-4-1-with-enketo-webforms-integration-is-now-available/>`_ -  Not sure about this yet, but this may be a way to build a web form for the Android input forms used in Collect

.. image:: http://oi60.tinypic.com/68ag3p.jpg

**Tutorials and Resources**

https://www.google.com/earth/outreach/tutorials/odk_gettingstarted.html

**Moving Forward**

There are two major directions that we can go with this:

* Implement Process that constant checks the App Engine Instance for new data, transforms it and loads into our backend system.
* Directly hookup our backend system with the ODK Collect application
