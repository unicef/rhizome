import _ from 'lodash'
import React from 'react'
import Chart from 'components/molecules/Chart'
import TableChart from 'components/organisms/charts/TableChart'
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

  getChartDefFromDashboard (type) {
    const chart = this.props.dashboard.charts.filter(chart => chart.type === type)
    return chart[0]
  },

  getChartFormat (indicator) {
    if (indicator.data_format === 'pct') {
      return d3.format(',.1%')
    } else if (indicator.data_format === 'bool') {
      return d3.format('')
    } else {
      return d3.format('')
    }
  },
  getColorScale (indicator) {
    let colorScale = ['#FF9489', '#FFED89', '#83F5A2']
    if (indicator.data_format === 'bool') {
      colorScale = ['#FF9489', '#83F5A2']
    }
    return colorScale
  },

  render () {
    const data = this.props.data
    const loading = this.props.loading
    const indicatorIndex = _.indexBy(this.props.indicators, 'id')

    // TABLE CHART
    // ----------------------------------------------------------------------------------------------
    const tableIndicators = this.getChartDefFromDashboard('TableChart').indicators.map(id => indicatorIndex[id])
    const tableChart = (
      <TableChart
        data={data.tableData.data}
        indicators={tableIndicators}
        defaultSortOrder={data.tableData.options.defaultSortOrder}
        onRowClick={ d => DashboardActions.navigate({ location: d }) }
      />
    )

    // LINE CHART
    // ----------------------------------------------------------------------------------------------
    const trendIndicator = indicatorIndex[this.getChartDefFromDashboard('LineChart').indicators[0]]
    const trendChart = data.trendData
      ? <Chart type='LineChart'
          data={data.trendData}
          loading={loading}
          options={{
            color: ['#000000'],
            height: '350',
            yFormat: this.getChartFormat(trendIndicator)
          }}
        />
      : ''

    // CHOROPLETH MAP
    // ----------------------------------------------------------------------------------------------
    const mapIndicator = indicatorIndex[this.getChartDefFromDashboard('ChoroplethMap').indicators[0]]
    const indicatorTicks = [0]

    const mapChart = data.mapData
      ? <div>
          <Chart type='ChoroplethMap'
            data={data.mapData}
            loading={loading}
            options={{
              aspect: 0.6,
              data_format: mapIndicator.data_format,
              domain: _.constant([mapIndicator.bad_bound, mapIndicator.good_bound]),
              value: _.property(`properties[${mapIndicator.id}]`),
              color: this.getColorScale(mapIndicator),
              xFormat: this.getChartFormat(mapIndicator),
              onClick: d => DashboardActions.navigate({ location: d })
            }}
          />
          <Chart type='ChoroplethMapLegend'
            data={data.mapData}
            loading={loading}
            options={{
              data_format: mapIndicator.data_format,
              extents: [0.1, 0.5],
              tickLabels: ['0 - 1%', '1 - 5%', '5% +'],
              // extents: [mapIndicator.bad_bound, mapIndicator.good_bound]
              color: this.getColorScale(mapIndicator),
              aspect: 3.5,
              yFormat: this.getChartFormat(mapIndicator),
              domain: _.constant([mapIndicator.bad_bound, mapIndicator.good_bound]),
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
          <div className='medium-5 columns cd-chart-size'>
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
