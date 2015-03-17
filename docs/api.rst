API
===

Response Format
---------------

The default format for responses is JSON. Each response is a JSON object
containing three parameters: ``meta``, ``objects``, and ``errors``:

.. code-block:: json

   {
       meta: {},
       objects: [],
       errors: {}
   }

``meta``
  An object containing metadata about the request such as the original request
  parameters and pagination information

``objects``
  An array containing the requested data. The contents of the array vary with
  the different requests

``errors``
  An object mapping an error type to an error message

Global Parameters
-----------------

``username``
  *required*

  The username for authentication of the request

``api_key``
  *required*

  The API key for authentication

``limit``
  default: 20

  The maximum number of objects to be returned

``offset``
  default: 0

  The offset into the list of matched objects. For example, if ``offset=10`` is
  passed to an endpoint, the first 10 records that match the query will not be
  returned, the response will begin with the 11th object

``format``
  default: ``json``

  One of either ``json`` or ``csv`` that determines the format of the response

Endpoints
---------

``/api/v1/datapoint/``
++++++++++++++++++++++

Return datapoints grouped by unique pairs of region and campaign. If no data is
stored for a requested region, the value is computed by aggregating sub-regions.

Parameters
~~~~~~~~~~

``indicator__in``
  A comma-separated list of indicator IDs to fetch. By default, all indicators
  are collected in a single object for each unique pair of region and campaign

``region__in``
  A comma-separated list of region IDs

``campaign_start``
  format: ``YYYY-MM-DD``

  Include only datapoints from campaigns that began on or after the supplied
  date

``campaign_end``
  format: ``YYYY-MM-DD``

  Include only datapoints from campaigns that ended on or before the supplied
  date

``campaign__in``
  A comma-separated list of campaign IDs. Only datapoints attached to one of the
  listed campaigns will be returned

``no_pivot``
  default: ``false``

  Return only one datapoint per object. Instead of collecting all requested
  indicators into a single object, return one object per region, campaign,
  indicator set.

``uri_format``
  default: ``id``

  Configure how references to other objects are provided. Valid values are:

  - ``id``
  - ``slug``
  - ``name``
  - ``uri``

Response Format
~~~~~~~~~~~~~~~

.. code-block:: json

  {
    meta: {
      limit: ...,
      offest: ...,
      total_count: ...,
      parameters_requested: {...}
    },

    objects: [{
      region: ...,
      campaign: ...,
      indicators: [{
        indicator: ...,
        value: ...
      }, {
        indicator: ...,
        value: ...
      }]
    }],

    errors: { ..}
  }

``region``
  The region for this set of data. Region will be the ID, slug, name, or URI for
  the region depending on the value of the ``uri_format`` parameter

``campaign``
  The campaign for this set of data. Campaign will be the ID, slug, name, or URI
  for the campaign depending on the value of the ``uri_format`` parameter

``indicators``
  An array of the values for the requested indicators. This will always be an
  array, even if the ``no_pivot`` parameter is passed

  ``indicator``
    The ID, slug, name, or URI (depending on the value of ``uri_format``) of the
    indicator represented by the object

  ``value``
    The value of the indicator

``/api/v1/campaign/``
+++++++++++++++++++++

Return a list of campaign definitions.

Response Format
~~~~~~~~~~~~~~~

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>,
      slug: <String>,
      start_date: "YYYY-MM-DD",
      end_date: "YYYY-MM-DD",
      office: <reference>,
      resource_uri: <String>,
      created_at: "YYYY-MM-DDTHH:MM:SS.sss"
    }],

    errors: {...}
  }

``office``
  A reference to the office under which the campaign was conducted. This will be
  an ID (``Number``), name (``String``), slug (``String``), or URI (``String``)
  for the office depending on the value of the ``uri_format`` parameter

``/api/v1/indicator/``
++++++++++++++++++++++

Return a list of indicator definitions.

Response Format
~~~~~~~~~~~~~~~

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>
      short_name: <String>,
      slug: <String>,
      description: <String>,
      is_reported: <Boolean>,
      resource_uri: <String>,
      created_at: "YYYY-MM-DDTHH:MM:SS.sss"
    }],

    errors: {...}
  }

``/api/v1/region/``
+++++++++++++++++++

Return a list of region definitions.

Response Format
~~~~~~~~~~~~~~~

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>,
      slug: <String>
      is_high_risk: <Boolean>,
      latitude: <Number>,
      longitude: <Number>,
      region_code: <String>,
      region_type: <String>,
      shape_file_path: <String>,
      office: <reference>,
      parent_region: <reference>,
      resource_uri: <String>,
      created_at: "YYYY-MM-DDTHH:MM:SS.sss",
    }],

    errors: {...}
  }

Properties with type ``<reference>`` can contain an ID (``Number``), name, slug,
or URI (all of type ``String``) depending on the value of the ``uri_format``
parameter.

``/api/v1/office/``
+++++++++++++++++++

