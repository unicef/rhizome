import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'

import ChartWizardActions from 'actions/ChartWizardActions'
import api from 'data/api'
import processChartData from 'stores/chartBuilder/processChartData'
import chartDefinitions from 'stores/chartBuilder/chartDefinitions'

let ChartWizardStore = Reflux.createStore({
  listenables: ChartWizardActions,
  data: {
    title: '',
    indicatorList: [],
    indicatorSelected: [],
    chartType: '',
    canDisplayChart: false
  },

  getInitialState() {
    return this.data
  },

  onInitialize(chartDef, location, campaign) {
    this.data.title = chartDef.title
    this.data.chartType = chartDef.type
    this.data.groupBy = chartDef.groupBy
    this.data.x = chartDef.x
    this.data.y = chartDef.y
    this.data.location = location
    this.data.campaign = campaign

    api.indicatorsTree().then(data => {
      this.indicatorIndex = _.indexBy(data.flat, 'id');
      this.data.indicatorList = _.sortBy(data.objects, 'title')
      this.data.indicatorSelected = chartDef.indicators.map(id => {
        return this.indicatorIndex[id]
      })
      this.onPreviewChart()
    })
  },

  onEditTitle(value) {
    this.data.title = value
    this.trigger(this.data)
  },

  onAddIndicator(index) {
    this.data.indicatorSelected.push(this.indicatorIndex[index])
    this.onPreviewChart()
  },

  onRemoveIndicator(id) {
    _.remove(this.data.indicatorSelected, {id: id})
    this.onPreviewChart()
  },

  onChangeChart(value) {
    this.data.chartType = value
    this.data.chartData = []
    this.onPreviewChart()
  },

  onPreviewChart() {
    if (!this.data.indicatorSelected.length) {
      this.data.canDisplayChart = false
      this.trigger(this.data)
      return
    }
    let chartType = this.data.chartType
    let groupBy = this.data.groupBy
    let indicatorIndex = _.indexBy(this.data.indicatorSelected, 'id')
    let groups = indicatorIndex // need work
    let start = moment(this.data.campaign.start_date)
    let lower = null // all time
    let upper = start.clone().startOf('month')
    let indicatorArray = _.map(this.data.indicatorSelected, _.property('id'))
    let query = {
      indicator__in: indicatorArray,
      location__in: _.map([this.data.location], _.property('id')),
      campaign_start: (lower ? lower.format('YYYY-MM-DD') : null),
      campaign_end: upper.format('YYYY-MM-DD')
    }

    processChartData.init(api.datapoints(query),
      chartType,
      this.data.indicatorsSelected,
      [this.data.location],
      lower,
      upper,
      groups,
      groupBy,
      this.data.x,
      this.data.y)
    .then(chart => {
      if (!chart.options || !chart.data) {
        this.data.canDisplayChart = false
      } else {
        this.data.canDisplayChart = true
        this.data.chartOptions = chart.options
        this.data.chartData = chart.data
      }
      this.trigger(this.data)
    });
  }
})

export default ChartWizardStore
