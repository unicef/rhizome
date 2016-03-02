import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
// import moment from 'moment'
import StateMixin from'reflux-state-mixin'
import Chart from '02-molecules/Chart.jsx'
import IndicatorStore from 'stores/IndicatorStore'
import IndicatorActions from 'actions/IndicatorActions'
import DashboardActions from 'actions/DashboardActions'
import api from 'data/api'
import ChartFactory from '02-molecules/charts'

var EocPreCampaign = React.createClass({

 mixins: [
    StateMixin.connect(IndicatorStore),
  ],

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

  getInitialState() {
    return {
      tableData: null
    }
  },

  componentWillMount() {
    const indicator_ids = this.props.dashboard.charts[0].indicators
    let query = {
      indicator__in: this.props.dashboard.charts[0].indicators,
      campaign_start: '2016-01-01',
      campaign_end: '2016-02-01',
      location_id__in: this.props.location_id,
      chart_type: 'TableChart'
    }

    api.datapoints(query).then(response => {
      console.log('response', response)
      this.setState({tableData: response.objects})
    })
  },

  render () {
    let tableChart = ''
    if (this.state.tableData && this.state.indicatorIndex.length > 0) {
      console.log('we got a table!')
      console.log('this.state', this.state)
      const indicator_ids = this.props.dashboard.charts[0].indicators
      const tableIndicators = indicator_ids.map(id => {
        return this.state.indicatorIndex[id]
      })
      console.log('tableIndicators', tableIndicators)
      const chart_options = {
        cellFontSize: 14,
        cellSize: 36,
        chartInDashboard: true,
        color: null,
        defaultSortOrder: [this.props.location.name],
        fontSize: 14,
        headers: tableIndicators,
        indicatorsSelected: tableIndicators,
        margin: {bottom: 40, left: 40, right: 40, top: 40},
        // parentLocationMap: Object
        xDomain: tableIndicators.map(indicator => { return indicator.short_name }),
        xFormat: ",.0f",
        yFormat: ",.0f"
      }
      tableChart = ChartFactory('TableChart', React.findDOMNode(this), this.state.tableData, chart_options)
      console.log('tableChart', tableChart)
      // tableChart = <Chart type='TableChart' data={this.state.tableData} options={chart_options} loading={loading} />
    }

    const data = this.props.data
    const loading = this.props.loading
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
