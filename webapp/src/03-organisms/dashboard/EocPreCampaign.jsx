import _ from 'lodash'
import React from 'react'
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
    const data = this.props.data
    const loading = this.props.loading
    let tableChart = ''

    if (data.tableData && data.tableData.options) {
      console.log('tableData: ', data.tableData)
      tableChart = <Chart type='TableChart' data={data.tableData.data} options={data.tableData.options} loading={loading} />
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
          color: ['#FF0000', '#79909F', '#04B404'],
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
