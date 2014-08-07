Aggregate Api
=============

**GET REQUESTS**

This resource is GET only.  You will not be able to post data to this resource
because by its definition, this API generates aggregated data as opposed to
simply report on data that is physically stored in the database.

In the example below, given the length of some of the requests we make, i will
write a sample script in which i interface with the API from python as opposed
to with a URL or curl request.

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


**AUTO GENERATED DOCUMENTATION FROM DATAPOINTS API**

.. automodule:: aggregate
   :members:
