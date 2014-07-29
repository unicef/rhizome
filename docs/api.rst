API
===

Here is an example as to how to POST a new indicator

.. code-block:: python
   :linenos:

    import ast
    import json
    import requests

    ENDPOINT = 'http://127.0.0.1:8000/api/v1/indicator/'
    USERNAME = 'myUsername'
    API_KEY  = 'myApiKey'

    def test_indicator_POST():

        data = '{"name": "this is a test","description": "this is also a test"}'

        payload = ast.literal_eval(data)
        url = ENDPOINT + '?username=' + USERNAME + '&api_key=' + API_KEY
        headers = {'content-type': 'application/json'}

        r = requests.post(url, data=json.dumps(payload), headers=headers)

        print r.status_code

        # see below for more information on dealing with the requests module
        # http://docs.python-requests.org/en/latest/user/quickstart/

    if __name__ == "__main__":
        test_indicator_POST()


.. automodule:: datapoints.api
   :members:
