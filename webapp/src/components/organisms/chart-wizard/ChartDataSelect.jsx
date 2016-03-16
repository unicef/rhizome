import React, { PropTypes } from 'react'
import DateRangePicker from 'components/molecules/DateRangePicker'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'

import ChartActions from 'actions/ChartActions'
import LocationActions from 'actions/LocationActions'
import IndicatorActions from 'actions/IndicatorActions'

const ChartDataSelect = React.createClass({
  propTypes: {
    start_date: PropTypes.object,
    end_date: PropTypes.object,
    locations: PropTypes.shape({
      lpd_statuses: PropTypes.array,
      filtered: PropTypes.array,
      selected: PropTypes.array
    }),
    indicators: PropTypes.shape({
      list: PropTypes.array,
      selected: PropTypes.array
    })
  },

  updateIndicators (indicators) {
    console.log('Indicators changed', indicators)
  },

  updateLocations (locations) {
    console.log('Locations changed', locations)
  },

  render () {
    const props = this.props

    return (
      <div className='medium-3 columns'>
        <div>
          <h3>Time</h3>
          <DateRangePicker
            sendValue={ChartActions.setDateRange}
            start={props.start_date}
            end={props.end_date}
            fromComponent='ChartWizard'
          />
        </div>
        <div className='row data-filters'>
          <br/>
          <IndicatorSelector
            indicators={props.indicators}
            classes='medium-6 columns'
            onChange={this.updateIndicators}
          />
          <LocationSelector
            locations={props.locations}
            classes='medium-6 columns'
            onChange={this.updateLocations}
          />
        </div>
      </div>
    )
  }
})

export default ChartDataSelect
