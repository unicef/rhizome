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


Want to Pull Data from Rhizome?
+++++++++++++++++++++++++++++++

Contact dingeej@gmail.com to get an API key


Global Parameters and Query Filters
-----------------------------------

``limit``
  default: 20

``offset``
  default: 0

  The offset into the list of matched objects. For example, if ``offset=10`` is
  passed to an endpoint, the first 10 records that match the query will not be
  returned, the response will begin with the 11th object

  *note - For the /v1 api, the limit / offset is applied after the queryset is
  returned.  Since most of the object lists are small this isnt a huge issue
  , however it is to be of note when querying the location endpoint which returns
  20k+ results*

``format``
  default: ``json``

  One of either ``json`` or ``csv`` that determines the format of the response

``simple_evaluation``

.. code-block:: json

  /api/v1/indicator/?id=21
  /api/v1/indicator/?slug=number-of-all-missed-children


``__in``

pass a list of values and retrieve one result for each match

.. code-block:: json

    /api/v1/indicator/?id__in=21,164


``__gt; __lt; __gte; __lte``

.. code-block:: json

    /api/v1/campaign/?start_date__lte=2015-01-01
    /api/v1/campaign/?start_date__gte=2015-01-01
    /api/v1/office/?id__gt=2
    /api/v1/office/?id__lt=2

``__contains; __starts_with``

filter resources with simple string functions.

.. code-block:: json

  /api/v1/indicator/?name__startswith=Number
  /api/v1/indicator/?name__contains=polio


* Note - These query parameters are taken directly from the Django ORM.  For
  more on how these work see here:*
  https://docs.djangoproject.com/en/1.8/topics/db/queries/#field-lookups

API Methods
-----------

``/api/v1/datapoint/``
++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.datapoint.DatapointResource


``/api/v1/campaign/``
+++++++++++++++++++++

.. autoclass:: rhizome.api.resources.campaign.CampaignResource

``/api/v1/indicator/``
++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.indicator.IndicatorResource

``/api/v1/location/``
+++++++++++++++++++++

Return a list of location definitions in accordance to the schema melow.

This endpoint will only return locations that the user has permissions for.  In
this case, and in all other instances of GET requests dealing with locations,
and location_ids, we use the ``fn_get_authorized_locations_by_user`` stored
procedure which gets recursively the list of location_ids that a user can
access.


Custom Parameters
~~~~~~~~~~~~~~~~~

``depth_level``
  - default = 0
  - the depth parameter controls how far down the location tree the API should
    traverse when returning location data.
  - a parameter of 0 returns ALL data, while a parameter of 1 retreives
    locations at most one level underneath the locations avaliable to that user.
    -> that is if a user has permission to see Nigeria only, and they pass
    a depth=1 parameter, they will see data Nigeria, as well as for the
    provinces but not for districts, sub-districts and settlemnts.

``read_write``
  - default = r
  - This controls whether or not the application needs to see data a user can
    READ or WRITE to.

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>,
      slug: <String>
      latitude: <Number>,
      longitude: <Number>,
      location_code: <String>,
      location_type: <String>,
      shape_file_path: <String>,
      office: <reference>,
      parent_location: <reference>,
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
represent different parts of the organization that oversee locations. For example,
there might be an office for Nigeria that represents the Nigerian Country
Office. The location Nigeria that represents the country, as well as all of its
sub-locations, would be associated with the Nigeria office.

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

``/api/v1/campaign_type/``
++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.campaign_type.CampaignTypeResource

``/api/v1/location_type/``
++++++++++++++++++++++++++

List of location types ( each location must have a location type ).  For now we are
dealing with Country, Province, District, Sub-District and Settlement.

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name:<String>,
    }],

    errors: {...}
  }


``/api/v1/indicator_tag/``
++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.indicator_tag.IndicatorTagResource


.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      tag_name:<String>,
      parent_tag_id:<Number>
    }],

    errors: {...}
  }


``/api/v1/location_map/``
+++++++++++++++++++++++++

