import _ from 'lodash'
import moment from 'moment'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import RadioGroup from 'components/form/RadioGroup'

import builderDefinitions from 'components/d3chart/utils/builderDefinitions'
import IconButton from 'components/button/IconButton'
import CampaignMultiSelect from 'components/multi_select/CampaignMultiSelect'
import IndicatorMultiSelect from 'components/multi_select/IndicatorMultiSelect'
import LocationMultiSelect from 'components/multi_select/LocationMultiSelect'
import DateMultiSelect from 'components/select/DateRangeSelect'
import DistrictSelect from 'components/select/DistrictSelect'

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
    const groupedChart = _.indexOf(builderDefinitions.grouped_charts, type) !== -1
    const multiIndicator = type === 'TableChart' || type === 'RawData'
    const multiLocation = type === 'TableChart'
    const groupByIndicator = groupedChart && chart.groupBy === 'location'
    const groupByLocation = groupedChart && chart.groupBy === 'indicator'

    const date_range_picker = !chartShowsOneCampaign && chart.groupByTime !== 'year' ? (
      <div className='medium-12 columns'>
        <h3>Date Range</h3>
        <DateMultiSelect
          sendValue={props.setDateRange}
          start={start_date}
          end={end_date}
          fromComponent='MultiChartControls'
        />
        <br/>
        <br/>
      </div>
    ) : null

    const group_by_time_selector = !chartShowsOneCampaign ? (
      <div className='medium-12 columns radio-group'>
        <h3>Group By</h3>
        <RadioGroup
          name={'groupByTime' + chart.uuid}
          value={chart.groupByTime}
          onChange={props.setGroupByTime}
          horizontal
          values={[
            {value: 'campaign', title: 'Campaign'},
            {value: 'quarter', title: 'Quarter'},
            {value: 'year', title: 'Year'}
          ]}/>
      </div>
    ) : null

    const indicator_filter = (
      <div className='medium-12 columns'>
        <h3>Filter By</h3>
        <DistrictSelect selected={chart.indicator_filter} sendValue={props.setIndicatorFilter}/>
      </div>
    )

    const group_by_selector = groupedChart ? (
      <div className='medium-12 columns radio-group'>
        <RadioGroup
          name={'groupBy' + chart.uuid}
          value={chart.groupBy}
          onChange={props.setGroupBy}
          horizontal
          values={[
            {value: 'indicator', title: 'Multiple Indicators'},
            {value: 'location', title: ' Multiple Locations'}
          ]}/>
      </div>
    ) : null

    const campaign_selector = chartShowsOneCampaign ? (
      <CampaignMultiSelect
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

    const location_selector = (
      <LocationMultiSelect
        locations={this.state.locations}
        selected_locations={chart.selected_locations}
        selectLocation={props.selectLocation}
        deselectLocation={props.deselectLocation}
        setLocations={props.setLocations}
        clearSelectedLocations={props.clearSelectedLocations}
        classes={multiLocation || groupByIndicator ? 'medium-6 columns' : 'medium-12 columns'}
        multi={multiLocation || groupByIndicator}
        hideLastLevel={chart.type === 'MapChart'}
      />
    )

    const indicator_selector = (
      <IndicatorMultiSelect
        indicators={this.state.indicators}
        selected_indicators={chart.selected_indicators}
        indicator_colors={chart.indicator_colors}
        selectIndicator={props.selectIndicator}
        setIndicators={props.setIndicators}
        setIndicatorColor={props.setIndicatorColor}
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
        { group_by_time_selector }
        { date_range_picker }
        { campaign_selector }
        { group_by_selector }
        { indicator_filter }
        { location_selector }
        { indicator_selector }
      </div>
    )
  }
})

export default MultiChartControls
