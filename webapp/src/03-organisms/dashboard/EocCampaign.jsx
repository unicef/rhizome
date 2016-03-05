import _ from 'lodash'
import React from 'react'
import Chart from '02-molecules/Chart.jsx'
import DashboardActions from 'actions/DashboardActions'
import d3 from 'd3'

var EocPreCampaign = React.createClass({

  propTypes: {
    dashboard: React.PropTypes.object.isRequired,
    indicators: React.PropTypes.array.isRequired,
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

  getHardCodedChartByType (type) {
    const chart = this.props.dashboard.charts.filter(chart => chart.type === type)
    return chart[0]
  },

  render () {
    const data = this.props.data
    const loading = this.props.loading
    const colorScale = ['#FF9489', '#FFED89', '#83F5A2']
    const indicatorIndex = _.indexBy(this.props.indicators, 'id')

    // TABLE CHART
    // ----------------------------------------------------------------------------------------------
    const tableIndicators = this.getHardCodedChartByType('TableChart').indicators.map(id => indicatorIndex[id])
    const tableChart = data.tableData
      ? <Chart type='TableChart'
          data={data.tableData.data}
          loading={loading}
          options={{
            color: colorScale,
            cellFontSize: 14,
            cellSize: 40,
            onRowClick: d => { DashboardActions.navigate({ location: d }) },
            headers: tableIndicators,
            xDomain: _.map(tableIndicators, 'short_name'),
            defaultSortOrder: data.tableData.options.defaultSortOrder,
            margin: {bottom: 40, left: 40, right: 40, top: 40}
          }}
        />
      : ''

    // LINE CHART
    // ----------------------------------------------------------------------------------------------
    const trendIndicator = indicatorIndex[this.getHardCodedChartByType('LineChart').indicators[0]]
    const trendChart = data.trendData
      ? <Chart type='LineChart'
          data={data.trendData}
          loading={loading}
          options={{
            color: ['#000000'],
            height: '300',
            yFormat: d3.format(',.1%')
          }}
        />
      : ''

    // CHOROPLETH MAP
    // ----------------------------------------------------------------------------------------------
    const mapIndicator = indicatorIndex[this.getHardCodedChartByType('ChoroplethMap').indicators[0]]
    const mapChart = data.mapData
      ? <div>
          <Chart type='ChoroplethMap'
            data={data.mapData}
            loading={loading}
            options={{
              aspect: 0.6,
              domain: _.constant([0, 0.1]),
              value: _.property(`properties[${mapIndicator.id}]`),
              color: colorScale,
              xFormat: d3.format(',.1%'),
              onClick: d => { DashboardActions.navigate({ location: d }) }
            }}
          />
          <Chart type='ChoroplethMapLegend'
            data={data.mapData}
            loading={loading}
            options={{
              color: colorScale,
              aspect: 3.5,
              yFormat: d3.format(',.1%'),
              domain: _.constant([0, 0.1]),
              value: _.property(`properties[${mapIndicator.id}]`),
              margin: {
                top: 5,
                bottom: 0,
                left: 20,
                right: 0
              }
            }}
          />
        </div>
      : ''

    // LAYOUT
    // ----------------------------------------------------------------------------------------------
    return (
      <div id='management-dashboard'>
        <div className='row'>
          <div className='medium-12 columns'>
            <h1>{this.props.dashboard.title}</h1>
          </div>
        </div>
        <div className='row'>
          <div className='medium-8 columns' style={{'marginBottom': '-10px'}}>
            {tableChart}
          </div>
        </div>
        <div className='row'>
          <div className='medium-5 columns cd-chart-size' id='mapChart'>
            <h3>{trendIndicator.short_name}</h3>
            {trendChart}
          </div>
          <div className='medium-3 columns cd-chart-size'>
            <h3>{mapIndicator.short_name}</h3>
            {mapChart}
          </div>
        </div>
      </div>
    )
  }
})

export default EocPreCampaign
