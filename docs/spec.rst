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
   - One Web Server Running django / apache
   - One ODK Server Running ODK sync 4 Times Daily

Total: 6 Servers @
Average Data Transfer cost: ??


Refactoring
~~~~~~~~~~~

Note to Developers: **We are not going to have time to de-couple these apps given our deadline**  Taking over the front end code has frankly been a nightmare and we are goign to need to do a pretty serious re-write in order to achieve what we need for November 4th.

However, we do have time to set ourselves up for this when our November deadline passes by **removing all references to django templates with the exception of the django admin.**  For November 4th We will continue to serve the static assets as well as the application logic with apache / modwsgi.

There are a few major refactoring efforts that are needed in the front end:
   - Application Must be a Single Page HTML App.
   - All references to vue must be removed.
   - Remove all dependencies on Django Templates with the exception of Login and Admin pages ( and the one .html file needed to run our javascript).
   - The data acess layer was very poorly designed and though, and i've already done alot to help this, but there is alot more to do.   see more in the [LINK ME] application overview.


Application Overview
~~~~~~~~~~~~~~~~~~~~

The current application has the idea of a "dashboard" but also have.  These dashboards are effective because they allow the user to filter their experience based on who they are and what they need to see.  This big difference between the current set up and what we need in the next weeks is that from a technical perspective **everything is a dashboard**.  The dashboard is the entry point for everything in the application and depending on the URL, we will render subcomponents as necessary.

The layout of the .js should be as follows:

webapp
  > src
     > component


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

*API Format *:
~~~~~~~~~~~~~~
  - GET:
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
~~~~~~~~~~~~~~~~~~~~~
  - user:
      -> subcomponents: location_permissions
  - location
        -> subcomponents: associated_mappings
  - campaign
        -> subcomponents: associated_mappings
  - indicator
        -> subcomponents: associated_mappings, tags, calculations, bounds
  - tag
        -> subcomponents: tags ( view/add indicators for tag)

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

Back End Business Rules and ETL
===============================

ETL - Source Data Backend
~~~~~~~~~~~~~~~~~~~~~~~~~
  .. image:: http://s27.postimg.org/hh2retykz/rhizome_data_flow.png
     :width: 600pt

1. A unique source (ODK form, csv upload, .shp file) has a corresponding source_dic_id as well as a pointer to the raw data stored on the file system.
2. A user specifies configurations for this sources, for instance, the unique_id column, region and campaign columns.
3. Based on the “document_details” the raw data is translated into source_submissions.  The source_submission table has a document_id, and the raw json of the submission.
4. Based on the configurations, source_object_maps are created and queued up for a user to map.  This table contains {content_type, source_object_code, master_obj_id}. Note, if meta data mapped from other source_docs, the user need not map them again.
5. Based on the metadata mappings, submissions are transformed into datapoints with their corresponding master object ids.  This table does not have any unique indexes.,
6. A user can validate, invalidate and resolve conflicts from the source data
7. Based on validation and business logic, chose valid create datapoitns from above table. doc_datapoint and datapoint  same exact except datapoint has a unique index on region_id, campaign_id, location_id
8. Datapoint are our main source of truth, data stored and collected at the lowest level possible.  In step 8 datapoints are aggregated and values created for all parents recursively.
9. Based on metadata about indicator calculation definitions, we create new indicators based on calculations from the raw and aggregated values. For instance, % of missed children due to refusal.
10. The datapoint API and the application as a whole use campaign_id and region_id as parameters to initialize a dashboard.  So, the datapoints model here is transformed so that *[ region_id, campaign_id, indicator_id, value ]* --- becomes --->  *[ region_id, campaign_id, indicator_json ]*


ODK
~~~

Detailed API Specifications
===========================

Base
~~~~

All api calls require a location_id and campaign_id.  The below API name spaces inherit from what is in Base.py

source_data
~~~~~~~~~~~
      - POST document configurations, GET document data at various stages of ETL process
      - required params: document_id

manage
~~~~~~
    - add/edit/view campaigns, indicators, locations and datapoints.
    - required params: content_type
    - dashboard

Data Entry
~~~~~~~~~~
  - see DataEntryResource
