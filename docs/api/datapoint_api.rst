DataPoint API
=============


``/api/v1/date_datapoint/``
++++++++++++++++++++++++

.. autoclass:: rhizome.api.resources.date_datapoint.DateDatapointResource

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
