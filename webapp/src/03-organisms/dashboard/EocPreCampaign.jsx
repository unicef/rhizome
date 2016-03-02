import _ from 'lodash'
import React from 'react'
// import moment from 'moment'
import Chart from '02-molecules/Chart.jsx'
import DashboardActions from 'actions/DashboardActions'

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
    const chart_options = null

    console.log(chart_options)

    const data = this.props.data
    const loading = this.props.loading
    const tableChart = <Chart type='TableChart' data={data.tableData} loading={loading} />
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
            {trendChart}
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
