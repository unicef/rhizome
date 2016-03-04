import _ from 'lodash'
import React from 'react'
import Chart from '02-molecules/Chart.jsx'
import DashboardActions from 'actions/DashboardActions'
import d3 from 'd3'

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
    const colorScale = ['#F9152F', '#FDFD5B', '#27E833']

    let tableChart = ''

    if (this.props.data.tableData) {
      const tableIndicators = this.props.data.tableData.options.indicatorsSelected
      const tableIndicatorNames = tableIndicators.map(indicator => { return indicator.short_name })
      // const tableLocationNames = this.props.data.tableData.data.map(d => (d.name))
      const chart_options = {
        color: colorScale,
        cellFontSize: 14,
        cellSize: 36,
        onRowClick: d => { DashboardActions.navigate({ location: d }) },
        headers: tableIndicators,
        xDomain: tableIndicatorNames,
        defaultSortOrder: this.props.data.tableData.options.defaultSortOrder,
        margin: {bottom: 40, left: 40, right: 40, top: 40}
      }

      tableChart = (
          <Chart type='TableChart'
            data={this.props.data.tableData.data}
            options={chart_options}
            loading={loading} />
      )
    }

    const trendChart = <Chart type='LineChart' data={data.trendData} loading={loading} />

    const hardCodedMapData = this.props.dashboard.charts.filter(chart => chart.type === 'ChoroplethMap')
    const mapIndicatorId = hardCodedMapData[0].indicators[0]
    const mapChart = (
      <Chart type='ChoroplethMap'
        data={data.mapData}
        loading={loading}
        options={{
          aspect: 0.6,
          domain: _.constant([0, 0.1]),
          value: _.property(`properties[${mapIndicatorId}]`),
          color: colorScale,
          xFormat: d3.format(',.1%'),
          onClick: d => { DashboardActions.navigate({ location: d }) }
        }}/>
    )

    const mapLegend = (
      <Chart type='ChoroplethMapLegend'
        data={data.mapData}
        loading={loading}
        options={{
          aspect: 3.5,
          xFormat: d3.format(',.1%'),
          domain: _.constant([0, 0.1]),
          value: _.property(`properties[${mapIndicatorId}]`),
          margin: {
            top: 5,
            bottom: 0,
            left: 1,
            right: 0
          }
        }}
      />
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
                {mapLegend}
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
