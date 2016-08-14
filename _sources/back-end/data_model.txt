Data Model
==========

Datapoint Models
----------------

``DataPoint``
+++++++++++++

.. autoclass:: rhizome.models.datapoint_models.DataPoint


``DocDataPoint``
+++++++++++++

.. autoclass:: rhizome.models.datapoint_models.DocDataPoint


Document Models
---------------

``Document``
+++++++++++++

.. autoclass:: rhizome.models.document_models.Document


document.transform_upload()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes a file and moves the file data into the ``source_submission`` table which stores one row in the table for one row in the CSV.

.. automethod:: rhizome.models.document_models.Document.transform_upload

document.refresh_master()
^^^^^^^^^^^^^^^^^^^^^^^^^

This method takes the data for a document, and takes the source submissions ( rows in a csv ), maps them and syncs them to the DataPoint Table.


.. automethod:: rhizome.models.document_models.Document.refresh_master


``SourceSubmission``
++++++++++++++++++++

.. autoclass:: rhizome.models.document_models.SourceSubmission


``SourceObjectMap``
+++++++++++++++++++

.. autoclass:: rhizome.models.document_models.SourceObjectMap

Indicator Models
-----------------

``Indicator``
+++++++++++++

.. autoclass:: rhizome.models.indicator_models.Indicator

Location Models
-----------------

``Location``
+++++++++++++

.. autoclass:: rhizome.models.location_models.Location

``LocationPolygon``
+++++++++++++

.. autoclass:: rhizome.models.location_models.LocationPolygon

Campaign Models
-----------------

``Campaign``
++++++++++++

.. autoclass:: rhizome.models.campaign_models.Campaign

.. automethod:: rhizome.models.campaign_models.Campaign.aggregate_and_calculate

.. automethod:: rhizome.models.campaign_models.Campaign.agg_datapoints

.. automethod:: rhizome.models.campaign_models.Campaign.calc_datapoints

.. autoclass:: rhizome.models.campaign_models.AggDataPoint

.. autoclass:: rhizome.models.campaign_models.DataPointComputed


Dashboard Models
-----------------

``Custom Chart``
++++++++++++++++++++

.. autoclass:: rhizome.models.dashboard_models.CustomChart

``Custom Dashboard``
++++++++++++++++++++

.. autoclass:: rhizome.models.dashboard_models.CustomDashboard