TODO - Needs documentation


``/api/v1/source_doc/``
+++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.document.DocumentResource


``/api/v1/document_review/``
+++++++++++++++++++++++++++++

TODO - Needs documentation


``/api/v1/custom_dashboard/``
+++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.custom_dashboard.CustomDashboardResource

``/api/v1/group_permission/``
+++++++++++++++++++++++++++++

The list of indicators each group has permissions to and vice versa.
For instance to see what groups have permission to view indicator_id 21, simply
pass:

'/api/v1/group_permission/?indicator=21'

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      indicator_id <Number>,
      group_id <Number>,
    }],

    errors: {...}
  }


``/api/v1/group/``
++++++++++++++++++

.. autoclass:: rhizome.api.resources.group.GroupResource


``/api/v1/user/``
+++++++++++++++++

The list of users in the application.  All filters outlined above are avaliable
here to all of the fields included in the response.

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      username: <Text>,
      first_name: <Text>,
      last_name: <Text>,
      is_active: <Boolean>,
      is_superuser: <Boolean>,
      is_staff: <Boolean>,
      last_login: <Datetime>,
      email: <Text>,
      date_joined:<Datetime>,
    }],

    errors: {...}
  }


``/api/v1/location_responsiblity/``
+++++++++++++++++++++++++++++++++++

This endpoint tells which locations a user is responsible for. 

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      read_write: <Text>,
      user_id: <Number>,
      location_id: <Number>
    }],

    errors: {...}
  }


``/api/v1/user_group/``
+++++++++++++++++++++++++

This endpoint tells which groups a user is in and vice versa.

For instance to see all the groups user_id 1 is in .. simply pass the following
url to the application:

'/api/v1/user_group/?user=1'


.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      group_id: <Number>,
      user_id: <Number>,
    }],

    errors: {...}
  }

``/api/v1/agg_refresh/``
++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.agg_refresh.AggRefreshResource

``/api/v1/cache_meta/``
+++++++++++++++++++++++

TODO - Needs documentation

``/api/v1/location_map/``
+++++++++++++++++++++++++

TODO - Needs documentation

``/api/v1/indicator_id/``
+++++++++++++++++++++++++

TODO - Needs documentation

``/api/v1/chart_type/``
+++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.chart_type.ChartTypeResource

``/api/v1/computed_datapoint/``
+++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.computed_datapoint.ComputedDataPointResource

``/api/v1/custom_chart/``
+++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.custom_chart.CustomChartResource

``/api/v1/datapointentry/``
+++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.datapoint_entry.DatapointEntryResource

``/api/v1/doc_datapoint/``
++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.doc_datapoint.DocDataPointResource

``/api/v1/doc_detail_type/``
++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.doc_detail_type.DocDetailTypeResource

``/api/v1/transform_upload/``
+++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.doc_trans_form.DocTransFormResource

``/api/v1/doc_detail/``
+++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.document_detail.DocumentDetailResource

``/api/v1/geo/``
++++++++++++++++

.. autoclass:: rhizome.api.resources.geo.GeoResource


``/api/v1/homepage/``
+++++++++++++++++++++

TODO - Needs documentation


``/api/v1/indicator_to_tag/``
+++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.indicator_to_tag.IndicatorToTagResource

``/api/v1/queue_process/``
++++++++++++++++++++++++++

TODO - Needs documentation

``/api/v1/refresh_master/``
+++++++++++++++++++++++++++

TODO - Needs documentation

``/api/v1/source_object_map/``
++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.source_object_map.SourceObjectMapResource

``/api/v1/source_submission/``
++++++++++++++++++++++++++++++

TODO - Needs documentation

``/api/v1/odk_form_id/``
++++++++++++++++++++++++

TODO - Needs documentation


``/api/v1/all_meta/``
+++++++++++++++++++++

.. autoclass:: rhizome.api.resources.all_meta.AllMetaResource

``/api/v1/indicator_calculation/``
++++++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.calculated_indicator_component.CalculatedIndicatorComponentResource


