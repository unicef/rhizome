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

