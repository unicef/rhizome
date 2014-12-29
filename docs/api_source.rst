API Source Documentation
========================


Datapoint Resource
---------------

This is the main method used by the API to retrieve data about datapoints.


  .. autoclass:: datapoints.api.datapoint.DataPointResource
      :members:


CSV Serializer
---------------

This takes the response given to the api ( list of objects where the region / campaigns are the keys), and translates that data into a csv where the indicators are columns, and the value for each campaign / region couple is the cooresponding cell value.  This method also looks up the region/campaign/indicator id and passes these strings ( not ids ) back to the API.

  .. autoclass:: datapoints.api.serialize.CustomSerializer
     :members:


Campaign Resource
---------------

  .. autoclass:: datapoints.api.meta_data.RegionResource
     :members:


Indicator Resource
---------------

  .. autoclass:: datapoints.api.meta_data.RegionResource
     :members:


Region Resource
---------------

  .. autoclass:: datapoints.api.meta_data.RegionResource
     :members:
