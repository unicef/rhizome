API
===

*the following responds to the v2 api
 -- /api/v2/content_type/?<query_params>* --

Response Format
---------------

The default format for responses is JSON. Each response is a JSON object
containing three parameters: ``meta``, ``objects``, and ``errors``:

The following response format applies for GET and POST requests.

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


POST
====

Note: Insert, Update and Delete are all implemented currently as POST requests, but it is a to do to replace this functionality with DELETE / PUT when time allows.

insert
------

pass a dictionary according to the "column":"value" for each field that you would like to insert

update
------

pass a json dictionary with the id and cooresponding values that need to be updated.

delete
------

id = ''

permissions
-----------

endpoints
---------
``POST api/v2/region``
'region': {'orm_obj':Region,

``POST api/v2/indicator``
'indicator': {'orm_obj':IndicatorAbstracted,

``POST api/v2/campaign``
'campaign': {'orm_obj':Campaign,

``POST api/v2/region_map``
  'region_map': {'orm_obj':RegionMap,

sample post

.. code-block:: json

  {
  'source_object_id': 184381,
  'master_object_id':12908
  }

response
.. code-block:: json
  {"objects": {"new_id": 73658}, "meta": null, "error": null}


'document_review' : {'orm_obj':DocumentDetail,
'group': {'orm_obj':Group,
'user': {'orm_obj':UserAbstracted,
'region_permission': {'orm_obj':RegionPermission,
'user_group': {'orm_obj':UserGroup,
'document': {'orm_obj':Document,
'office': {'orm_obj':Office,

'indicator_map': {'orm_obj':IndicatorMap,


'campaign_map': {'orm_obj':CampaignMap,


GET
===

Global Parameters and Query Filters
-----------------------------------

``limit``
  default: 20

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
``api/v2/region``
  default: 20

  The maximum number of objects to be returned

``api/v2/indicator``
  default: 0

``api/v2/campaign``
  default: 0


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



Custom Serialization
--------------------

This takes the response given to the api ( list of objects where the region / campaigns are the keys), and translates that data into a csv where the indicators are columns, and the value for each campaign / region couple is the cooresponding cell value.  This method also looks up the region/campaign/indicator id and passes these strings ( not ids ) back to the API.

  .. autoclass:: datapoints.api.serialize.CustomSerializer
     :members:


PERMISSIONS
------------


API REQUIREMENTS
------------

Golbal
  - Limit
  - Offset
  - always_return_data = True

https://seedscientific.atlassian.net/wiki/display/CE/User+Permissions+System
