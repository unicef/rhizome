import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
// import moment from 'moment'
import StateMixin from'reflux-state-mixin'
import Chart from '02-molecules/Chart.jsx'
import DashboardActions from 'actions/DashboardActions'
import api from 'data/api'
import ChartFactory from '02-molecules/charts_d3/ChartFactory'

var EocPreCampaign = React.createClass({

  propTypes: {
    dashboard: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.object.isRequired,
    campaign: React.PropTypes.object,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool,
    location: React.PropTypes.object
  },

  getDefaultProps () {
    return {
      data: [],
      loading: true
    }
  },

  render () {
    const data = this.props.data
    const loading = this.props.loading

    let tableChart = ''

    if (this.props.data.tableData) {
      const tableIndicators = this.props.data.tableData.options.indicatorsSelected
      const tableIndicatorNames = tableIndicators.map(indicator => { return indicator.short_name })
      const tableLocationNames = this.props.data.tableData.data.map(d => (d.name))
      const chart_options = {
        color: ['#EA2D19', '#EACE19', '#13B13D'],
        cellFontSize: 14,
        cellSize: 36,
        onRowClick: d => { DashboardActions.navigate({ location: d }) },
        headers: tableIndicators,
        xDomain: tableIndicatorNames,
        defaultSortOrder: tableLocationNames,
        margin: {bottom: 40, left: 40, right: 40, top: 40},
      }

      tableChart = <Chart type='TableChart' data={this.props.data.tableData.data} options={chart_options} loading={loading} />
    }

    const trendChart = <Chart type='LineChart' data={data.trendData} loading={loading} />

    const mapChart = (
      <Chart type='ChoroplethMap'
        data={data.mapData}
        loading={loading}
        options={{
        aspect: 0.6,
        domain: _.constant([0, 0.1]),
        value: _.property('properties[21]'),
        //  bubbleValue: _.property('properties[177]'),
        //  stripeValue: _.property('properties[203]'),
        //  xFormat: d3.format(',.1%'),
        onClick: d => { DashboardActions.navigate({ location: d }) }
      }}/>
    )

    return (
      <div id='eoc-dashboard-dashboard'>
        <div className='row'>
          <div className='medium-8 columns end cd-chart-size'>
            <h2>Table Chart</h2>
            {tableChart}
          </div>
          <div className='medium-4 columns end'>
            <div className='row'>
              <div className='medium-12 columns end cd-chart-size'>
                <h2>Map Chart</h2>
                {mapChart}
              </div>
            </div>
            <div className='row'>
              <div className='medium-12 columns end cd-chart-size'>
                <h2>Trend Chart</h2>
                {trendChart}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
})

export default EocPreCampaign
