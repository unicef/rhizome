*****************
Table Chart Type
*****************

Overview
========

  - This is a way to create a heat map matrix for a custom set of indicators.
  - See district dashboard: http://rhizome.work/datapoints/district-dashboard/Afghanistan/2014/11/
  - User needs to be able to define "cutoffs" for values of particular indicators
  - Value for the indicator value needs to show inside the cell.
  - On Hover -- show indicator_name, campaign and value.

As a baseline explanation of why the user needs this functionality please see below:

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

*Bottom line is, if we want people to adopt Rhizome as the partnership database here, having the possibility of creating these tables directly on the platform where the data is stored rather than download the data and use excel would be an important condition.*

*So, when choosing a layout for the dashboard, I would like to add the possibility of creating a table as a fourth layout.
The wizard would then be about defining the number of indicators (columns), number of regions (lines), and then selecting these indicators and regions in our drop down. After that, for each indicator, the user should be able to define cut-of values (either Y/N, or thresholds for bad/average/good) which will drive the color of the cell (red, yellow, green).*


Creating a Table via the Data Explorer
--------------------------------------


Technical Details
-----------------

Using the email above, i have transformed an abstracted specification as to how this type of chart could be customized rendered and rendered in the browser.

The ultimate objective is to be able to create all of the three tables exactly as they are rendered in excel, but with this new chart type.

The specific objective for this is to be able to create the dashboard below, in rhizome given the technical specifications below:

    - User

The following is ALWAYS TRUE for every type of table.

    - Rows are locations
    - There is always a column for "parent_location" that shows the parent location of the location for which the data is rendering in that row.
    - The value of the datapoint will show in
          -> if indicator.data_type = "bool" show Yes, or No
          -> if indicator.data_type = "pct" format the percentage
          -> if indicator.data_type = "integer" do not format
    - The hover will show ( for phase one ) simply the indicator.short_name, location.name and campaign.slug
    - Each Cell will be at minimum three times as wide as it is tall.
          -> ( the current district dashboard has a scale for cells equal 1-1 )
    - The cell is colored in accordance to the "indicator bound" ( good, bad, or O.K. )
          -> if no indicator_bound for the indicator is available, use a Normal Distribution of the values to "fake" the indicator bound data between the three thresholds.
          -> phase two we will allow the user to edit the "good", "ok" or "bad" thresholds within the chart wizard,

The following is true for a "single campaign" table:

    - Columns are Indicators
    - Campaign Drop down for the selected country is available at the top right of the "view" page.

The following is true for a "Trend" table:

    - the "primary" indicator shows when the chart is rendered in "view" mode
    - The "secondary indicators" show in a drop down on the top right of the page.  Selecting those, changes the color of the effected locations in the choropleth map

Default Behavior
~~~~~~~~~~~~~~~~

The below will only require four clicks from the user, but will create a sensible matrix chart.

Step 1: Select Country
  -> user selects afghanistan

Step 2: Select Indicator
  - user selects: Missed Children ( 475 )

Step 3: Select Location
      - user click next, and moves to chart type select
    -> If the user goes back and chooses "Kandahar (Province)", then the rows swap out to the "sub locations" of Kandahar, as opposed to the Provinces in Afghanistan.

Step 4: Select Chart Type:

TABLE CHART IS RENDERED WITH DEFAULTS
  - by default, the application renders the following table:
      - rows are  "sub-locations" if Afghanistan ()
      - headers are last 5 campaigns ( ordered by start date descending )
      - cells are the value of the "missed children" indicator, and colored on a "normal distribution" scale in three groups
  - There is also a drop down on the top right of the rendered chart that shows one value for the "primary indicator" selected.  The user can add more indicators to this drop down in step 6.

Step 5: Select Time Range
  - By default the last 3 months are rendering
      -> user has the ability to select a "single campaign" option which will adjust the chart such that the column headers change from "camapign" to "indicators".
      -> if the user selects "single campaign" then there will be one header, in addition to the two location columns, with the "primary indicator" selected in step 2.

Step 6: Customize / Add additional Indicators
   - User Clicks Next.
      -> If the user selects additional indicators and they are added to the drop down.

Step 7: Preview
    - Click Save

Customize Style
~~~~~~~~~~~~~~~

If the user has selected the "table" chart type, then the user will have the following options in adjusting the style:
   - Show a "sum" row as the final row
   - User can select "use bounds" or "use normal distribution"
      - this will allow them to flip between a color distribution that is based on the numbers in the series, or by the "indicator bounds" of the indicator.
      - by default the chart will render the "normal distribution" in order to show colors.
      - The current implementation of the map uses the "normal distribution" logic to plot light red colors ( for low values ) and black for high values.
