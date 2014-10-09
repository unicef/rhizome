API
===



**GET REQUESTS**

For the sake of brevity, the username and api key parameters are not
contained in the example strings below.  When testing these in your
application or in curl, dont forget to append your api key.



**Filtering**

For the Datapoint Resource, the following filtering methods are available

These numeric filters are  available on the ID, value, and created_at columns.

Greater Than

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__gt=9

Less Than

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__lt=9

Greater Than or Equal to

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__gte=9

Less Than or Equal to

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/datapoint/format=json&id__lte=9

Range

.. code-block:: python
   :linenos:

    http://polio.seedscientific.com/api/v1/indicator/format=json&id__id__range=9,12


Multiple Objects

Lets say that i want to see data 5 regions (14589,15863,17562,17940)
Simply use the "in" operator on any of the columns avaliable for this resource (indicator,campaign, etc)

.. code-block:: python
   :linenos:

    localhost:8000/api/v1/datapoint/?region__in=14589,15863,17562,17940



Filter By Date of Campaign

  ## TO DO ##
