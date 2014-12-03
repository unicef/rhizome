API
===



**GET REQUESTS**

For the sake of brevity, the username and api key parameters are not
contained in the example strings below.  When testing these in your
application or in curl, dont forget to append your api key.



Parameters Avalible in the API
   - indicator,region,campaign

        - <basic filter> http://localhost:8000/api/v1/datapoint/?username=evan&api_key=67bd6ab9a494e744a213de2641def88163652dad&region=116&indicator=26&campaign=3
        - <__in filter> http://localhost:8000/api/v1/datapoint/?username=evan&api_key=67bd6ab9a494e744a213de2641def88163652dad&region=12&indicator__in=51,35&campaign=2

   - limit: the default limit for the application is 20.  This means that the API pulls the first 20 records from the database, and if those 20 contain only 3 indicators, you will only receive data forthose 3 indicators.
   - format: the default is JSON, but CSV is also avalible.  CSV gives one record per campaign/region combination, and uses indicators as column headers
   - uri_display 'slug' , 'id' , 'name'
   - campaign_start : pass in date (format yyyy-mm-dd)
   - campaign end : pass in date (format yyyy-mm-dd)

  TO DO
  - pivot_type: defaults to <indicator_key>, also available, <datapoint_key>, <region_key>, <campaign_key>



**Filtering**

For the Datapoint Resource, the following filtering methods are available

These numeric filters are  available on the ID, value, and created_at columns.

Greater Than

blablablabla


.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__gt=9

Less Than

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__lt=9

Greater Than or Equal to

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__gte=9

Less Than or Equal to

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__lte=9

Range

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/indicator/format=json&id__id__range=9,12


Multiple Objects

Lets say that i want to see data 5 regions (14589,15863,17562,17940)
Simply use the "in" operator on any of the columns avaliable for this resource (indicator,campaign, etc)

.. code-block:: python
   :linenos:

    localhost:8000/api/v1/datapoint/?region__in=14589,15863,17562,17940


Filter By Date of Campaign

The API will let you filter a campaign, or a specific campaing to query on, but you also have the otion to pass in the start and end date.

If you pass only start date, you will receive datapoints after ( and including ) the date passed in.
If you pass only end date, you will receive datapoints befre ( and including ) the date passed in.
If you pass in both start and end, you will get the data relevant to the campaigns in between the two dates.

Please Pass the date format as 'YYYY-MM-DD'

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/datapoint/?campaign_start=2014-06-01&campaign_end=2014-09-01


Aggregating By Region

When aggregating my parent region use the 'parent_region_agg' resource

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/parent_region_agg/?format=json&indicator__in=25&parent_region=23


Using This Resource
  - campaign__in, indicator__in and parent_region are the filter parameters for this resource

About the result set
  - currently i have NOT enabled the same pivoting as in the simple resource
  - currently this resource does not have the uri_display option that allows the client to request data based on slug, id or name
  - this is totally doable but i will only do this once i am asked.
  
.. code-block:: python
   :linenos:

    "objects": [
      {
          "campaign": "/api/v1/campaign/2/",
          "id": 69,
          "indicator": "/api/v1/indicator/25/",
          "parent_region": "/api/v1/region/23/",
          "resource_uri": "/api/v1/parent_region_agg/69/",
          "the_sum": 144665
      },
      ...
