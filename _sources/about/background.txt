Background
==========

The Rhizome platform was funded by UNICEF Headquarters to assist in the Polio Eradication Intiative.

The purpose of the platform was to provide both Headquarters, and country offices transparancy into the data captured during the Polio campaigns in the three endemic countries Pakistan, Afghanistan anad Nigeria.

The difficulty in designing and building this platform is that those who funded this project, wanted for this platform to not only meet the needs of the polio program, but also in the future to be applicable to other program areas in UNICEF and the United Nations.

The U.N. has been using `Dev Info <http://www.devinfo.org/>`_. for many years, but has been looking for a cheaper more flexible and modern software platform to perform analysis, monitoring and evaluation on core programs.

To date, the Rhizome platform has one major implementation which is in Afghanistan in the EOC ( Emergency Operations Center ) in Kabul.  The platform currently supports the program with four main dashboards, all of which are rendered via configurations in the database.  That is -- they are not hardcoded dashboards.

While the only production level implementation of the software is in Kabul, there are a number of other instances of the software that have been deployed as an attempt to visualize data for other UNICEF Areas.

As the platform has been funded and supported by the polio program, we have had to deliver for their needs, which specifically involve analysis over Polio Campaigns.  While this idea is for the most part unique to Polio, we have also engineer the ability to store data based on Dates.

Thus the data model has two main ways of describing facts in the system:

**Campaign**

.. code-block:: json

   {
       location: {},
       indicator: {},
       campaign: {}
       value: 0.0
   }

Ex: In Kandahar District Afghanistan ( location ) were 220 Missed Children ( indicator ) in the August Polio Campaign ( Campaign )

**Date**

.. code-block:: json

   {
       location: {},
       indicator: {},
       data_date: {}
       value: 0.0
   }

Ex: In Kandahar District Afghanistan ( location ) was one (value ) case of polio ( indicator ) on Friday August 12th ( Date )

The Date data model is much more flexible, for instance we could use this data model to say

In Zambia ( location ) the GDP ( Indicator ) for 2015 (date) was 21.20 Billion USD ( Value)

or

In Al-raqqa Province Syria ( location ) in the month of July (date) there were 2200 ( value ) new refugees ( Indicator ).
