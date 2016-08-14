Core Application Resources
==========================

While there are a number of tangential api calls that the application makes, the above description of the BaseModeLReource should give a good idea as to how to handle them.

However, when it comes to making the application work, we have a number of core requests that allow us to provide data for our core functionaliy.

These endpoints are listed in relative importance to the application.

``/api/v1/date_datapoint/``
++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.date_datapoint.DateDataPointResource

``/api/v1/campaign_datapoint/``
++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.campaign_datapoint.CampaignDataPointResource

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
