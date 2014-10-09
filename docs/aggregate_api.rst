Aggregate Api
=============

When making a call to the aggregate api the first required parameter is "api_method"

Each API Method has a set of data that it expects, and uses to return a calculation.

This page documents the various api methods associated with the Aggregation api along with examples, sample results and explanations of the calculation.

NOTE:  The application will have to know the IDs before submitting requests.


.. py:function:: calc_pct_solo_region_solo_campaign(region_solo,campaign_solo,indicator_part,indicator_whole)


  Takes one campaign, one region, a indicator that represents a numerator (indicator_part) and another that represents the denominator (indicator_whole)

  *Calculation*

   - Find two datapoints
       1. DataPoint.objects.filter(region_id = region_solo, campaing_id = campaign_solo, indicator_id = indicator_part)
       2. DataPoint.objects.filter(region_id = region_solo, campaing_id = campaign_solo, indicator_id = indicator_whole)
   - Calculate the final result as the Part over the Whole and Return the result as a decimal

  Example: "Show me the percentage of children missed due to refusal in Jigawa" (see below)

  .. code-block:: python

      import urllib,urllib2,json

      API_URL = 'http://localhost:8000/api/v1/aggregate/'

      request_dict = {
      "format": "json",
      "api_method" : "calc_pct_solo_region_solo_campaign",
      "region_solo" : 14881,   # Jigawa
      "campaign_solo" : 14046, # nigeria-april-2014
      "indicator_part" : 1643, # Total Missed Due to Refusal
      "indicator_whole" : 1626 # Total Missed
      }

      url = API_URL + "?" + urllib.urlencode(request_dict)
      data = urllib2.urlopen( url )
      json_response = json.load ( data )

      print json_response

      data.close()

      # {
      #    u'meta':{u'previous': None, u'total_count': 1, u'offset': 0, u'limit': 20, u'next': None},
      #    u'objects': [{u'DATA': u'0.07534246575342465753424657534'}]}
      # }



.. py:function:: calc_pct_parent_region_solo_campaign(region_parent,campaign_solo,indicator_part,indicator_whole)

   Takes a parent region, finds all sub regions (with one level of depth) and returns a ratio given indicators representing the *part* and the *whole*

    *Calculation*

     - Find all sub regions for the parent region
     - for each sub region:
         - find the value for the "part"
         - find the value for the "whole"
     - return the sub of the Parts over the sum of the Wholes


    Example: "Show me the percentage of children missed due to refusal in all of Nigeria" (see below)

    .. code-block:: python

        import urllib,urllib2
        import pprint as pp
        import json

        API_URL = 'http://localhost:8000/api/v1/aggregate/'

        request_dict = {
        "format": "json",
        "api_method" : "calc_pct_parent_region_solo_campaign",
        "region_parent" : 22454,
        "indicator_whole" : 1626,
        "campaign_solo" : 14046,
        "indicator_part" : 1643
        }

        url = API_URL + "?" + urllib.urlencode(request_dict)
        data = urllib2.urlopen( url )
        json_response = json.load ( data )

        print json_response

        data.close()

        # {
        #   u'meta': {u'previous': None, u'total_count': 1, u'offset': 0, u'limit': 20, u'next': None},
        #   u'objects': [{u'DATA': u'0.1672584326654831346690337307'}]
        # }












..
    **GET REQUESTS**

    This resource is GET only.  You will not be able to post data to this resource
    because by its definition, this API generates aggregated data as opposed to
    simply report on data that is physically stored in the database.

    In the example below, given the length of some of the requests we make, i will
    write a sample script in which i interface with the API from python as opposed
    to with a URL or curl request.

    **How the Aggregate API Works**

    The idea behind the Aggregate resource, is that we want for our api, and our
    front end reporting and visualization framework to be able to retrieve data
    with a number of aggregation techniques.  A few example, that our aggregation
    framework is meant to support:

    * Show me the average number of children missed per region in Nigeria
    * Show me the median percentage of refusals over the last two campaigns in
    Region x
    * Sow me the min and max number of children vacinated for x,y, and z regions

    The idea here is that given the data that we capture and store around polio,
    our aggregation framework allows for flexible analysis on the core data set.


    **When the Aggregate API receives a Request**

    * parse the argument passed into "api_method"
    * parse the indicator, region, campaign from the URL and find their IDs
    * for that api_method, look up the value in the aggregation_type table
    * for that aggregation type, join to find the relevant data in
    aggregation_expcected_data
        * at this point you should know what data is required in order to make the
          necessary calculation given the campaign, region, indicator etc
    * Match the "expected data" with the data parsed from the URL
    * If the data passed through the URL matches the requirements from the
      expected_data, then call the function passed through the api_method param with
      the keyword arguments of indicator, region, campaign etc.
    * Execute the function passed in and return the relevant data back to the API.


    .. code-block:: python
       :linenos:

        import urllib,urllib2
        import pprint as pp
        import json

        API_URL = 'http://localhost:8000/api/v1/aggregate/'
        API_KEY = '3018e5d944e1a37d2e2af952198bef4ab0d9f9fc'


        def api_request(**kwargs):
              json_response = {}

              ## update the request obect with attribtues
              ## that are shared with all API requests
              kwargs.update({
                  "api_key": API_KEY,
                  "format": "json",
                  "username" : "john",
                  "api_method" : "calc_pct_single_reg_single_campaign",
                  "region_slug" : "11-lpds-of-south-region",
                  "indicator_part" : "number-of-children-missed-due-to-refusal-to-accept-opv",
                  "indicator_whole" : "number-of-children-missed-total",
                  "campaign_slug" : "nigeria-2019-10-01",
              })


              ## Encode the request into a URL
              url = API_URL + "?" + urllib.urlencode(kwargs)
              print 'URL: ' +  url

              try:
                  # Send Request and Collect it
                  data = urllib2.urlopen( url )
                  # decode json
                  json_response = json.load ( data )

                  data.close()

              # provive URL and HTTP exceptions for API requests
              except urllib2.HTTPError, e:
                  print "HTTP error: %d" % e.code
              except urllib2.URLError, e:
                  print "Network error: %s" % e.reason.args[1]

              pp.pprint(json_response)
              return json_response

        if __name__ == "__main__":
            api_request()
