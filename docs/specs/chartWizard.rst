*****************
Rhizome Tech Spec
*****************

Overview
========

Heat Map Matrix
===============
  - This is a way to create a heat map matrix for a custom set of indicators.
  - See district dashboard: http://rhizome.work/datapoints/district-dashboard/Afghanistan/2014/11/
  - User needs to be able to define "cutoffs" for values of particular indicators
  - Value for the indicator value needs to show inside the cell.
  - On Hover -- show indicator_name, campaign and value.

As a baseline explination of why the user needs this functionality please see below:

Email Exchange
~~~~~~~~~~~~~~

Below is an email, embedded with relevant attachments that explains the request for the functionality below.

*I am in Afghanistan setting dashboards that will be used to monitor the vaccination campaigns. We have pre-, intra- and post-campaign dashboards. These dashboards are traffic lights only.
So far, all of them are tables. See attached:*

**Pre Campaign**

.. image:: http://s29.postimg.org/77n38onjb/Screen_Shot_2015_12_07_at_2_33_31_PM.png
   :width: 500pt

**Intra Campaign**

.. image:: http://s17.postimg.org/slag66jqn/Screen_Shot_2015_12_07_at_3_06_57_PM.png
   :width: 500pt

**Post Campaign Snapshot**

.. image:: http://s7.postimg.org/jagdrh5ej/Screen_Shot_2015_12_07_at_2_41_33_PM.png
   :width: 500pt

**Post Campaign Trend**

.. image:: http://s18.postimg.org/b3dy91oy1/Screen_Shot_2015_12_07_at_2_41_40_PM.png
   :width: 500pt

*During the management meetings when these dashboards will be reviewed, people would like to see them presented as table. And then maybe some charts in a second time, but table is the first ask.*

*Bottom line is, if we want people to adopt Rhizome as the partnership database here, having the possibility of creating these tables directly on the platform where the data is stored rather than download the data and use excel would be an important condition.

*So, when choosing a layout for the dashboard, I would like to add the possibility of creating a table as a fourth layout.
The wizard would then be about defining the number of indicators (columns), number of regions (lines), and then selecting these indicators and regions in our drop down. After that, for each indicator, the user should be able to define cut-of values (either Y/N, or thresholds for bad/average/good) which will drive the color of the cell (red, yellow, green).*


Creating a Table via the Chart Wizard
--------------------------------------


Technical Details
-----------------

Using the email above, i have transformed an abstracted specification as to how this type of chart could be customized rendered and rendered in the browser.

The ultimate objective is to be able to create all of the three tables exactly as they are rendered in excel, but with this new chart type.

The specific objective for this is to be able to create the dashboard below, in rhizome given the technical specifications below:



Map
~~~

.. image:: http://s13.postimg.org/6b7t8ltgn/Screen_Shot_2015_12_07_at_3_03_31_PM.png
   :width: 500pt

- Ability to Dynamically select indicators via drop down on map.
    -> user selects a number of new Indicators in chart wizard
    -> when a dashboard is rendered, drop down at top right where user can pick and choose indicators that will be dynamically updated.
