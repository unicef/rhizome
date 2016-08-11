CSV / Excel File Uploader
======================

Uploading Data
--------------

Requirements for Uploading Documents
++++++++++++++++++++++++++++++++++++
The application supports data upload from documents with .csv, .xls, and .xlsx file extensions. In order to ensure proper ingestion of data, the following document formatting criteria must be met:
	- All data must be arranged in a strict table format, with column header names on the first row, and column in each subsequent row. See example below:
	- In addition, a document must contain the following column headers: 'geocode', 'location', and 'campaign'. Each row of data must contain a value for these required fields. If one of these header columns is not included in the document (or mislabeled), the document will fail to upload and an error message will be displayed.
	- Values for all fields must be properly formatted based on the indicator data type. If not, the value will be ignored upon aggregation. For example, a numeric indicator with a string value will fail. Percent indicator will accept percent values in the following formats: 0.95 or 95%. Classification indicators will accept string values following very strict guidelines that are determined when the indicator is created.


Procedure for Uploading Documents
+++++++++++++++++++++++++++++++++
Uploading Raw Data
~~~~~~~~~~~~~~~~~~
1. Navigate to: http://localhost:8000/source-data/
2. Click on the button "CHOOSE TO UPLOAD"
3. Select your document from the file explorer
4. Click "Sync Data"
5. Click "Review". This allows you to review the raw data that's been uploaded.

Now we need to map the data so that it can properly be ingested by the analytics system.

Mapping Content
~~~~~~~~~~~~~~~
1. From the review data page, click the "meta-data" button.
2. This page includes a table that contains the column headers from your document. (Reference to as "Source Object Codes" in the table) These need to be mapped to indicators that have been created in the system. If some headers from your file are not included in the table, this is because the mapping has already been provided for the given column header.
3. For each document column that you would like the system to ingest, click the "map!" button corresponding to that header. Make sure to map campaigns and locations, as these are required for aggregation.
4. A popup will appear. Click the "Map Indicator" button to select an indicator.
5. Once you've mapped all the indicators that you'd like to include, click the "Refresh Master" button. This will run the aggregation engine.

Your data has now been added to the system, and can be included in data tables and charts.
