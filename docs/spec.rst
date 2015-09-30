*****************
Rhizome Tech Spec
*****************

Overview
=======

RhizomeDB is a UNICEF initiative to lead a culture change within the U.N. as to how data is collected, cleaned and used to make data driven decisions in the field and within management.

RhizomeDB is to have the following base functionality:
   - **Admin**: Page to edit, view and create the necessary metadata in order to ingest data.  This icludes but is not limited to, locations, campaigns, indicators, users, roles and permissions.
   - **Source Data Management**: Page to upload and manage data sources from csv uploads, 3rd party apis, our ODK engine.  This part of the application will allow a user to configure 3rd party data source, upload new data, validate data from the people they manage, map necessary metadata and view the results of the upload
   - **Data Entry**: The Data Entry module gives the user direct access to the data that the system reports on.  The source data module above sends data through an ETL process with a number of steps of validation.  The data entry application essntially allows the user to shortcut these steps in order to alter data on demand.
   - **Static Dashboards**:  The application must provide 3 static dashboards, Management, NGA Campaign, and District.  These dashboards are complete and are to be the standard for the style and structure of the Custom Dashboard Module.
   - **Custom Dashboards**: The custom dashboard module allows permitted users to configure a dashboard to view data how they want, and for a particular set of indicators and locations.   Think of this as stripped down web version of Tableau.
   - **Home Page**:  The Homepage can be looked at as a static dashboard that updates dynamically based on the user's permissions and configurations.

Application Overview
~~~~~~~~~~~~~~~~~~~~

Stack
~~~~~

Deployment
~~~~~~~~~~

The application is served


Source Data Management
======================


Admin
=====

ODK Info Page
~~~~~~~~~~~~
