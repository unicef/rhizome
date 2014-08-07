API
===



**GET REQUESTS**

For the sake of brevity, the username and api key parameters are not
contained in the example strings below.  WHen testing these in your
application or in curl, dont forget to append your api key.



**Filtering**

For the Datapoint Resource, the following filtering methods are available

These numeric filters are  available on the ID, value, and created_at columns.

Greater Than

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/datapoint/format=json&id__gt=9

Less Than

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/datapoint/format=json&id__lt=9

Greater Than or Equal to

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/datapoint/format=json&id__gte=9

Less Than or Equal to

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/datapoint/format=json&id__lte=9

Range

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/indicator/format=json&id__id__range=9,12



Lets say that i wanted to query for all datapoints with IDs between 10 and 20
created after July 1 2014.


**Filtering By Resource**

In order to filter by campaign, region, or indicator you can either pass the slug
of the resource you are filtering on or, the ID.

For instance to see all datapoints for indicator "Pct of children missed
due to child not available" you could pass either

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/indicator/format=json&indicator_slug=pct-of-children-missed-due-to-child-not-available

or if you have the ID and you want to pass that

.. code-block:: python
   :linenos:

    http://localhost:8000/api/v1/indicator/format=json&indicator=11

Both Return the same exact data.

Here is an example of filtering on both indicator and region using the slug

.. code-block:: python
   :linenos:


    http://127.0.0.1:8000/api/v1/datapoint/?format=json&region_slug=kandahar-city&indicator_slug=number-of-children-missed-due-to-refusal-to-accept-opv




**Ordering**


**POST REQUESTS**

When posting to the datapoint resource, provide the *slug* of the indicator
region, and campaign.  Click here for the reference data information.

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

**AUTO GENERATED DOCUMENTATION FROM DATAPOINTS API**

.. automodule:: api.simple
   :members:
