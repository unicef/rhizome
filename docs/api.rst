API
===

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

Insert
------

pass a dictionary according to the "column":"value" for each field that you would like to insert

Update
------

pass a json dictionary with the id and cooresponding values that need to be updated.

Delete
------

pass a json dictionary in accordance to the ids you want to delete as well as:

id = ''


Region POST
-----------

``api/v2/region``

- ``django model: Region``


POST DATA

.. code-block:: json

  {
     "name": "fake_place",
     "office_id": "2",
     "parent_region_id": "12908",
     "region_code": "fake_code",
     "region_type_id": "1",
     "source_id": "1"
  }

POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 87472},
    "meta": null,
    "error": null
  }


Indicator POST
-----------

``api/v2/indicator``

- ``django model: Indicator``


POST DATA

.. code-block:: json

  {
   "description": "fake description",
   "is_reported": "0",
   "name": "fake indicator name",
   "short_name": "fake short name",
   "slug": "fake_indicator",
   "source_id": "1"
  }


POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 477},
    "meta": null,
    "error": null
  }

Campaign POST
-------------

``api/v2/campaign``

- ``django model: Campaign``

POST DATA

.. code-block:: json

  {
   "campaign_type_id": "1",
   "end_date": "2017-01-01",
   "office_id": "1",
   "slug": "fake_campaign",
   "start_date": "2017-01-01"
  }


POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 217},
    "meta": null,
    "error": null
  }

Office POST
-----------

``api/v2/office``

- ``django model: Office``

POST DATA

.. code-block:: json

  {
    "name": "somalia"
  }


POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 4},
    "meta": null,
    "error": null
  }


MapTable POST
-------------

``POST api/v2/<region;indicator;campaign>_map;``
  - ``django model: CampaignMap; IndicatorMap, RegionMmap``


sample post

.. code-block:: json

  {
  "source_object_id": 184381,
  "master_object_id":12908
  }

response

.. code-block:: json

  {
    "objects": {"new_id": 73658},
    "meta": null,
    "error": null
  }


User POST
---------

``api/v2/user``

- NOT Implemented!!!!
- Please use django admin form found at /datapoints/users/create and datapoitns/users/edit/<id>


Group POST
----------

``api/v2/group/``

- ``django model: Group``


POST DATA

.. code-block:: json

  {
    "name": "fake_group"
  }


POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 7},
    "meta": null,
    "error": null
  }


User to Group POST
------------------

``api/v2/user_group``

- ``django model: UserGroup``
- Used in /datapoints/users/edit/<user_id> page

POST DATA

.. code-block:: json

  {
    "user_id": 1,
    "group_id":7

  }


POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 41},
    "meta": null,
    "error": null
  }


Region Permission POST
-------------

``api/v2/region_permission``

- ``django model: RegionPermission``

POST DATA

.. code-block:: json

  {
    "user_id": 1,
    "region_id":12910

  }

POST RESPONSE

.. code-block:: json

  {
    "objects": {"new_id": 344},
    "meta": null,
    "error": null
  }



DataPoint POST
--------------

used by the /datapoints/entry page

``api/v1/dataentry``


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

  *note - For the /v2 api, the limit / offset is applied after the queryset is
  returned.  Since most of the object lists are small this isnt a huge issue
  , however it is to be of note when querying the region endpoint which returns
  20k+ results*

``format``
  default: ``json``

  One of either ``json`` or ``csv`` that determines the format of the response

``simple_evaluation``

.. code-block:: json

  /api/v2/indicator/?id=21
  /api/v2/indicator/?slug=number-of-all-missed-children


``__in``

pass a list of values and retrieve one result for each match

.. code-block:: json

    /api/v2/indicator/?id__in=21,164


``__gt; __lt; __gte; __lte``

.. code-block:: json

    /api/v2/campaign/?start_date__lte=2015-01-01
    /api/v2/campaign/?start_date__gte=2015-01-01
    /api/v2/office/?id__gt=2
    /api/v2/office/?id__lt=2

``__contains; __starts_with``

filter resources with simple string functions.

.. code-block:: json

  /api/v2/indicator/?name__startswith=Number
  /api/v2/indicator/?name__contains=polio


* Note - These query parameters are taken directly from the Django ORM.  For
  more on how these work see here:*
    https://docs.djangoproject.com/en/1.8/topics/db/queries/#field-lookups

v1 / v2
+++++++

The v1 API is only to be used by the datapoint, datapointentry, and geo
endpoints.  The functionality of these endpoints is very much customized to
the needs of our application, while the v2 endpoints are much more abstract and
easy to extend as new models needed to be added to the system and the API.

The metadata endpoints (/v1/campaign, v2/indicator etc) for v1 are retired and
v2 shoudl be used to access all data with the exception of the three endpoints
mentioned above.

The main difference between the v2 and the v1 API is that the v2 api applies
permissions to the result set.  The api itself is closely related to the django
ORM and because of which, all of the filters that are available to django are
available in the url.

Each resource has attached to it a model ( Region, Indicator, Campaign ) etc,
and an optional permission function.  The permission function takes the Model
type and the list of IDs that were the result of the initial filter.

The flow of the /v2 api is as follows:

  1. Parse the query parameters and query the database using this dictionary as the filter kwargs for that model.
      - i.e. if the url is /region/?id=12907, the Api translates that into:
        results = Region.objects.filter(**{'id':12907})
  2. Using the primary keys of the above result, apply the permission_function
     for that resource.
      - If there is no permission function applied, then return all the data from step 1.
      - In some instances the "permission_function" is not just used to filter the result set based on the user permission, it is used to modify the queryset in some way.
      - If the permissions function is called for, the list of IDs is passed as well to make sure that the result is the intersection of the query parameters, and the data that user is authorized to see.
  3. Serialize the data.
      - Depending on the data type, the model and the requests from the FE, the
        system cleans and returns data to the api for consuption.


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

  Return only one datapoint per object. Instead of collecting all requested
  indicators into a single object, return one object per region, campaign,
  indicator set.


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
  The region for this set of data. Region will be the ID of the resource.

``campaign``
  The campaign for this set of data. Campaign will be the ID of the resource.

``indicators``
  An array of the values for the requested indicators. This will always be an
  array, even if the ``no_pivot`` parameter is passed

``indicator``
  The ID of the indicator represented by the object

``value``
  The value of the indicator

``Filter By Date of Campaign``

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


``/api/v2/campaign/``
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


permissions
-----------

permissions are handled on a per object basis, specifically via a strict mapping in the V2 api that associates a permission function to each content type.

for instance:

.. code-block:: python

  {
  "region": {"orm_obj":Region,
    "permission_function":self.apply_region_permissions},
  }

permissions are largely based around the *fn_get_authorized_regions_by_user* stored procedure which uses a recursive CTE and the *region_permission* table to find the regions a particular user is allowed to read or write to.


Custom Serialization
--------------------

This takes the response given to the api ( list of objects where the region / campaigns are the keys), and translates that data into a csv where the indicators are columns, and the value for each campaign / region couple is the cooresponding cell value.  This method also looks up the region/campaign/indicator id and passes these strings ( not ids ) back to the API.

  .. autoclass:: datapoints.api.serialize.CustomSerializer
     :members:
