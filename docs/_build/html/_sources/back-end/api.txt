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


API Methods
-----------


``/api/v1/agg_refresh/``
++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.agg_refresh.AggRefreshResource


Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      campaign_type_id: <Integer>,
      created_at: <Date>,
      start_date: <Date>,
      end_date: <Date>,
      id: <Integer>,
      name: <String>,
      office_id: <Integer>,
      pct_complete: <Float>, 
      top_lvl_indicator_tag_id: <Integer>,
      top_lvl_location_id: <Integer>,
    }],

    errors: {...}
  }


``/api/v1/all_meta/``
+++++++++++++++++++++

.. autoclass:: rhizome.api.resources.all_meta.AllMetaResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      campaigns: <List>,
      charts: <List>,
      dashboards: <List>,
      indicators: <List>,
      indicator_tags: <List>,
      indicator_to_tags: <List>,
      locations: <List>,
      offices: <List>,
      is_supeuser: <Boolean>

    }],

    errors: {...}
  }


``/api/v1/cache_meta/``
+++++++++++++++++++++++

TODO - Needs documentation

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        id: <Integer>,
        name: <String>,
        created_at: <Date>
      ],
      errors: {}
   }

``/api/v1/campaign/``
+++++++++++++++++++++

.. autoclass:: rhizome.api.resources.campaign.CampaignResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        campaign_type_id: <Integer>,
        created_at: <Date>,
        start_date: <Date>,
        end_date: <Date>,
        id: <Integer>,
        name: <String>,
        office_id: <Integer>,
        pct_complete: <Float>, 
        top_lvl_indicator_tag_id: <Integer>,
        top_lvl_location_id: <Integer>,
      ],
      errors: {}
   }

``/api/v1/campaign_type/``
++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.campaign_type.CampaignTypeResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        id: <Integer>,
        name: <String>
      ],
      errors: {}
   }

``/api/v1/chart_type/``
+++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.chart_type.ChartTypeResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>
    }],

    errors: {...}
  }


``/api/v1/computed_datapoint/``
+++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.computed_datapoint.ComputedDataPointResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      indicator_id: <Number>,
      location_name: <String>,
      campaign_name: <String>,
      indicator_short_name:<String>,
      value: <Float>
    }],

    errors: {...}
  }


``/api/v1/custom_chart/``
+++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.custom_chart.CustomChartResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      uuid: <String>,
      title: <String>,
      chart_json: <JSON>
    }],

    errors: {...}
  }

``/api/v1/custom_dashboard/``
+++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.custom_dashboard.CustomDashboardResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        id: <Integer>,
        title: <String>,
        description: <String>,
        layout: <Integer>,
        rows: <JSON>,
      ],
      errors: {}
   }

``/api/v1/datapoint/``
++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.datapoint.DatapointResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        indicator_id: <Integer>,
        campaign_id: <Integer>,
        data_date: <Date>,
        computed_id: <Integer>,
        location_id: <Integer>,
        value: <String>
      ],
      errors: {}
   }


``/api/v1/datapointentry/``
+++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.datapoint_entry.DatapointEntryResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        indicator_id: <Integer>,
        campaign_id: <Integer>,
        data_date: <Date>,
        created_at: <Date>,
        computed_id: <Integer>,
        location_id: <Integer>,
        source_submission_id: <Integer>,
        cache_job_id: <Integer>,
        unique_index: <String>
        value: <String>
      ],
      errors: {}
   }


``/api/v1/doc_datapoint/``
++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.doc_datapoint.DocDataPointResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        location_name: <String>,
        indicator_short_name: <String>,
        campaign_name: <String>,
        value: <float>
      ],
      errors: {}
   }

``/api/v1/doc_detail/``
+++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.document_detail.DocumentDetailResource
'id','doc_detail_type_id','doc_detail_type__name',\
                    'document_id', 'doc_detail_value'

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Integer>,
      doc_detail_type_id: <Integer>,
      doc_detail_type_name: <String>,
      document_id: <Integer>,
      doc_detail_value: <String>
    }],

    errors: {...}
  }
     

``/api/v1/doc_detail_type/``
++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.doc_detail_type.DocDetailTypeResource
Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>
    }],

    errors: {...}
  }

``/api/v1/geo/``
++++++++++++++++

.. autoclass:: rhizome.api.resources.geo.GeoResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      location_id: <Integer>,
      type: <String>,
      properties <Dictionary>,
      geometry: <Dictionary>,
      parent_location_id: <Integer>
    }],

    errors: {...}
  }


``/api/v1/group/``
++++++++++++++++++

.. autoclass:: rhizome.api.resources.group.GroupResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        id: <Integer>,
        name: <String>
      ],
      errors: {}
   }

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


