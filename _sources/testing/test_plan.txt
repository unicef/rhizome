Test Plan
=========

Data Entry
----------

# Quality Assurance Procedure for Data Entry

### High Level Functionality

  * Click campaign dropdown and check if all campaigns are available.
  * Click dashboard dropdown(below dashboard navigation) and check if all dashboards are available.
  * Click location dropdown and check if all locations are available. Type 'Kabul' in the search drop down for locations to find Kabul.
  * Type 'Uru' and it should not show any search suggestions. (3 letters does not trigger search until 4th is typed in.)

##### Load table
  * Below the these drop down selections there should be an empty area designated for data entry to load.(unless a table for data entry was already loaded)
  * Click on add location and input 'Hilmand' and click on the location in the drop down menu. The other dropdowns to the left of this should be something along the lines of January 2016 and Pre Campaign. I state it as something along the lines because this data is subject to change.
  * A table with 2 rows should have loaded. First row is the 'table header' row, with multiple indicators, one for each column. Second row is the table data row. The very left, beginning, of the table data row should indicate 'Hilmand'. In each column, in the Hilmand data row, there should be a value, or potentionally no value. If there is a value the editable cell, which is a cross section of this table row and header, should be white in color and indicate a value. If any indicator has 'No Data' or is empty it should be greyed out.
  * This value may be numeric or a word. For example, some indicators will be a percentage(ex: 11%) or an integer(ex: 325), while some are boolean and indicate true or false(ex:'Yes'). If the indicator is 'Event meeting conducted' the value should be 'Yes', 'No', or 'No Data', if data was not collected. 'Percentage children missed' indicator should state a percentage, for example, '12%'. 'LQAS' indicator is an integer, and should have a basic number value, for example, '235'.
  * Verify all columns and values in cell follow the rules stated above in this section.

### Low Level Functionality

##### Update cell value
  * Click into the cell for a percentage indicator, there should now be a keyboard cursor in the cell. It should allow you to edit the number that is already there or if it is blank you can input a new number.
  * Input '99'. Now either click outside of the data table or press enter. This should show a small loading icon in the cell and then save. You may or may not see the loading icon depending how fast it saves. It should display '99%' for this cell.
  * Click outside the table or press enter to save.
  * Make note of this indicator name and value.
  * Let's edit a couple other cells and we will test if the database has saved these changes. Find one of the boolean indicators. These are cells which allow you to enter 1 of the 3, 'Yes', 'No' or 'No Data'.
  * Input either data if it is 'No Data' or the opposite answer('Yes' if 'No' etc.).
  * Click outside the table or press enter to save. It should now display the value you have selected. Make note of which indicator name this is and it's value.
  * Next, update an indicator with an integer value. This may be an indicator of 'LPD Status' or 'Number of children missed', for example. Let's input '777'. Click outside the table or press enter to save. This should have the same saving behavior as the percentage indicator. It should display '777' now in the cell.
  * Again, make note of this indicator name and value. If the values are showing after having changed the 3 indicators, let us test one more thing for this.
  * Refresh your browser. Select the same dropdowns we originally clicked to return to this state(Jan 2016, Pre Campaign, Hilmand, etc.)
  * Double check the 3 indicators and their values. The corresponding indicators should still have the new values which you entered.

##### Remove cell value
  * Let's use the same indicators we used to update the values. For each of those change the values, one by one, to ''(empty cell). For the boolean select 'No Data'.
  * Click outside the table or press enter to save. This should result in the value being removed, a blank cell, or 'No Data' for boolean and the cells should also have turned grey in color.
  * Refresh the browser and load the Hilmand data table again(Jan 2016, Pre Campaign, Hilmand, etc.)
  * Verify the values are still removed and that the cells are grey.

##### Remove cell value and then input a value
  * Choose a percentage indicator and remove it's value and update the table(press enter). It should now display ''(empty). Now let's add a value back into this same cell. Input '77' it should display '77%'.
  * Let's refresh the browser and return to this state again(Jan 2016, Pre Campaign, Hilmand, etc.) The cell should display '77%'.

##### Remove cell value, after browser refresh update value
  * Let's use the same indicators we used to update the values. For each of those change the values, one by one, to ''(empty cell). For the boolean select 'No Data'. This should result in the value being removed, a blank cell, or 'No Data' for boolean and the cells should also have turned grey in color.
  * Refresh the browser and load the Hilmand data table again(Jan 2016, Pre Campaign, Hilmand, etc.) Now let's update this cell with a valid value, it should display your value. Refresh the browser and return.
  * It should have the value you had input into the cell.

