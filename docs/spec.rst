*****************
Rhizome Tech Spec
*****************

Overview
=======

RhizomeDB is a UNICEF initiative to lead a culture change within the U.N. as to how data is collected, cleaned and used to make data driven decisions in the field and within management.

RhizomeDB is to have the following base functionality:
   - **Home Page**:  The Homepage can be looked at as a static dashboard that updates dynamically based on the user's permissions and  configurations.
   - **Admin**: Page to edit, view and create the necessary metadata in order to ingest data.  This icludes but is not limited to, locations, campaigns, indicators, users, roles and permissions.
   - **Source Data Management**: Page to upload and manage data sources from csv uploads, 3rd party apis, our ODK engine.  This part of the application will allow a user to configure 3rd party data source, upload new data, validate data from the people they manage, map necessary metadata and view the results of the upload.  The source data app is the groundwork for *Performance Management*
   - **Data Entry**: The Data Entry module gives the user direct access to the data that the system reports on.  The source data module above sends data through an ETL process with a number of steps of validation.  The data entry application essntially allows the user to shortcut these steps in order to alter data on demand.
   - **Static Dashboards**:  The application must provide 3 static dashboards, Management, NGA Campaign, and District.  These dashboards are complete and are to be the standard for the style and structure of the Custom Dashboard Module.
   - **Custom Dashboards**: The custom dashboard module allows permitted users to configure a dashboard to view data how they want, and for a particular set of indicators and locations.   Think of this as stripped down web version of Tableau.

Stack
~~~~~

We will have two environments, Test and Production ( C.I. After Nov 4th ) and each will need the following:
   - One DB Server Running Postgres
   - One Web Server


Deployment
~~~~~~~~~~

See fabfile.py

Refactoring
~~~~~~~~~~~

Note to Developers: ** We are not going to have time to de-couple these apps given our deadline **  Taking over the front end code has frankly been a nightmare and we are goign to need to do a pretty serious re-write in order to acheive what we need for November 4th.

However, we do have time to set ourselves up for this when our November deadline passes by **removing all references to django templates with the exception of the django admin.**  For November 4th We will continue to serve the static assets as well as the application logic with apache / modwsgi.

There are a few major refactoring efforts that are needed in the front end:
   - Application Must be a Single Page HTML App.
   - All references to vue must be removed.
   - Remove all dependencies on Django Templates with the exception of Login and Admin pages ( and the one .html file needed to run our javascript).
   - The data acess layer was very poorly designed and thoguht through, and i've already done alot to help this, but there is alot more to do.   see more in the [LINK ME] application overview.


Application Overview
~~~~~~~~~~~~~~~~~~~~

The current application has the idea of a "dashboard" but also have.  These dashboards are effective because they allow the user to filter their experience based on


Navigation
==========

Campaign Drop Down
~~~~~~~~~~~~~~~~~~

Location Drop Down
~~~~~~~~~~~~~~~~~~

Dashboard Drop Down
~~~~~~~~~~~~~~~~~~

Home page
=========

  .. image:: http://s27.postimg.org/a7rr9qdlf/Rhizome_Home_Page_1.png
     :width: 600pt

Admin
=====

The Admin Module allows users to Add / Edit and View metadata required for the system.

The header at the top of the component switches the content type and renders by default the Index page.  The "Create New" button expands the top peice of the screen and renders the create form.

The index page has an edit link, which opens up a component underneath the admin index with the a form that allows for inline editing.  Any changes must be persisted to the database with the "submit" button.  If the API returns a success message, there should be a "saved" icon alert, and if there is an error, the front end should report this as part of teh form.

The index has a search functionality as well as the ability to sort and filter column values.

* API Format *:
  - Index:
      -
  - POST:
      - New
      - Update


Index
~~~~~

.. image:: http://s30.postimg.org/dnzmymlq9/Rhizome_Admin_Index.png
   :width: 600pt

NOTE: the current ufadmin application calls data **FOR EVERY CONTENT TYPE** even though data is only needed for the content type that is selected.  To se this in action check out the inspector for http://rhizome.work/ufadmin/indicators

Create
~~~~~~

.. image:: http://s22.postimg.org/meahsttht/Rhizome_Admin_Create.png
   :width: 600pt


Edit
~~~~
.. image:: http://s10.postimg.org/f9k3aa2nd/Rhizome_Admin_Edit.png
   :width: 600pt


Content Type Behavior
~~~~~~~~~~~~~~~~~~~~
  - user
  - location
  - campaign
  - indicator
  - tag

Source Data API
~~~~~~~~~~~~~~~

Dashboards
=================

Custom
~~~~~~

Static
~~~~~~

Source Data Management
======================

Data Entry
==========
