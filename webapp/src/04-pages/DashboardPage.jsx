import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import StateMixin from 'reflux-state-mixin'

import Chart from '02-molecules/Chart'
import ExportPdf from '02-molecules/ExportPdf'
import DropdownMenu from '02-molecules/menus/DropdownMenu'

import IndicatorActions from 'actions/IndicatorActions'
import CampaignActions from 'actions/CampaignActions'
import LocationActions from 'actions/LocationActions'
import OfficeActions from 'actions/OfficeActions'
import ChartActions from 'actions/ChartActions'

import RootStore from 'stores/RootStore'
import DashboardPageStore from 'stores/DashboardPageStore'

var DashboardPage = React.createClass({

  mixins: [
    StateMixin.connect(RootStore),
    StateMixin.connect(DashboardPageStore)
  ],

   propTypes: {
    campaign: React.PropTypes.object,
    charts_ids: React.PropTypes.array
  },

  getDefaultProps () {
    return {
      chart_ids: [5, 3],
    }
  },

  componentDidMount () {
    ChartActions.fetchCharts()
    CampaignActions.fetchCampaigns()
    IndicatorActions.fetchIndicators()
    LocationActions.fetchLocations()
    OfficeActions.fetchOffices()
  },

  dataIsReady () {
    return this.state.chartIndex.length > 0
      &&  this.state.campaignIndex.length > 0
      &&  this.state.locationIndex.length > 0
      &&  this.state.indicatorIndex.length > 0
      &&  this.state.officeIndex.length > 0
  },

  render () {
    if (this.dataIsReady()) {
      console.log('COMPONENT - state.chartIndex', this.state.chartIndex)
      const dashboard_charts = this.props.chart_ids.map( id => {
        return (
          <Chart
            id='custom-chart'
            type={this.state.chart.type}
            data={this.state.chartIndex[id]}
            options={this.state.data.options}
            campaigns={this.state.campaigns}
            defaultCampaign={this.state.campaigns[0]} />
        )

        this.state.chartIndex[id]
      })
      console.log('dashboard_charts', dashboard_charts)
      return (
        <div className='row layout-basic'>
          <h1>we need a chart</h1>
        </div>
      )
    } else {
      return  (
        <div className='loading'>
          <i className='fa fa-spinner fa-spin fa-5x'></i>
          <div>Loading</div>
        </div>
      )
    }
  }
})

export default DashboardPage