##### Add values to row and remove row
  * Add locations Bagrami, Kabul, Uruzgan.
  * In the middle of the 3 locations(generally Kabul) row input valid values for each indicator possible.
  * Let's input all variations of valid data for each cell. So for percentage that is anything greater than 0 to 100, also a blank percentage cell should be at least one indicator in the row. Same for boolean, mostly 'Yes' or 'No' and one 'No Data'. Integers can be any range, 0 to infinity(stick to 200,000 being maximum). Also one indicator with blank data.
  * Now simply remove the location by clicking the little X at the beginning of the table row. The values in the other two rows should not change, and they definitely should not inherit any information from the middle row that was just removed.
  * Find the middle row location(Kabul if it was Kabul) from the Add Location dropdown and add it again. It should have all of the new changed values which you had just input.
  * Verify each cell value to indicator name.

##### Add values to row and change campaign
  * Add locations Bagrami, Kabul, Uruzgan.
  * Keep note of which campaign selected.
  * For Uruzgan row put input valid values for each indicator possible.
  * Let's input all variations of valid data for each cell. So for percentage that is anything greater than 0 to 100, also a blank percentage cell should be at least one indicator in the row. Same for boolean, mostly 'Yes' or 'No' and one 'No Data'. Integers can be any range, 0 to infinity(stick to 200,000 being maximum). Also one indicator with blank data.
  * Now switch campaign to a different campaign.
  * Click on Uruzgan location.
  * The data should not reflect what you have entered.
  * Return to the original campaign which was selected.
  * Select the locations again, Bagrami, Kabul, and Uruzgan.
  * Verify each cell value to indicator name for Uruzgan contain your updated values.


  // more test cases should be added to verify dashboard configurations and combinations


Situational Dashboard
---------------------

# Quality Assurance Procedure for Dashboard
## High Level Functionality
### Options
  * Unless the user is a 'super user', the edit dashboard functionality should not be available.
  * If you are able to click edit, it should change the button to a 'Save Dashboard' button. To the right of this is an option to cancel the edit, indicated by a small 'x' icon.
  * Changing the name of the dashboard name and clicking save should save. Let's do that and refresh the browser and see if the new updated name exists. Once loaded you should see the new dashboard name.
  * Lets do the same thing, but not save. Click edit, type in a new dashboard name. Press cancel(before saving). This should not save the name. Lets refresh the browser to confirm this.
### Dropdown Navigation
  * Campaigns drop down should exist. Clicking this will show campaign options to click on.
  * Locations drop down should exist. Clicking this will show location options to click on.
  * Districts drop down should exist. Clicking this will show district options to click on.
  * When selecting a campaign from this drop down, it should update any charts with a campaign display. See in 'Layout' for which rows may contain charts with campaign information visible to the user. These charts should each reflect the current selection for campaign name.
  * When selecting a location from this drop down, it should update any charts with a location display. See in 'Layout' for which rows may contain charts with location information visible to the user. These charts should each reflect the current selection for location name.
  * When selecting a district from this drop down, it should update any charts with a district display. See in 'Layout' for which rows may contain charts with district information visible to the user. These charts should each reflect the current selection for district name.
