import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import StateMixin from'reflux-state-mixin'

import Chart from '02-molecules/Chart'
import DropdownMenu from '02-molecules/menus/DropdownMenu'
import ExportPdf from '02-molecules/ExportPdf'
import ChartFactory from '02-molecules/charts_d3/ChartFactory'
import ChartInfo from '02-molecules/charts_d3/ChartInfo'


import ChartStore from 'stores/ChartStore'
import RootStore from 'stores/RootStore'

import ChartActions from 'actions/ChartActions'
import IndicatorActions from 'actions/IndicatorActions'
import CampaignActions from 'actions/CampaignActions'
import LocationActions from 'actions/LocationActions'
import OfficeActions from 'actions/OfficeActions'

import ChartAPI from 'data/requests/ChartAPI'
import CampaignAPI from 'data/requests/CampaignAPI'

var ChartPage = React.createClass({

  mixins: [
    StateMixin.connect(RootStore),
    StateMixin.connect(ChartStore)
  ],

  propTypes: {
    chart_id: React.PropTypes.number
  },

  componentWillMount () {
    ChartActions.fetchChart(this.props.chart_id)
  },

  getSelectedLocations (location_ids) {
    const locationIndex = this.state.locationIndex
    if (location_ids && locationIndex.length) {
      if (Array.isArray(location_ids)) {
        return location_ids.map(id => locationIndex[id])
      } else {
        return [locationIndex[location_ids]]
      }
    }
  },

  getSelectedIndicators (indicator_ids) {
    const indicatorIndex = this.state.indicatorIndex
    if (indicator_ids && indicatorIndex.length) {
      if (Array.isArray(indicator_ids)) {
        return indicator_ids.map(id => indicatorIndex[id])
      } else {
        return [indicatorIndex[indicator_ids]]
      }
    }
  },

  render () {
    let chart_title = 'Test Title'

    if (this.state.datapoints && this.state.chartDef) {
      const chartDef = this.state.chartDef
      const selectedLocations = this.getSelectedLocations(chartDef.location_ids)
      const selectedIndicators = this.getSelectedIndicators(chartDef.indicator_ids)
      const chart = ChartInfo.getChartInfo(chartDef, this.state.datapoints, selectedLocations, selectedIndicators)
      chart_title = chart.title
      return (
        <div className='row layout-basic'>
          <div className='medium-12 columns text-center'>
            <h1>{ chart_title }</h1>
          </div>
          <div className='medium-2 columns'>
            <a href={'/charts/' + this.props.chart_id + '/edit'} className='button expand small'>
              <i className='fa fa-pencil'></i> Edit Chart
            </a>
            <ExportPdf className='button expand small' />
          </div>
          <div className='medium-10 columns'>
            <Chart type={chartDef.type} data={chart.data} options={chart.options} loading={true}/>
          </div>
        </div>
      )
    }

    return (
      <div className='row layout-basic'>
        <div className='medium-12 columns text-center'>
          <h1>{ chart_title }</h1>
        </div>
        <div className='medium-2 columns'>
          <a href={'/charts/' + this.props.chart_id + '/edit'} className='button expand small'>
            <i className='fa fa-pencil'></i> Edit Chart
          </a>
          <ExportPdf className='button expand small' />
        </div>
        <div className='medium-10 columns'>
        </div>
      </div>
    )
  }
})

export default ChartPage