``/api/v1/indicator/``
++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.indicator.IndicatorResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

   {
      meta: {},
      objects: [
        short_name: <String>,
        name: <String>,
        description: <String>,
        is_reported: <Boolean>,
        data_format: <String>,
        created_at: <Date>,
        bound_json: <JSON>,
        tag_json: <JSON>,
        office_id: <JSON>,
        good_bound: <Float>,
        bad_bound: <Float>,
        source_name: <String>
      ],
      errors: {}
   }

``/api/v1/indicator_calculation/``
++++++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.calculated_indicator_component.CalculatedIndicatorComponentResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},
    
    objects: [{
      id: <Integer>,
      indicator_id: <Integer>,
      indicator_component_id: <Integer>,
      indicator_component_short_name: <String>,
      calculation: <String>
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


``/api/v1/indicator_to_tag/``
+++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.indicator_to_tag.IndicatorToTagResource
{"id": 146, "indicator__short_name": "Polio From Saliva", "indicator_id": 123, "indicator_tag__tag_name": "Perceived Threat", "indicator_tag_id": 19

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Integer>,
      indicator_short_name: <String>,
      indicator_id: <Integer>,
      indicator_tag_name: <String>,
      indicator_tag_id: <Integer>,
    }],

    errors: {...}
  }

``/api/v1/location/``
+++++++++++++++++++++

.. autoclass:: rhizome.api.resources.location.LocationResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name: <String>,
      latitude: <Number>,
      longitude: <Number>,
      location_code: <String>,
      location_type: <String>,
      office_id: <Number>,
      parent_location_id: <Number>,
      resource_uri: <String>,
      created_at: "YYYY-MM-DDTHH:MM:SS.sss",
    }],

    errors: {...}
  }



``/api/v1/location_responsiblity/``
+++++++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.location_permission.LocationPermissionResource


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



``/api/v1/location_type/``
++++++++++++++++++++++++++
.. autoclass:: rhizome.api.resources.location_type.LocationTypeResource

.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Number>,
      name:<String>,
    }],

    errors: {...}
  }



``/api/v1/odk_form_id/``
++++++++++++++++++++++++

TODO - Needs documentation



``/api/v1/office/``
+++++++++++++++++++

.. autoclass:: rhizome.api.resources.office.OfficeResource

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

``/api/v1/queue_process/``
++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.queue_process.QueueProcessResource


Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Integer>,
      doc_detail_type_id: <Integer>,
      doc_detail_type_name: <String>,
      document_id: <Integer>,
      doc_detail_value: <String>
    }],

    errors: {...}
  }


``/api/v1/refresh_master/``
+++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.refresh_master.RefreshMasterResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      docfile: <String>,
      doc_title: <String>,
      file_header: <JSON>,
      guid: <String>,
      created_at: <Date>,
      id: <Integer>,
      resource_uri: <String>
    }],

    errors: {...}
  }


``/api/v1/source_doc/``
+++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.document.DocumentResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      docfile: <String>,
      doc_title: <String>,
      file_header: <JSON>,
      guid: <String>,
      created_at: <Date>,
      id: <Integer>,
      resource_uri: <String>
    }],

    errors: {...}
  }

``/api/v1/source_object_map/``
++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.source_object_map.SourceObjectMapResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      id: <Integer>,
      content_type: <String>,
      mapped_by_id: <Integer>,
      master_object_id: <Integer>,
      master_object_name: <String>,
      source_object_code: <String>
    }],

    errors: {...}
  }


``/api/v1/source_submission/``
++++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.source_submission.SourceSubmissionResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      document_id: <Integer>,
      instance_guid: <String>,
      row_number: <Integer>,
      data_date: <Date>,
      location_code: <String>,
      campaign_code: <String>,
      location_display: <String>,
      submission_json: <JSON>,
      created_at: <Date>,
      process_status: <String>
    }],

    errors: {...}
  }


``/api/v1/transform_upload/``
+++++++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.doc_trans_form.DocTransFormResource

Response Format
~~~~~~~~~~~~~~~
.. code-block:: json

  {
    meta: {...},

    objects: [{
      docfile: <String>,
      doc_title: <String>,
      file_header: <JSON>,
      guid: <String>,
      created_at: <Date>,
      id: <Integer>,
      resource_uri: <String>
    }],

    errors: {...}
  }

``/api/v1/user/``
+++++++++++++++++

.. autoclass:: rhizome.api.resources.user.UserResource


Response Format
~~~~~~~~~~~~~~~
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

``/api/v1/user_group/``
+++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.user_group.UserGroupResource

Response Format
~~~~~~~~~~~~~~~
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