### Layout
  * All of the elements should exist:
  * Row 1
    * On the left side of the row there is a section for a bubble map showing with a title of 'Polio Cases - 2014 to Present' with a map and bubbles indicating the intensity.
    * On the right side of this row, there are two charts stacked on top of each other. 'Annual Cast Table' this is a basic data table chart with Afghanistan and recent campaigns displaying their indicator data.
    * Below 'Annual Case Table' is the Immunity Profile stacked column chart. The X Axis should reflect years, grouped into regions, 'central, 'central highlands', 'east', 'north', 'north east', 'south', 'south east' and 'west'. Y axis should show percent, 0%-100%. The indicators shown are 'Number of Unvaccinated Non Polio AFP Cases', 'Number of Non Polio AFP cases vaccinated 1-3 doses', 'Number of Non Polio AFP cases vaccinated 4-6 doses', 'Number of Non Polio AFP cases vaccinated 7+ doses'. The chart itself should display the proportion of the value of each indicator listed in the legend as a vertical column. The bar size should make sense. What this means is if 'percent missed due to refusal' has a value of 0.9% and 'percent children missed due to not available' value is 0.1%, 'percent missed due to refusal should be 90% of the column and 'percent children missed due to not available' should color 10% of the column. Each indicator should be displayed by the assigned legend color. The values, when mouse hovers on the column, should display as a small modal tooltip. Clicking the button next to the 'export' button will toggle the view of the chart. There are two other views than the side-by-side column chart. One is the stacked columns by proportion based on their exact values. The other view is based on the values as well however the visualization will stretch the column to 100%. The values in this second view will be shown in proportion to their value.

  * Row 2
    * One stacked column chart 'Missed Children By Reason' displaying percent childrens missed by specific reasons, 'Percent children missed due to refusal - PCA', 'Percent children missed due to not available - PCA', 'Percent children missed due to no team visit - PCA', 'Percent children missed due to other reasons - PCA'. X axis should indicate campaign (month and year) grouped by region. Regions should be 'central, 'central highlands', 'east', 'north', 'north east', 'south', 'south east' and 'west'. Y axis should default to percentage(0%-100%). The chart itself should display the proportion of the value of each indicator listed in the legend as a vertical column. The bar size should make sense. What this means is if 'percent missed due to refusal' has a value of 0.9% and 'percent children missed due to not available' value is 0.1%, 'percent missed due to refusal should be 90% of the column and 'percent children missed due to not available' should color 10% of the column. Each indicator should be displayed by the assigned legend color. The values, when mouse hovers on the column, should display as a small modal tooltip.
    * Clicking the button next to the 'export' button will toggle the view of the chart. There are two other views than the side-by-side column chart. One is the stacked columns by proportion based on their exact values. The other view is based on the values as well however the visualization will stretch the column to 100%. The values in this second view will be shown in proportion to their value.
  * Row 3
    * Here we have a stacked column chart displaying 'LQAS'. The indicators for this are '# of Accepted Lots by 90%', '# of Accepted Lots by 80%', '# of Rejected Lots by 80%'. This should show an integer value on the Y axis and the X axis displays campaign month and year grouped by region. Regions should be 'central, 'central highlands', 'east', 'north', 'north east', 'south', 'south east' and 'west'. The indicators should show data in each grouping, unless there is no value or the value is 0, as a column.
    * Clicking the button next to the 'export' button will toggle the view of the chart. There are two other views than the side-by-side column chart. One is the stacked columns by proportion based on their exact values. The other view is based on the values as well however the visualization will stretch the column to 100%. The values in this second view will be shown in proportion to their value.
  * Row 4
    * Here we have a stacked column chart displaying 'Environmental Results'. The indicators for this are 'Number of Environmental Samples with Negative result' and 'Number of Environmental Samples with Positive result'. This should show an integer value on the Y axis and the X axis displays campaign month and year grouped by region. Regions should be 'central, 'central highlands', 'east', 'north', 'north east', 'south', 'south east' and 'west'. The indicators should show data in each grouping, unless there is no value or the value is 0, as a column.
    * Clicking the button next to the 'export' button will toggle the view of the chart. There are two other views than the side-by-side column chart. One is the stacked columns by proportion based on their exact values. The other view is based on the values as well however the visualization will stretch the column to 100%. The values in this second view will be shown in proportion to their value.
  * Row 5
    * Here we have a stacked column chart displaying 'Missed Children: PCA vs. Out of House Survey'. The indicators for this are 'Percent Missed Children - Out of House Survey' and 'Percent Missed Children - PCA'. This should show an integer value on the Y axis and the X axis displays campaign month and year grouped by region. Regions should be 'central, 'central highlands', 'east', 'north', 'north east', 'south', 'south east' and 'west'. The indicators should show data in each grouping, unless there is no value or the value is 0, as a column.
    * Clicking the button next to the 'export' button will toggle the view of the chart. There are two other views than the side-by-side column chart. One is the stacked columns by proportion based on their exact values. The other view is based on the values as well however the visualization will stretch the column to 100%. The values in this second view will be shown in proportion to their value.
  * Row 6
    * This row has 2 charts. The left column has a bubble map. The right column contains a column chart.
    * The bubble map shows Afghanistan with the title of 'Inaccessible Children (Map View)'. This map shows the data by displaying a grey circle. The size of the circle is proportionate to the value of the indicator for that area.
    * The column chart title is 'Inaccessible Children'. The X axis should display the campaign month and year. The Y axis displays the scale of indicator value by integer. The columns are proportionate in size to the value of the indicator for the campaign.
  * Row 7
    * There is one chart for this row, it has two indicators in it. The title of the chart is 'Non Polio AFP Rate and Adequate Specimens'. The indicators are 'Non Polio AFP Rate' which is display as a column chart. The other indicator, 'Percentage of Adequate Specimen', which is displayed as a line chart. The X axis indicates the campaign month and year. The Y axis will reflect the indicator value range as a percentage.
