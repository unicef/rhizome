Application User Guide
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
	2. Click on the button "CHOOSE TO UPLOAD
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


Backend Principle Components
============================

Data Ingestion and Aggregation
++++++++++++++++++++++++++++++
The user's upload and mapping corresponds to the following backend procedures and components.

	1. Uploading raw data
	---------------------
	During the upload process, the web app makes two API calls. 
	1. An initial API call to the 'source_doc' endpoint is made when the document is uploaded. This uploads the document to the backend and does some simple validation, such as making sure that uploaded document has the correct file format.

	2. Pressing the "Sync Data" button sends a second API call to the 'transform_upload' endpoint. This initiates the entire cycle of data validation, ingesting and aggregation, preparing the data for use within the application. The cycle is comprised of three main steps:

	DocTransform
	------------
	DocTransform and its subclasses are used to convert a csv file, xlxs file, or pandas DataFrame to a SourceSubmission object. A SourceSubmission object represents a row in the csv file. DocTransform also does some basic data validation for the csv file, such as making sure that the csv file contains required columns for "data_date" or "campaign", and "geocode".

	MasterRefresh
	-------------
	MasterRefresh converts SourceSubmission objects, created by the DocTransform class, into DataPoints. While a SourceSubmission represents a row in the csv file, a datapoint object represents the data that can be extracted from that row. More specifically, datapoints contain values for an indicator collected during a given campaign at a given location. For example, a row might contain entry cells with values for the columns 'campaign', 'geocode', 'Number Missed Children', 'Evening Meeting Conducted'. This would produce two datapoints-- one for "Number Missed Children" and another for "Evening Meeting Conducted". Each of these datapoints would contain the same campaign and location (provided by geocode). Put another way, campaigns and locations are indexes for a given datapoint and are used to collect and aggregate datapoints.

	AggRefresh
	----------
	AggRefresh converts Datapoints into ComputedDatapoints. These two data models are formally similar-- they each contain a value for a single indicator/campaign/location. The key distinction is that they are produced be means of aggregation, and are the product of sums, averages, etc of multiple datapoints for multiple locations, or other indicators. Computed datapoints are the "final product" and are served to the frontend via the data points api. See detailed specs for aggregation further on in the documentation.

	2. Mapping Meta-Data
	--------------------
	If a Source Object Map is created for a given column header, the data for that column will be ingested up through aggregation. If not, a column header needs to be mapped to a Source Object Map, and then "Refresh Master" clicked in order to populate datapoints through aggregation.

	

