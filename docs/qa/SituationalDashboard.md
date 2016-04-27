# Quality Assurance Procedure for Dashboard
## High Level Functionality
### Options
  * Unless the user is a 'super user', the edit dashboard functionality should not be available.
  * If you are able to click edit, it should change the button to a 'Save Dashboard' button. To the right of this is an option to cancel the edit, indicated by a small 'x' icon.
  * Changing the name of the dashboard name and clicking save should save. Let's do that and refresh the browser and see if the new updated name exists. Once loaded you should see the new dashboard name.
  * Lets do the same thing, but not save. Click edit, type in a new dashboard name. Press cancel(before saving). This should not save the name. Lets refresh the browser to confirm this.
### Dropdown Navigation
  * Campaign drop down should exist. Clicking this will show campaign options to click on.
  * Location drop down should exist. Clicking this will show location options to click on.
  * Districts drop down should exist. Clicking this will show district options to click on.
  * When selecting a campaign from this drop down, it should update any charts with a campaign display. See in 'Layout' for which rows may contain charts with campaign information visible to the user. These charts should each reflect the current selection for campaign name.
  * When selecting a location from this drop down, it should update any charts with a location display. See in 'Layout' for which rows may contain charts with location information visible to the user. These charts should each reflect the current selection for location name.
  * When selecting a district from this drop down, it should update any charts with a district display. See in 'Layout' for which rows may contain charts with district information visible to the user. These charts should each reflect the current selection for district name.
### Layout
  * All of the elements should exist:
  * Row 1
    * On the left side of the row there is a section for a bubble map showing with a title of 'Polio Cases - 2014 to Present' with a map and bubbles indicating the intensity.
    * On the right side of this row, there are two charts stacked on top of each other. 'Annual Cast Table' this is a basic data table chart with Afghanistan and recent campaigns displaying their indicator data.
    * Below 'Annual Cast Table' is a stacked column chart for Immunity Profile.
    //update immunity profile information in future for more QA data.

  * Row 2
    * One column chart 'Non Polio AFP Rate and Adequate Specimens' displaying acute flaccid paralysis rates for most recent campaigns. X axis should indicate campaign name, Y axis
  * Row 3
    * Two column charts.
    * First chart (left side) displays 'Inaccessible Children'. Second chart (right side) displays 'Environmental Results'. The X axis for both is campaign name. Y axis displays an integer scale.
  * Row 4
    * Two charts in this row, the left chart, data table chart 'Preparatory Indicators' this is a basic data table chart with Afghanistan and recent campaigns displaying their indicator data.
    * The right side of this row is a data table chart 'Campaign Analysis' this is a basic data table chart with Afghanistan and recent campaigns displaying their indicator data.
    * Both of these charts will display general summary data with percentage bars in them for certain indicators.
  * Row 5
    * Two charts for this row.
    * The chart on the left side is a column chart displaying indicator 'Missed Children PCA vs. Out of House'. The X axis displays campaign name. //update Y axis info.
    * Right side chart is a stacked column chart displaying 'Missed Children By Reason'. X axis indicates the regions, each with their own color. Y axis indicates number in integer form.
  * Row 6
    * Last row has one chart for LQAS data. This is a stacked percentage column chart. The Y axis should be percentages for lot accepted. The X axis is displaying abbrieviated campaign dates.