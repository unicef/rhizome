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
   - The data acess layer was very poorly designed and though, and i've already done alot to help this, but there is alot more to do.  ( see more in the application overview )


Application Overview
~~~~~~~~~~~~~~~~~~~~

The current application has the idea of a "dashboard" but also has.  These dashboards are effective because they allow the user to filter their experience based on who they are and what they need to see.  This big difference between the current set up and what we need in the next weeks is that from a technical perspective **everything is a dashboard**.  The dashboard is the entry point for everything in the application and depending on the URL, we will render subcomponents as necessary.

Navigation
==========

The Navigation Drives the data flow of the application.  Each page that a user sees will be restricted by location_id and campaign_id.

**IMPORTANT** : We will need to change the current Url structure such that:

  - /datapoints/management-dashboard/Nigeria/2015/06/
becomes
  - /datapoints/management-dashboard/<location_id/<campaign_id>


The current behavior ( using the old URL ) requires the following logic:
   - indiscriminently fetch all regions in the database
   - Look up the ID for "Nigeria" or whatever fit the location variable in the URL
   - Make API calls for *datapoints* and *shapes* based on the id found in step 2.

The New behavior will be as follows:
   - Take the <location_id> from the URL
   - Pass <location_id> as the *parent_location_id* parameter to the location endpoint, *returning only direct children of existing location*
   - Pass <location_id> to the datapoint and geo and whatever other endpoint needed to render data on the page.

This means that whenever the user is viewing a particular page, the only data rendering on the page shoudl be relevant to the location in the url, as well as it's direct children.  This means for instance, when i am viewing "Bauchi Province" the API only needs to return Bauchi, it's children, and if it its lineage ( in this case that would be Nigeria) so that we can build the bread crumb.  Currently the API returns over 4000 regions, the application makes no use of almost all of these and the user experiences unnaceptable load times.

Also to note:  The campaign list that is rendered **is dependent on locations** that is you should not be able to select a campaign in pakistan if you are viewing data about nigeria.  This also means that *any time a location is changed in teh navigation* the application has to make another call to the campaign api.


Location Drop Down
~~~~~~~~~~~~~~~~~~

**VERY IMPORTANT** The application as it is designed currently sees huge performance hits because whenever a call is made, ALL REGIONS are returned.  We need to change this ASAP such that the API works with the application to acheive the following.

   - each request from the .js must pass a location_id.
   - If the URL has no location provided, pass 1 ( Nigeria ) and update the URL accordingly.
        > yes not pretty but Nigeria is our main use case, and i can gaurentee you that it will have ID = 1 ;)


Campaign Drop Down
~~~~~~~~~~~~~~~~~~

The campaign drop down must have the following structure.  Right now, unlike the location drop down which is a tree view, this is flat.  We need to enhance this so we can see the following:

- Nigeria
   - campaign_type_1
   - campaign_type_2
       - Campaign_type_2 in Month January 2015
       - Campaign_type_2 in Month February 2015
       - ...
   - campaign_type_3

The response for the api should allow the application to render this data without any front end data manipulation.  Currently, the api for Locations and indicatorsTree pivots the data in order to build the tree view.

Dashboard Drop Down
~~~~~~~~~~~~~~~~~~

> Static Dashboards
   > Management
   > District
   > Campaign Monitoring
> Custom Dashboards
  > dash_1
  > dash_2
  > dash_3


Home page
=========

  .. image:: http://s27.postimg.org/a7rr9qdlf/Rhizome_Home_Page_1.png
     :width: 600pt

Admin
=====

The Admin Module allows users to Add / Edit and View metadata required for the system.

The header at the top of the component switches the content type and renders by default the Index page.  The "Create New" button expands the top piece of the screen and renders the create form.

The index page has an edit link, which opens up a component underneath the admin index with the a form that allows for inline editing.  Any changes must be persisted to the database with the "submit" button.  If the API returns a success message, there should be a "saved" icon alert, and if there is an error, the front end should report this as part of teh form.

The index has a search functionality as well as the ability to sort and filter column values.

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

Dashboards
==========

As i mentioned earlier **everything is a dashboard**.  Lets review the flow of data when we land on a dashboard:

Currently The Management Dashboard Makes 21 API Calls.  This is outrageous and we should only need the following calls:

  -  /api/location/?parent_location_id=<x>
      - returns this location, it's lineage ( parent / grandparent etc ), and it's children
  -  /api/campaign/?id=<y>
      - Gets us the campaign object so we know the start/end date and display name
  -  /api/geo/?parent_location_id=<x>
      - Gets us the geojson to draw a map.
  -  /api/datapoints/  ( One of These Calls Per Chart Section )
      - ?location_id=<x>&campaign_id=<y>&indicator__in=<z>
      - ?location_id=<x>&campaign_start=<some_date>&campaign_end=<some_other_date>&&indicator__in=<z>
      - ?parent_location_id=<x>&campaign_id=<y>&indicator__in=<z>

in the case of the management dashboard, given the variety of data that appears on this dashboard, the calls to the /api/datapoint endpoint will remain the same, however i have already fixed the FE code so that the /location and /geo endpoint is hit only once.


Custom Dashboard Functionality
==============================

* Rendering Custom Dashboards is exactly the same as rending static dashboards *  See above for more information on this.  This section will be about creating and editing dashboards.

Data Model For Dashbaord Table:
    - id
    - Title
    - dashboard_json
    - layout_id
    - default_office_id

Creating a dashboard
~~~~~~~~~~~~~~~~~~~~

When the user clicks "create dashboard" they are taken to the screen below where they name the dashboard and pick **one of 4 layouts**.  On save, the application should POST - the title, the layout ID and the default office_id, as it has been selected in the drop down.

