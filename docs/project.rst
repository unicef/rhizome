*******
Project
*******

Functionality
=============

    - GET and POST api methods that allow for retrieval, and insert of
      datapoints
    - Basic CRUD (create, read , update, delete) front end interface
    - Basic Search functionality which allows users to find datapoints with
      a region, indicator, campaign and / or created by attributes
    - Permissioning for Create, Update, Delete
    - Audit Functionality using django-simple-history
      (https://github.com/treyhunner/django-simple-history)

Dependencies
============

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
===========
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


********************
How The System Works
********************

The polio backend is based around the **datapoint** table which has a key for region, indicator and campaign.  The datapoint table gathers and consolidates information from Data Entry, CSV upload, ETL of 3rd party APIs and Data Sources and makes this information available to a REST api.  This api powers the dashboards, as well as the data explorer.

The system differentiates between conflicts and information from different sources via the **source_datapoint** table which holds information uploaded directly from spreadsheets.

In addition the system maintains **source_indicators** , **source_regions**, and **source_campaigns** all of which have cooresponding mapping tables.  Each of the source tables have a cooresponding **document_id** which gives a link to the source of the raw data.

When a source_datapoint has mappings for region, campaign, and indicator, by using the **refresh_master** method for that document_id will create, or update ( if a conflicting datapoint exists ) the datapoint table.


Regions
=============

Regions have a parent, lon / lat, region type

**uniqueness for region is defined by region_name, region_type, country**

Prior we had an issue in which two regions with the same name ( HRA Level ) and in our ingestion we collapsed both regions into one, causing regional aggregation to break and display conflicting data.

We also had an issue in which a region in the same country has the same name but with a different region type ( sokoto settlement vs. sokoto state).


We will also be storing a region_geo_json table that will hold region_id, geo_json ( as a blob )



Region Upload
=============

The region upload is largely meant for internal use and will not be available when the application is out in the field.

  - Upload a file with parent reginos, country, region type
  - Insert the Parent Regions into Source Regions.
  - Insert Children into Source Regions
       - Update the parent region string, and code from the parents inserted initially
  - Refreshing Master for that document_id will *source_regions*
       - If a region with the same name, type, country exists:
          -> Create Mapping for that new source_region_id
          -> Update Master with the Longitude, Latitude, Parent_id ( join to region table, if id is differnet update, if no match, keep parent_region_id
      - Else - user ( Bo ) will need to map these by accessing the document_id in accordance with the upload.



Meta Data Mapping
=================

Regarding POLIO-205 - How are we to determine the semantic identities of Regions in a complex regional heirarchy.

Consider the following wikipedia page:

  http://en.wikipedia.org/wiki/Killa_Abdullah_District

  "Killa Abdullah or Qilla Abdullah or Abdullah Qilla (Pashto: قلعہ عبد الله‎)"...

In our system we map data from each source, to semantic identites in our system.  For instance, "# vaccinated" is the same as "num vaccinated," and "NG JUN 2014" is the same as "Nigeria June 2014."

When ingesting a spreadsheet, here are the rules as to how datapoints are mapped and validated.
  - each souce_datapoint must have a record explicilty mapping the indicator_string, campaign_string and region_code to their respective IDs.
  - Regions are not Auto mapped on their Name, but rather their region code.

*Region Codes*

NIGERIA
  - WHO has a naming convention for Settlements in Nigeria
  - <province><district><sub-district><settlement>
  - Bo created existing sub-districts with this convention so i was able to map a large part of the ODK data using this convention.

AFGHANISTAN
  - * i am not sure we need to ask bo *

PAKISTAN
  - * i am not sure we need to ask bo *


Needs Documentation
  - Shape File ingestion
  - source datapoint -> datapoint process in depth
  - transforming data into source_datapoints
      ->CSV pivoted
      ->CSV Non Pivoted
      ->ODK
  - document_ids and their significance


Future Topics Regarding Regions
  - is_high_risk changes over time
  - when boundries change over time
  - outbreak countries and new office_ids
