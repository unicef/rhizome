Backend Source Code
===================

***
ETL
***

There are two ways that information gets into the system.

1. Data Entry Form (DataEntryResource API)
2. ETL Process

The flow of data in the ETL Process is as follows:

- Each file, or incoming data stream has a corresponding *document_id*
- Each fact in a document is then translated to a *source_datapoint* which
  contains principally a *campaign_string*, *region_string*,
  *indicator_string* and *value*.
- The RefreshMaster class is instantiated for a document_id which in turn:
- Creates an necessary meta_data rows (ex. source_indicator) from the
  raw data.
- **INSERT** a datapoint for each source_datapoint that has a corresponding
  mapping for the region, campaign, and indicator.
- **UPDATE** datapoints only in the case when that original datapoint was
  the result of another source_datapoint. That is, this method will NOT
  override data that was inserted via the data_entry form (a datapoint that
  has been inserted from the data_entry form will have the
  source_datapoint_id =-1).
- **DELETE** datapoints for which a mapping has expired.  If the mappings
   that were the result of that document_id
      - so if you load a csv with 10 source_datapoints, map everything,
        then refresh master you should see 10 datapoints.
      - if then you delete the mapping for a region in this document that
        has attached to it 2 datapoints, and refreshed master, you would
        then see that the document_id has 8 datapoints instead of 10.

Mapping
-------

TO DO -> Convert the three mapping tables to one.

- The general principal is that, the system creates a source_metadata record
  only when the system has never seen that string before.
- If the source_meta_data_id has been mapped by a user on a previous document
  then the data should flow for that particular meta data item without the user
  having to map that meta data.


**********
Data Entry
**********


*******
Caching
*******


***
API
***

Datapoint Resource
------------------

This is the main method used by the API to retrieve data about datapoints.


  .. autoclass:: datapoints.api.datapoint.DataPointResource
      :members:


CSV Serializer
--------------

This takes the response given to the api ( list of objects where the region / campaigns are the keys), and translates that data into a csv where the indicators are columns, and the value for each campaign / region couple is the cooresponding cell value.  This method also looks up the region/campaign/indicator id and passes these strings ( not ids ) back to the API.

  .. autoclass:: datapoints.api.serialize.CustomSerializer
     :members:


Campaign Resource
-----------------

  .. autoclass:: datapoints.api.meta_data.RegionResource
     :members:


Indicator Resource
------------------

  .. autoclass:: datapoints.api.meta_data.RegionResource
     :members:


Region Resource
---------------

  .. autoclass:: datapoints.api.meta_data.RegionResource
     :members:


***************
Reference Sheet
***************

socument_id -
source_datapoint -
datapoint -
region -
indicator -
campaign -
map -
agg_datapoint -
datapoint_with_computed -
calculated_indicator_component -
etl_job -
