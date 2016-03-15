import _ from 'lodash'
import React, { PropTypes } from 'react'
import DateRangePicker from 'components/molecules/DateRangePicker'
import List from 'components/molecules/list/List'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

import LocationActions from 'actions/LocationActions'
import IndicatorActions from 'actions/IndicatorActions'

const ChartDataSelect = React.createClass({
  propTypes: {
    start_date: PropTypes.string,
    end_date: PropTypes.string,
    locations: PropTypes.shape({
      lpd_statuses: PropTypes.array,
      filtered: PropTypes.array,
      selected: PropTypes.array
    }),
    indicators: PropTypes.shape({
      list: PropTypes.array,
      selected: PropTypes.array
    }),
    setDateRange: PropTypes.func
  },

  render () {
    const props = this.props
    const location_options = [
      { title: 'by Status', value: props.locations.lpd_statuses },
      { title: 'by Country', value: props.locations.filtered || [] }
    ]

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
                items={props.indicators.list}
                sendValue={IndicatorActions.selectIndicator}
                item_plural_name='Indicators'
                style='icon-button right'
                icon='fa-plus' />
            </h3>
            <a className='remove-filters-link' onClick={IndicatorActions.clearSelectedIndicators}>Remove All </a>
            <ReorderableList items={props.indicators.selected} removeItem={IndicatorActions.deselectIndicator} dragItem={IndicatorActions.reorderIndicator} />
          </div>
          <div className='medium-6 columns'>
            <h3>
              Locations
              <DropdownMenu
                items={location_options}
                sendValue={LocationActions.selectLocation}
                item_plural_name='Locations'
                style='icon-button right'
                icon='fa-plus'
                grouped/>
            </h3>
            <a className='remove-filters-link' onClick={LocationActions.clearSelectedLocations}>Remove All </a>
            <List items={props.locations.selected} removeItem={LocationActions.deselectLocation} />
            <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
          </div>
        </div>
      </div>
    )
  }
})

export default ChartDataSelect
