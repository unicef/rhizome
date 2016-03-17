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
    const charts = this.props.dashboard.charts || []
    const chart = charts.filter(chart => chart.type === type)
    return chart[0]
  },

  getChartFormat (indicator) {
    let d3Format = d3.format('')
    if (indicator.data_format === 'pct') {
      d3Format =  d3.format(',.1%')
    }
    return d3Format
  },
  getColorScale (indicator) {
    let colorScale = ['#FF9489', '#FFED89', '#83F5A2']
    if (indicator.data_format === 'bool') {
      colorScale = ['#FF9489', '#83F5A2']
    }
    return colorScale
  },
  reverseBounds: function(bounds){
    bounds.reversed = false
    if (bounds.bad_bound > bounds.good_bound){
      var temp = bounds.bad_bound
      bounds.bad_bound = bounds.good_bound
      bounds.good_bound = temp
      bounds.reversed = true
    }
    return bounds
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
        default_sort_order={data.tableData.options.default_sort_order}
        parentLocationMap={data.tableData.options.parentLocationMap}
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

    //for legend text
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
              color: this.getColorScale(mapIndicator),
              aspect: 3.5,
              ticks: this.reverseBounds({bad_bound: mapIndicator.bad_bound, good_bound: mapIndicator.good_bound}),
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
            <h1 id='dashboard-title'>{this.props.dashboard.title}</h1>
          </div>
        </div>
        <div className='row'>
          <div className='medium-8 columns' style={{'marginBottom': '-10px'}}>
            {tableChart}
          </div>
        </div>
        <div className='row'>
          <div className='medium-5 columns cd-chart-size'>
            <h3 className='chart_header_text'>{trendIndicator.short_name}</h3>
            {trendChart}
          </div>
          <div className='medium-3 columns cd-chart-size'>
            <h3 className='chart_header_text'>{mapIndicator.short_name}</h3>
            {mapChart}
          </div>
        </div>
      </div>
    )
  }
})

export default EocPreCampaign
