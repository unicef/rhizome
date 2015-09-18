*******
Project
*******

ODK
===

The ODK process is kicked off by a cron job that runs once an hour.

The cron job kicks off a file: <refresh_odk.sh>

Which does the following:
  - Makes an API request to the app saying "starting_odk_jar"
  - Runs the ODK Jar file for the relevant forms.
  - Makes an API request to the app saying "done_with_odk_jar"
  - Makes an API request that says "ingest_odk_locations"
      -> Takes any new locations from the vcm_settlement form and merges them into the source_location table
      -> A new source_location must have a parent_location_code.
      -> Adds Lon/Lat when able
  - Makes an API request that says "convert_odk_ingest_to_document"
      -> For how ever many forms there are, create one document for each form
         that has incremental data.
      -> would be nice to link cache_job_id and document_id here
  - Makes an API call that says "odk_docs_to_source_dps?cache_job_id=<x>"
      -> For each document in this cache job, create a bunch of source_datapoints
  - Makes an API call that says "odk_source_dps_to_master?cache_job_id=<x>"
      -> For each document id, refresh master
  - /odk_review shows what has been ingested and when!


ODK Info Page
~~~~~~~~~~~~~




Master Refresh
==============

Cache Refresh
==============
