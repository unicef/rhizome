import _ from 'lodash'
import moment from 'moment'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import {DropdownList} from 'react-widgets'
import RadioGroup from 'react-radio-group'

import IconButton from 'components/atoms/IconButton'
import ColorSwatch from 'components/atoms/ColorSwatch'
import palettes from 'utilities/palettes'
import CampaignSelector from 'components/molecules/CampaignSelector'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'
import DateRangePicker from 'components/molecules/DateRangePicker'

import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'
import CampaignStore from 'stores/CampaignStore'

const MultiChartControls = React.createClass({

  mixins: [
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

  propTypes: {
    chart: PropTypes.object,
    setDateRange: PropTypes.func,
    setGroupBy: PropTypes.func,
    setPalette: PropTypes.func,
    selectCampaign: PropTypes.func,
    deselectCampaign: PropTypes.func,
    setCampaigns: PropTypes.func,
    linkCampaigns: PropTypes.func,
    selectLocation: PropTypes.func,
    deselectLocation: PropTypes.func,
    setLocations: PropTypes.func,
    clearSelectedLocations: PropTypes.func,
    selectIndicator: PropTypes.func,
    setIndicators: PropTypes.func,
    deselectIndicator: PropTypes.func,
    clearSelectedIndicators: PropTypes.func,
    reorderIndicator: PropTypes.func,
    className: PropTypes.string
  },

  render () {
    const props = this.props
    const chart = props.chart
    const start_date = chart ? moment(chart.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart ? moment(chart.end_date, 'YYYY-MM-DD').toDate() : moment()

    const palette_selector = chart.type !== 'RawData' ? (
      <div className='medium-12 columns' style={{position: 'absolute', bottom: 0}}>
        <DropdownList
          data={ _.map(palettes, (key, value) => ({colors: key, value: value}) )}
          textField='value'
          valueField='value'
          value={chart.palette}
          itemComponent={ColorSwatch}
          valueComponent={ColorSwatch}
          onChange={item => props.setPalette(item.value)}
        />
        <br />
      </div>
    ) : null

    const date_range_picker = chart.type === 'LineChart' || chart.type === 'RawData' ? (
      <div className='medium-12 columns'>
        <h3>Date Range</h3>
        <DateRangePicker
          sendValue={this.props.setDateRange}
          start={start_date}
          end={end_date}
          fromComponent='MultiChartControls'
        />
        <br/>
        <br/>
      </div>
    ) : null

    const group_by_selector = chart.type === 'LineChart' ? (
      <div className='medium-12 columns radio-group'>
        <RadioGroup name={'groupBy' + chart.uuid} selectedValue={chart.groupBy} onChange={this.props.setGroupBy}>
          {Radio => (
            <div>
              <Radio value='indicator' /> Multiple Indicators
              <span>&nbsp;&nbsp;</span>
              <Radio value='location' /> Multiple Locations
            </div>
          )}
        </RadioGroup>
      </div>
    ) : null

    const campaign_selector = chart.type !== 'LineChart' && chart.type !== 'RawData' ? (
      <CampaignSelector
        campaigns={this.state.campaigns}
        selected_campaigns={chart.selected_campaigns}
        selectCampaign={this.props.selectCampaign}
        deselectCampaign={this.props.deselectCampaign}
        setCampaigns={this.props.setCampaigns}
        linkCampaigns={this.props.linkCampaigns}
        classes='medium-12 columns'
        linked={chart.linkedCampaigns}
      />
    ) : ''

    const multiIndicator = chart.type === 'TableChart' || chart.type === 'RawData'
    const multiLocation = chart.type === 'TableChart' || chart.type === 'RawData'
    const groupByIndicator = chart.type === 'LineChart'  && chart.groupBy === 'location'
    const groupByLocation = chart.type === 'LineChart'  && chart.groupBy === 'indicator'

    const location_selector = (
      <LocationSelector
        locations={this.state.locations}
        selected_locations={chart.selected_locations}
        selectLocation={this.props.selectLocation}
        deselectLocation={this.props.deselectLocation}
        setLocations={this.props.setLocations}
        clearSelectedLocations={this.props.clearSelectedLocations}
        classes={multiLocation && !groupByIndicator ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multiLocation || groupByIndicator}
        hideLastLevel={chart.type === 'MapChart'}
      />
    )

    const indicator_selector = (
      <IndicatorSelector
        indicators={this.state.indicators}
        selected_indicators={chart.selected_indicators}
        selectIndicator={this.props.selectIndicator}
        setIndicators={this.props.setIndicators}
        deselectIndicator={this.props.deselectIndicator}
        clearSelectedIndicators={this.props.clearSelectedIndicators}
        reorderIndicator={this.props.reorderIndicator}
        classes={multiIndicator && !groupByLocation ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multiIndicator || groupByLocation}
        avoidBooleans={chart.type === 'LineChart'}
      />
    )

    return (
      <div className={this.props.className}>
        <IconButton onClick={props.toggleEditMode} icon='fa-angle-double-right' className='chart-options-button' />
        { date_range_picker }
        { campaign_selector }
        { group_by_selector }
        { location_selector }
        { indicator_selector }
        { !this.props.readOnlyMode ? palette_selector : null }
      </div>
    )
  }
})

export default MultiChartControls
