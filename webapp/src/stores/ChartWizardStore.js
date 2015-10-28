import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'

import ChartWizardActions from 'actions/ChartWizardActions'
import api from 'data/api'
import processChartData from 'stores/chartBuilder/processChartData'
import chartDefinitions from 'stores/chartBuilder/chartDefinitions'
import treeify from 'data/transform/treeify'
import ancestryString from 'data/transform/ancestryString'

let ChartWizardStore = Reflux.createStore({
  listenables: ChartWizardActions,
  data: {
    indicatorList: [],
    indicatorSelected: [],
    locationList: [],
    locationSelected: null,
    campaignFilteredList: [],
    groupByValue: 0,
    canDisplayChart: false,
    chartDef: {}
  },

  filterCampaignByLocation(campaigns, location) {
    return campaigns.filter(campaign => {
      return campaign.office.name == location.name
    })
  },

  applyChartDef(chartDef) {
    let timeValue = !chartDef.timeRange ? 'all' :
      chartDef.timeRange.years ? '1year' :
      chartDef.timeRange.months ? +chartDef.timeRange.months + 1 + 'month' : 'all'
    this.data.timeValue = Math.max(_.findIndex(chartDefinitions.times, {value: timeValue}), 0);
  },

  getInitialState() {
    return this.data
  },

  onInitialize(chartDef, location, campaign) {
    this.data.chartDef = _.clone(chartDef)
    this.data.location = location
    this.data.campaign = campaign
    this.data.groupByValue = _.findIndex(chartDefinitions.groups, {value: this.data.chartDef.groupBy})

    Promise.all([api.indicatorsTree(), api.locations(), api.campaign(), api.office()]).
      then(([indicators, locations, campaigns, offices]) => {
        this.indicatorIndex = _.indexBy(indicators.flat, 'id')
        this.data.indicatorList = _.sortBy(indicators.objects, 'title')
        this.data.indicatorSelected = chartDef.indicators.map(id => {
          return this.indicatorIndex[id]
        })

        this.locationIndex = _.indexBy(locations.objects, 'id')
        this.data.locationList = _(locations.objects)
          .map(location => {
            return {
              'title'  : location.name,
              'value'  : location.id,
              'parent' : location.parent_location_id
            }
          })
          .sortBy('title')
          .reverse()
          .thru(_.curryRight(treeify)('value'))
          .map(ancestryString)
          .value()

        let officeIndex = _.indexBy(offices.objects, 'id')
        this.campaignList = _(campaigns.objects)
          .map(campaign => {
            return _.assign({}, campaign, {
              'start_date' : moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
              'end_date'   : moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
              'office'     : officeIndex[campaign.office_id]
            });
          })
          .sortBy(_.method('start_date.getTime'))
          .reverse()
          .value()
        this.data.campaignFilteredList = this.filterCampaignByLocation(this.campaignList, this.data.location)
        this.campaignIndex = _.indexBy(this.campaignList, 'id')

        this.applyChartDef(chartDef)

        this.previewChart()
    })
  },

  onEditTitle(value) {
    this.data.chartDef.title = value
    this.trigger(this.data)
  },

  onAddLocation(index) {
    this.data.location = this.locationIndex[index]
    this.data.campaignFilteredList = this.filterCampaignByLocation(this.campaignList, this.data.location)
    this.previewChart()
  },

  onAddIndicator(index) {
    this.data.indicatorSelected.push(this.indicatorIndex[index])
    this.previewChart()
  },

  onRemoveIndicator(id) {
    _.remove(this.data.indicatorSelected, {id: id})
    this.previewChart()
  },

  onAddCampaign(index) {
    this.data.campaign = this.campaignIndex[index]
    this.previewChart()
  },

  onChangeChart(value) {
    this.data.chartDef.type = value
    this.data.chartData = []
    this.previewChart()
  },

  onChangeGroupRadio(value) {
    this.data.groupByValue = value
    this.previewChart()
  },

  onChangeTimeRadio(value) {
    this.data.timeValue = value
    this.previewChart()
  },

  onSaveChart(callback) {
    callback(_.merge(this.data.chartDef, {
      indicators: this.data.indicatorSelected.map(item => {
        return item.id
      }),
      groupBy: chartDefinitions.groups[this.data.groupByValue].value,
      timeRange: chartDefinitions.times[this.data.timeValue].json
    }, (a, b) => {
      return b
    }))
  },

  previewChart() {
    if (!this.data.indicatorSelected.length) {
      this.data.canDisplayChart = false
      this.trigger(this.data)
      return
    }
    let chartType = this.data.chartDef.type
    let groupBy = chartDefinitions.groups[this.data.groupByValue].value
    let indicatorIndex = _.indexBy(this.data.indicatorSelected, 'id')
    let locationIndex = _.indexBy([this.data.location], 'id')
    let groups = this.data.groupByValue == 0 ? indicatorIndex : locationIndex
    let start = moment(this.data.campaign.start_date)
    let lower = chartDefinitions.times[this.data.timeValue].getLower(start)
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
      this.data.chartDef.indicatorsSelected,
      [this.data.location],
      lower,
      upper,
      groups,
      groupBy,
      this.data.chartDef.x,
      this.data.chartDef.y)
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
