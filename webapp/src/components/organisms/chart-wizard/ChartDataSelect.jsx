import React, { Component, PropTypes } from 'react'
import DateRangePicker from 'components/molecules/DateRangePicker'
import List from 'components/molecules/list/List'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

class ChartProperties extends Component {
  render = () => {
    const props = this.props
    return (
      <div className='medium-3 columns'>
        <div>
          <h3>Time</h3>
          <DateRangePicker
            sendValue={props.setDateRange}
            start={props.start_date}
            end={props.end_date}
            fromComponent='ChartWizard'
          />
        </div>
        <div className='row data-filters'>
          <br/>
          <div className='medium-6 columns'>
            <h3>
              Indicators
              <DropdownMenu
                items={props.all_indicators}
                items={props.all_indicators}
                sendValue={props.addIndicator}
                item_plural_name='Indicators'
                style='icon-button right'
                icon='fa-plus' />
            </h3>
            <a className='remove-filters-link' onClick={props.clearIndicators}>Remove All </a>
            <ReorderableList items={props.selected_indicators} removeItem={props.removeIndicator} dragItem={props.reorderIndicator} />
          </div>
          <div className='medium-6 columns'>
            <h3>
              Locations
              <DropdownMenu
                items={props.all_locations}
                sendValue={props.addLocation}
                item_plural_name='Locations'
                style='icon-button right'
                icon='fa-plus'
                grouped/>
            </h3>
            <a className='remove-filters-link' onClick={props.clearSelectedLocations}>Remove All </a>
            <List items={props.selected_locations} removeItem={props.removeLocation} />
            <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
          </div>
        </div>
      </div>
    )
  }
}

ChartProperties.propTypes = {
  start_date: PropTypes.string,
  end_date: PropTypes.string,
  all_indicators: PropTypes.array,
  all_locations: PropTypes.array,
  selected_indicators: PropTypes.array,
  selected_locations: PropTypes.array,
  addLocation: PropTypes.func,
  removeLocation: PropTypes.func,
  addIndicator: PropTypes.func,
  reorderIndicator: PropTypes.func,
  removeIndicator: PropTypes.func,
  clearSelectedIndicators: PropTypes.func,
  clearSelectedLocations: PropTypes.func,
  setDateRange: PropTypes.func
}

export default ChartProperties