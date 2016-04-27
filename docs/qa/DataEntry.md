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