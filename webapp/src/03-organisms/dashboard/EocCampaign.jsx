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
    const colorScale = ['#FF9489', '#FFED89', '#83F5A2']

    // TABLE CHART
    // ----------------------------------------------------------------------------------------------
    let tableChart = ''
    if (data.tableData) {
      const tableIndicators = data.tableData.options.indicatorsSelected
      const tableIndicatorNames = tableIndicators.map(indicator => { return indicator.short_name })
      tableChart = (
          <Chart type='TableChart'
            data={data.tableData.data}
            options={{
              color: colorScale,
              cellFontSize: 14,
              cellSize: 36,
              onRowClick: d => { DashboardActions.navigate({ location: d }) },
              headers: tableIndicators,
              xDomain: tableIndicatorNames,
              defaultSortOrder: data.tableData.options.defaultSortOrder,
              margin: {bottom: 40, left: 40, right: 40, top: 40}
            }}
            loading={loading} />
      )
    }

    // LINE CHART
    // ----------------------------------------------------------------------------------------------
    const hardCodedTrendData = this.props.dashboard.charts.filter(chart => chart.type === 'LineChart')
    const trendIndicatorId = hardCodedTrendData[0].indicators[0]
    const trendIndicator = this.props.indicators.filter(indicator => { return indicator.id === trendIndicatorId })
    const trendChart = (
        <Chart type='LineChart'
          data={data.trendData}
          loading={loading}
          options={{
            color: ['#000000'],
            height: '300',
            hasDots: true
          }}
        />
    )

    // CHOROPLETH MAP
    // ----------------------------------------------------------------------------------------------
    const hardCodedMapData = this.props.dashboard.charts.filter(chart => chart.type === 'ChoroplethMap')
    const mapIndicatorId = hardCodedMapData[0].indicators[0]
    const mapIndicator = this.props.indicators.filter(indicator => { return indicator.id === mapIndicatorId })
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
          color: colorScale,
          aspect: 3.5,
          yFormat: d3.format(',.1%'),
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
      <div id='management-dashboard'>
        <div className='row'>
          <div className='medium-12 columns'>
            <h1>{this.props.dashboard.title}</h1>
          </div>
        </div>
        <div className='row'>
          <div className='medium-8 columns' style={{'margin-bottom': -10 + 'px !important'}}>
            {tableChart}
          </div>
        </div>
        <div className='row'>
          <div className='medium-5 columns cd-chart-size' id='mapChart'>
            <h3>{trendIndicator[0].short_name}</h3>
            {trendChart}
          </div>
          <div className='medium-3 columns cd-chart-size'>
            <h3>{mapIndicator[0].short_name}</h3>
            {mapChart}
            {mapLegend}
          </div>
        </div>
      </div>
    )
  }
})

export default EocPreCampaign