API Calls needed for this:
  - On page init -> GET /new_dashboard
        -> returns: the 3 layout objects, and all offices to populate the drop down at the lower right.
  - on save -> POST / dashboard {title:<x>,layout_id<y>,default_office_id=<z>}

  .. image:: http://s4.postimg.org/5h4ahvwkt/Custom_Dash_Landing_1.png
     :width: 600pt

See: http://rhizome.work/datapoints/dashboards/edit for the current version of this page.

Layout Details
~~~~~~~~~~~~~~

Each layout must be mobile, tablet and desktop responsive.  The current app renders nicely on a macbook, but tweaks when dealing with a desktop monitor.  It's critical that these layouts are clean and can show on any and all screens.

  - Layout #1: Basic (selected by default)
      - Very Similar to the management dashboard.  8 Charts , fluid layout
  - Layout #2: Heat Map Matrix
      - This is a way to create a heat map matrix ( see district dashboard ) for a custom set of indicators
      - See district dashboard: http://rhizome.work/datapoints/district-dashboard/Afghanistan/2014/11/
  - Layout #3: Map
      - This layout focuses on the Map on the left hand corner and provides three sections for custom chart on the right hand side.


Editing A Dashboard
~~~~~~~~~~~~~~~~~~~
When it comes to editing the "dashboard" there is actually very little functionality needed, as the vast amount of logic and functionality is handled in the chart builder.  The following basic functions are needed.

    - *Render Dashboard*:  with the ability to *click* into each chart component
    - *Select Chart*: User clicks on a chart section and this allows them to enter into the "chart edit" mode
    - *Update Title*: Ajax POST to save the title of a dashboard
    - *Naviation* : This inherits from the navigation used througout the application and will dynmically shift the data in the charts accordingly.

Note - once the default_office_id and layout_id have been set **they can not be changed**

Editing A Chart
~~~~~~~~~~~~~~~

see here: http://rhizome.work/datapoints/dashboards/edit/1/

Unlike the current dashboard builder, there will be no "create chart" method.  The charts will be pre-populated based on the layout_id and the user will have the ability to click in and alter the information provided.  By default, each chart within a particular layout will have a *chart_type* (chloroploeth, line, column, bar, pie, scatter plot ).

Assume that the user chose *layout-1* and clicked the *chart-8* component in the top right which by default is a map.

When the user clicks into a chart component, the see the following:

.. image:: http://s27.postimg.org/w6gr4eggj/Custom_Dash_Edit_Chart.png
   :width: 600pt


Note - Unlike the current set up in which there are navigation controls *within the chart builder* the user must instead use the campaign / location navigation at the top right of the screen to see the preview adapt accordingly.


Dashboard Json Specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently the dashboard builder posts "dashboard_json" which contains the definition of the dashboard.  The schema is as follows:

  - bla
      -bla
  - bla

Business Rules for Chart Types:
   - chloropleth Map accepts exactly 1 indicator.

Source Data Management
======================

This is complete, but needs a design treatment.  **THIS APP CAN EASILY BE EXTENDED TO HANDLE PERFORMANCE MANAGEMENT** so it would be good to get their designer on this.

Data Entry
==========

This is complete.

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


*Misc Rules*
  - No datapoint can be the result of data from two documents.  In a case where there is a location/campaign/indicator dupe between two


Aggregation and Calculation
===========================

- When a value in datapoints exists for location X, populate agg_datapoint with this value and NOT the aggregated values of X's children
- When a value in datapoint exists for a calculated indicator, chose this value as opposed the calculated value.
- When there is a recursive relationship bewteen "PART_OF_SUM" indicators, aggregate recursively, but allow for overrides ( as noted in the use case directly above. )

As an example

.. image:: http://s29.postimg.org/cvegbyfmf/imageedit_3_6644065823.png
   :width: 300pt

In the above case, the Total number of missed children is 19 because the value of 7 overrides the aggregated values.

ODK
~~~

4 Times Daily Run a job that does the following:

   - Look up in document_detail all of the documents that have been configured with the "ODK_FORM" and "ODK_HOST" configuration
   - For each of those strings
      - Execute a odk_breifcase.jar for that from
      - Find any new submissions by looking for meta-instance-ids that do not exist in the source_submission table for that documentation.
      - Append those rows to the submission table for taht documentation
      - Sync datapoints by running RefreshMaster for the document_id of the form.


Detailed API Specifications
===========================

Base
~~~~

All api calls require a location_id and campaign_id.  The below API name spaces inherit from what is in Base.py

*Headers*
    - 200, 400, 401, 500 etc.  Make sure that these are avaialable for FE team.

*Errors*

*Meta*
    - Form Data
    - Pagination
    -

geo
~~~
    - required parameter = parent_region_id
    - retuns shapes for the parent_region requested as well as all of it's children


source_data
~~~~~~~~~~~
      - POST document configurations, GET document data at various stages of ETL process
      - required params: document_id

manage
~~~~~~
    - add/edit/view campaigns, indicators, locations and datapoints.
    - required params: content_type
    - dashboard

New Functionality Needed
*/api/campaign/*
   - Requires Location_id and returns only campaigns for which there is data for that location.


Suggested Work Time Line
========================

Week of Oct 5
    - John: API Enhancements
    - Rouran / Sichu: refactor Data Access
    - Ang: Designing / scoping the performance management / source data app

Week of Oct 12
    - John: Admin Module
    - Rouran / Sichu: Custom dash
    - Ang: Designing / scoping the performance management / source data app

Week of Oct 19
    - John: Admin Module
    - Rouran / Sichu: Custom dash

Week of Oct 26
    - John : Implement New Styles From Jim
    - All hands on deck to make the application stable.
