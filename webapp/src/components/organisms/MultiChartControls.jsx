import _ from 'lodash'
import moment from 'moment'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'
import {DropdownList} from 'react-widgets'
import RadioGroup from 'react-radio-group'

import builderDefinitions from 'components/molecules/charts/utils/builderDefinitions'
import IconButton from 'components/atoms/IconButton'
import ColorSwatch from 'components/atoms/ColorSwatch'
import palettes from 'utilities/palettes'
import CampaignSelector from 'components/molecules/CampaignSelector'
import IndicatorSelector from 'components/molecules/IndicatorSelector'
import LocationSelector from 'components/molecules/LocationSelector'
import DateRangePicker from 'components/molecules/DateRangePicker'
import DistrictDropdown from 'components/molecules/menus/DistrictDropdown'

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
    const type = chart.type
    const start_date = chart ? moment(chart.start_date, 'YYYY-MM-DD').toDate() : moment()
    const end_date = chart ? moment(chart.end_date, 'YYYY-MM-DD').toDate() : moment()
    const chartShowsOneCampaign = _.indexOf(builderDefinitions.single_campaign_charts, type) !== -1

    const palette_selector = type !== 'RawData' ? (
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

    const date_range_picker = !chartShowsOneCampaign ? (
      <div className='medium-12 columns'>
        <h3>Date Range</h3>
        <DateRangePicker
          sendValue={props.setDateRange}
          start={start_date}
          end={end_date}
          fromComponent='MultiChartControls'
        />
        <br/>
        <br/>
      </div>
    ) : null

    const indicator_filter = (
      <div className='medium-12 columns'>
        <h3>LPD Status</h3>
        <DistrictDropdown selected={chart.indicator_filter} sendValue={props.setIndicatorFilter}/>
      </div>
    )

    const groupedChart = type === 'LineChart' || type === 'ColumnChart' || type === 'StackedColumnChart' || type === 'StackedPercentColumnChart'
    
    const group_by_selector = groupedChart ? (
      <div className='medium-12 columns radio-group'>
        <RadioGroup name={'groupBy' + chart.uuid} selectedValue={chart.groupBy} onChange={props.setGroupBy}>
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

    const campaign_selector = chartShowsOneCampaign ? (
      <CampaignSelector
        campaigns={this.state.campaigns}
        selected_campaigns={chart.selected_campaigns}
        selectCampaign={props.selectCampaign}
        deselectCampaign={props.deselectCampaign}
        setCampaigns={props.setCampaigns}
        linkCampaigns={props.linkCampaigns}
        classes='medium-12 columns'
        linked={chart.linkedCampaigns}
      />
    ) : ''

    const multiIndicator = type === 'TableChart' || type === 'RawData'
    const multiLocation = type === 'TableChart' || type === 'RawData'
    const groupByIndicator = groupedChart && chart.groupBy === 'location'
    const groupByLocation = groupedChart && chart.groupBy === 'indicator'

    const location_selector = (
      <LocationSelector
        locations={this.state.locations}
        selected_locations={chart.selected_locations}
        selectLocation={props.selectLocation}
        deselectLocation={props.deselectLocation}
        setLocations={props.setLocations}
        clearSelectedLocations={props.clearSelectedLocations}
        classes={multiLocation && !groupByIndicator ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multiLocation || groupByIndicator}
        hideLastLevel={chart.type === 'MapChart'}
      />
    )

    const indicator_selector = (
      <IndicatorSelector
        indicators={this.state.indicators}
        selected_indicators={chart.selected_indicators}
        selectIndicator={props.selectIndicator}
        setIndicators={props.setIndicators}
        deselectIndicator={props.deselectIndicator}
        clearSelectedIndicators={props.clearSelectedIndicators}
        reorderIndicator={props.reorderIndicator}
        classes={multiIndicator && !groupByLocation ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multiIndicator || groupByLocation}
        avoidBooleans={chart.type === 'LineChart'}
        filterByFormat={chart.type !== 'TableChart' && chart.type !== 'RawData'}
      />
    )

    return (
      <div className={this.props.className}>
        <IconButton onClick={props.toggleEditMode} icon='fa-angle-double-right' className='chart-options-button' />
        { date_range_picker }
        { campaign_selector }
        { indicator_filter }
        { group_by_selector }
        { location_selector }
        { indicator_selector }
        { !this.props.readOnlyMode ? palette_selector : null }
      </div>
    )
  }
})

export default MultiChartControls
