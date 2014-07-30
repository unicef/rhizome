API
===

Here is an Example on posting a Datapoint using Python

.. code-block:: python
   :linenos:

    import ast
    import json
    import pprint as pp
    import requests

    ENDPOINT = 'http://127.0.0.1:8000/api/v1/datapoint/'
    USERNAME = 'john'
    API_KEY  = '3018e5d944e1a37d2e2af952198bef4ab0d9f9fc'


    def test_datapoint_POST():

        data = '{"indicator": "this-is-a-testxyzhalla" \
        ,"campaign": "/api/v1/campaign/7/" \
        ,"region": "khakrez" \
        ,"value": "1.077"}'

        payload = ast.literal_eval(data) # esure your post data is a dictionary
        url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY

        headers = {'content-type': 'application/json'}

        r = requests.post(url, data=json.dumps(payload), headers=headers)

        print r.status_code  # should 201, if not, see error message in response
        print r._content     # the data we just created

    if __name__ == "__main__":
        test_datapoint_POST()


When posting to the datapoint resource, provide the *slug* of the indicator
region, and campaign.  Click here for the reference data information



.. automodule:: datapoints.api
   :members:
