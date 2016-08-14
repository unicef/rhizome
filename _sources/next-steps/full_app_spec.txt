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

We will have two environments, Test and Production and each will need the following:
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
      -> subcomponents: location_responsibilty
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

Custom Dashboard Functionality
==============================


Creating a dashboard
~~~~~~~~~~~~~~~~~~~~

New Data Models Needed:
  - chart_type
  - chart_type_to_indicator
  - layout_id

When the user clicks "create dashboard" they are taken to the screen below where they pick one indicator to get started.

The user must first pick the country, and then the indicator.

.. image:: http://s28.postimg.org/pux4cy5st/ang_li_dash_01.png
   :width: 600pt

After picking the country, the indicator drop down should update so that we can filter to data that exists in that country.

.. image:: http://s22.postimg.org/s30fwsp1d/ang_li_dash_02.png
   :width: 600pt

 - Technical Note: you will need to pass a ?office_id=<x> parameter to the indicator API when it is selected.  The indicator drop down shoudl be disabled until a country is selected.


NOTE: BELOW NEEDS WIREFRAME

Next the User will pick the locations that they would like to visualize.  The location can either be:
   - static: there is no location drop down that allows you to chose different location_ids
   - dynamic: for one chart, the locations can be filtered using the location title menu that we use to navigate through current dashboards.

Note: unlike the current dashboard schema in which the dashboard is bound by location, in the new set up, the user will be able to control the location of each chart.

In addition at this step the user will be able to choose if they want to see on their visualization:
   - Just this location
   - Sub Locations of Selected.
   - Choose multiple Locations.

So for instance, if you selected Nigeria, and wanted to see a bar chart for all of teh provinces, you would simply select "Show Sub Locations of Selected."

If however you wanted to look at 5 specific districts in Pakistan, you would click "choose multiple locations", select the 5 you wanted to visualize and click next.

NOTE: THE ABOVE NEEDS WIREFRAMES

On the next screen the user must pick the type of chart that they would like to visualize.

Based on the charty_type_id returned when selecting the indicator, the user will the have the option to pick from the chart types that the system allows for the above indicator.

.. image:: http://s17.postimg.org/keksqydov/ang_li_dash_03.png
   :width: 600pt

After choosing the chart type, the user is taken to the existing chart builder / chart preview screen as shown below.

.. image:: http://s8.postimg.org/imv8a40w5/ang_li_dash_05.png
   :width: 600pt

In addition to the chart builder functionality the next screen the user should see the indicator plotted using the mechanism selected, however with this control, they will be able to perform the following operations:
  - add additional indicators to the visualization ( depending on the chart type )
  - select a time frame - start_date, end_date and time period ( quarterly, monthly etc. )
  - change the "group by" logic ( group by indicators vs. locations)
  - Dev Note: all of the above attributes are to be saved in the `chart_json` data type

Throughout this part of the process, changes that the user makes to the definition of the chart are to be dynamic and reflect themselves immediately in the chart preview section of the page.

The date will default to the most recent data when creating a chart.

Note: for the most part we will be using the existing chart builder functionality to accomplish the chart building / saving neccessary for Beta.

The following charts will have the following behaviors:

Chloropleth map
~~~~~~~~~~~~~~
    - Ability to switch between shape, satalite, and roadway views/
    - Ability to add bubbles on top of the map in which the radius of the circle represent the size of the indicator, and the point on the map represents the lon/lat of the location.
        -> http://bost.ocks.org/mike/bubble-map/

Pie Chart
~~~~~~~~~
    - When Selecting a pie chart the user selects an indicator that is the parent in a `part_to_be_summed` relationship.
    - The Pie chart will by definition be the representation of the indicators below it in the relations.
        -> for instance, if i pick "missed children" as my parent indicator, the pie chart will automatically be created with the sub reasons ( refusal, no-team, child not avail )
    - The user will ( for now ) not have the ability to remove indicators and just pot those that they want int he pie chart.  This is because doing so may by nature of it's functionality lead to mis-interperatation of data.

Scatter Plot
~~~~~~~~~~~~
    - When creating a scatter plot chart, the user must chose exactly two indicators.
    - both the x and the y values will be populated with the indicator chosen when initializing the chart
    - The user can pick the x or the y value as the additional indicator to be plotted, but the two indicators must be different in order for the data to be previewed.
    - The indicators available in the the drop down will have a `?chart_type=scatter` parameter added to the request in order to properly filter indicators for the drop down.

Note: Here it is important that we have a hover over both indicator drop downs that display the instructions for the scatter plot.  We need this for all charts, but for scatterplot fistly as this is the most complicated chart type.

Bar Chart
~~~~~~~~~
    - Ability to group by either indicator or location
    - Choose up to 5 indicators
    - Chose quarterly or monthly break down.

For missing data: a bar is skipped if x axis is time and we dont have data for a particular month.

Line Chart
~~~~~~~~~~
    - No more than two Indicators can be used in a line chart vizualzation
    - The user can choose the time line such that two line charts coudld appear in the same chart for the same indicator but for different years ( See top left polio case counter in management dashboard )

For missing data: if a month does not have data, the line should "smooth" or extrapolate the difference.  So instead of going from 4->0->5 in the case where zer represents a month of missing data.. simply skip over the month without data and draw a line from 4->5.

Heat Map Matrix
~~~~~~~~~~~~~~~
    - Note: Optional for Beta.
    - This is a way to create a heat map matrix ( see district dashboard ) for a custom set of indicators
    - See district dashboard: http://rhizome.work/datapoints/district-dashboard/Afghanistan/2014/11/

Chart Style Wizard
~~~~~~~~~~~~

User clicks "you may also change additional chart settings " in order to acess the below

    - After creating the chart the user goes thorugh a "style" wizard in which they are prompted to do the following:
       -> give chart a name
       -> pick from one of 3 palletes for the chart
       -> label x-axis / y-axis
       -> select legend title and position

Mounting Chart to Layout
~~~~~~~~~~~~~~~~~~~~~~~~

After saving the dashboard, the user will be able to Mount the chart on a dashboard.

The simplest thing the user can do is mount a single visualization in which the created chart consumes the entire container.

Tis chart will have a unique URL as well as a export function to .jpeg, .pdf, and direct_link,

If however, the user wants to mount this chart on a dashboard with other charts, they can pick from a variety of layouts, mounting the created chart at the default, first position of each layout.

Layout Details
~~~~~~~~~~~~~~

Each layout must be mobile, tablet and desktop responsive.  The current app renders nicely on a macbook, but tweaks when dealing with a desktop monitor.  It's critical that these layouts are clean and can show on any and all screens.

.. image:: http://s15.postimg.org/safbke97v/mount_chart_to_dash.jpg
   :width: 600pt

- Layout #1: Chart is Dashboard
    - Simply mount the created chart on an empty dashboard and assign a unique URL for that dashboard.
- Layout #2: Basic (selected by default)
    - Very Similar to the management dashboard.  8 Charts , fluid layout
- Layout #3: Map
    - This layout focuses on the Map on the left hand corner and provides three sections for custom chart on the right hand side.
- Layout #4: 3 charts, no Map.  See the design for the homepage re-design for an idea how this layout works.

After selecting the layout, the user simply clicks the " add new chart " option and goes to the beginning of the flow in which they are prompted to select an indicator in order to create a chart, finally mounting it on the parent dashboard.

Editing A Dashboard
~~~~~~~~~~~~~~~~~~~
When it comes to editing the "dashboard" there is actually very little functionality needed, as the vast amount of logic and functionality is handled in the chart builder.  The following basic functions are needed.

    - *Render Dashboard*:  with the ability to *click* into each chart component
    - *Select Chart*: User clicks on a chart section and this allows them to enter into the "chart edit" mode
    - *Drag and Drop Chart Position*: The user should be able to drag and drop a chart from one position of the template into any other on the page.  When this happens, the other charts fill in the missing space based on what chart has been moved.  I.e. if chart 4 is moved to position 1, the original chart 1 will be chart 2 and so on.
    - *Update Title*: Ajax POST to save the title of a dashboard
    - *Naviation* : This inherits from the navigation used througout the application and will dynmically shift the data in the charts according to the *campaign* selected.  Being as that the char itself has it's own location_control then we do not need this control for the parent (dashboard) page.
    - *Add New Chart*: When viewing the dashboard in edit mode, the "add new chart" button will appear at the bottom right hand of the screen in same place that we have it currently (within the footer)


Dashboard Export
~~~~~~~~~~~~~~~~
When in "view" mode of a dashboard, at the bottom right there is an "export" button.

Clicking that button has the same functionality as the chart export and will allow for:
    - .pdf, .jpg, .png
    - direct link , embed code

NOTE: This is separate from the chart export funciton, that is users should be able to export a chart itself, or the entire dashboard.

Other Requirements
~~~~~~~~~~~~~~~~~~
  - Both the Builder and the Render of the custom Dashbboard must be compatiable with all modern web browsers including:
    - i.e. 10+
    - firefox
    - chrome

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
  - Duplicate datapoints (i.e. datapoints with an identical location, campaign and indicators) are prohibited.
    - If a document is uploaded which contains a duplicate datapoint from a previous document, the datapoint from the new document will override the datapoint from the old document.
    - If a single document contains duplicate values for a datapoint, the datapoint that appears later in the document overrides the previous datapoint. For example, if a row on line 4 contains identical location, campaign and indicator values as a row on line 7, line 7 will override line 4.


Aggregation and Calculation
===========================
- When a value in datapoints exists for location X, populate agg_datapoint with this value and NOT the aggregated values of X's children
- When a value in datapoint exists for a calculated indicator, choose this value as opposed the calculated value.
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
    - returns shapes for the parent_region requested as well as all of it's children


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
