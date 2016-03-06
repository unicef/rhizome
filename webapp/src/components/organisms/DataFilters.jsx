import React from 'react'
import Reflux from 'reflux'

import ExpandableSection from 'components/molecules/ExpandableSection'
import DataFilter from 'components/molecules/DataFilter'
import DateRangePicker from 'components/molecules/DateRangePicker'

import DataFiltersStore from 'stores/DataFiltersStore'
import DataFiltersActions from 'actions/DataFiltersActions'

let DataFilters = React.createClass({

  mixins: [
    Reflux.connect(DataFiltersStore)
  ],

  propTypes: {
    processResults: React.PropTypes.func.isRequired
  },

  componentWillMount: function () {
    DataFiltersActions.getLocations()
    DataFiltersActions.getIndicators()
  },

  submitQuery: function () {
    if (!this.state.couldLoad) return
    DataFiltersActions.getData(this.state.campaign, this.state.selected_locations, this.state.selected_indicators)
  },

  componentDidUpdate: function(prevProps, prevState) {
    if (this.state.data !== null) {
      this.props.processResults(this.state)
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    let shouldUpdate = nextState !== this.state
    return shouldUpdate
  },

  render: function () {
    return (
      <form className='inline'>
        <DataFilter
          items={this.state.locations}
          selected_items={this.state.selected_locations}
          addItem={DataFiltersActions.addLocation}
          removeItem={DataFiltersActions.removeLocation}
          item_plural_name='Locations'
          text='Select Locations'
          icon='fa-globe'/>

        <DataFilter
          items={this.state.indicators}
          selected_items={this.state.selected_indicators}
          addItem={DataFiltersActions.addIndicator}
          removeItem={DataFiltersActions.removeIndicator}
          item_plural_name='Indicators'
          text='Select Indicators'
          icon='fa-globe'/>

        <ExpandableSection title='Time Period' refer='preview'>
          <DateRangePicker sendValue={DataFiltersActions.updateDateRangePicker} start={this.state.campaign.start} end={this.state.campaign.end} fromComponent='Explorer'/>
        </ExpandableSection>

        <a role='button' onClick={this.submitQuery} className={this.state.couldLoad ? 'button success' : 'button success disabled'} style={{marginTop: '21px'}}>
          <i className='fa fa-fw fa-refresh'/>&emsp;Load Data
        </a>
      </form>
    )
  }
})

export default DataFilters