Return a list of office definitions. Offices are administrative concepts that
represent different parts of the organization that oversee regions. For example,
there might be an office for Nigeria that represents the Nigerian Country
Office. The region Nigeria that represents the country, as well as all of its
sub-regions, would be associated with the Nigeria office.

Response Format
~~~~~~~~~~~~~~~

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>,
      resource_uri: <String>,
      created_at: "YYYY-MM-DDTHH:MM:SS.sss",
    }],

    errors: {...}
  }

Computed vs Stored Indicators
-----------------------------

Computed indicators are not stored in the database, they are calculated from
other indicators in the database. For example, the "Percentage of Missed
Children" indicator is computed by dividing the "Number of Missed Children"
indicator by the "Number of Targetd Children" indicator.

Computed indicators are fetched using the same ``/api/v1/datapoint/`` endpoint
as stored indicators.

The response from the ``/api/v1/indicator/`` endpoint for a computed indicator
will include an additional property not included in a stored indicator:
``computed_from``.

.. code-block:: json

  {
    meta: {...},
    objects:[{
      ...
      computed_from: [...]
    }],
    errors: {...}
  }

The ``computed_from`` property is an array of references to the indicators used
to compute this one. The format of the references depends on the ``uri_format``
parameter.

Aggregation by Region
---------------------

If you request a region for which there is no data, the system will traverse the
hierarchy of regions down and aggregate the data it finds at those levels by
adding them together. For example, if you request the "Number of Missed
Children" for Nigeria, but that indicator is not stored in the database for
Nigeria, the system will iterate over the states that comprise Nigeria and add
the values it finds for that indicator together. For each state that does not
have a value, it will check its constituent regions, and so on until it finds a
region with a value for that indicator or it runs out of sub-regions to check.

.. image:: img/geo_agg.png

If the value of an indicator was generated by aggregating data from sub-regions,
the indicator object will have an ``is_agg`` property:

.. code-block:: json

  ...
  region: 23,
  indicators: [{
    indicator: 1,
    value: ...
  }, {
    indicator: 2,
    value: ...,
    is_agg: true
  }]
  ...

In the above example, a value for indicator 1 was found for region 23. No value
for indicator 2 was found for region 23, so the system calculated that value by
aggregating the values of it sub-regions.

Conflicts with Sub-regions
++++++++++++++++++++++++++

If a value is stored for a given region, that is the value returned regardless
of whether or not the region's sub-regions also have values. Because there is
nothing preventing a value being stored for a region and its sub-regions, it is
possible that the stored values at differing levels may conflict.

.. image:: img/geo_agg_conflict.png

In the above example one of the regions has a stored value of 7, and its three
sub-regions have values of 1, 1, and 3. This could be indicative of an error in
the data and should be flagged. Regardless of whether this is an error or
intentional, the value returned for that region (and the value used in
aggregation for any of its parent regions) is the value stored for the region;
the values in the sub-regions are ignored except when they are explicitly
requested.

Partial Missing Values
++++++++++++++++++++++

When aggregating data geographically, it is possible to calculate the value for
a region even if not all of its sub-regions have data.

.. image:: img/geo_agg_partial.png

These situations should be flagged so that users are aware of them when they
occur. It's important to know that the value for the country you are seeing is
actually only representative of some portion of its sub-regions and not the
entire country.

Controlling Aggregation Behavior
++++++++++++++++++++++++++++++++

You can control the behavior of the aggregation using the ```` parameter.

``mixed``
  default

  If the requested region has stored data, use that, otherwise travers the sub-
  regions to aggregate the indicators found there

``agg-only``
  Only return data aggregated from sub-regions. If the region you requested
  actually has data stored on it, it will be ignored

``no-agg``
  Do not travers the sub-regions to aggregate data if the requested region does
  not have a value stored

Filtering
---------

For the Datapoint Resource, the following filtering methods are available

These numeric filters are  available on the ID, value, and created_at columns.

Greater Than
++++++++++++

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__gt=9

Less Than
+++++++++

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__lt=9

Greater Than or Equal to
++++++++++++++++++++++++

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__gte=9

Less Than or Equal to
+++++++++++++++++++++

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__lte=9

Range
+++++

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/indicator/format=json&id__id__range=9,12


Multiple Objects
++++++++++++++++

Lets say that i want to see data 5 regions (14589,15863,17562,17940)
Simply use the "in" operator on any of the columns avaliable for this resource (indicator,campaign, etc)

.. code-block:: python
   :linenos:

    localhost:8000/api/v1/datapoint/?region__in=14589,15863,17562,17940


Filter By Date of Campaign
++++++++++++++++++++++++++

The API will let you filter a campaign, or a specific campaign to query on, but
you also have the option to pass in the start and end date.

If you pass only start date, you will receive datapoints after (and including)
the date passed in.

If you pass only end date, you will receive datapoints befre (and including) the
date passed in.

If you pass in both start and end, you will get the data relevant to the
campaigns in between the two dates.

Please Pass the date format as 'YYYY-MM-DD'

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/datapoint/?campaign_start=2014-06-01&campaign_end=2014-09-01




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
