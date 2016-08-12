Core Functionality
==================

Uploader
--------

The Source Data module allows a user to upload .csv or .xls files to the system and map any meta data necessary to ingest the data in the system.

After uploading a file, the use can see mapped and un-mapped metadata, as well as the results of the upload.  Each upload can be downloaded by clikcing the "download raw" link.

Each upload has a cooresponding URL that can be shared so that it makes it easy for colleauges to share information without emailing files back and fordth.

Manage System
-------------

The manage system link represents a basiec CRUD ( Create Read Update Delete ) application around the application's core metadata.  A permissioned users can create indicators, campaigns, users, indicator tags as well as create calculations for campaign indicators.

At this time we do not have the ability to delete metadata itemsin the manage system, but please see the section on the React App enhancements for more on this.  Also, while we can create Campaigns, Indicators, Users, Groups and Tags but we ** Can Not Create Locations **.

Chart Builder
-------------

The Chart builder allows a user to explore data at various aggregation levels and save this data to one of a number of Chart Types.  With this fucntionality a user can create maps, tables, and trend charts according to the necessary analysis.

Dashboard Builder
-----------------

The dashbaord builder allows for a user to create a dashboard which is in essence a collection of charts.  A dashbaord is comprised of Rows, and rows are comprised of charts.  When adding a chart to a row, the user can either create a new chart in line in the dashbaord builder itself, or search for and add an existing chart to the dashboard.
