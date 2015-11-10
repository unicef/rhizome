import Reflux from 'reflux'
import _ from 'lodash'
import moment from 'moment'
import d3 from 'd3'

import ChartWizardActions from 'actions/ChartWizardActions'
import api from 'data/api'
import processChartData from 'stores/chartBuilder/processChartData'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'
import treeify from 'data/transform/treeify'
import ancestryString from 'data/transform/ancestryString'

let ChartWizardStore = Reflux.createStore({
  listenables: ChartWizardActions,
  data: {
    indicatorList: [],
    indicatorSelected: [],
    indicatorFilteredList: [],
    locationList: [],
    locationSelected: null,
    campaignFilteredList: [],
    timeRangeFilteredList: [],
    chartTypeFilteredList: [],
    groupByValue: 0,
    locationLevelValue: 0,
    timeValue: 0,
    yFormatValue: 0,
    xFormatValue: 0,
    canDisplayChart: false,
    isLoading: true,
    chartOptions: {},
    chartData: [],
    chartDef: {}
  },

  filterCampaignByLocation (campaigns, location) {
    return campaigns.filter(campaign => {
      return campaign.office_id === location.office_id
    })
  },

  filterTimeRangeByChartType (timeRanges, chartType) {
    let expectTimes = _.find(builderDefinitions.charts, { name: chartType }).timeRadios
    return timeRanges.filter(time => {
      return _.includes(expectTimes, time.value)
    })
  },

  filterChartTypeByIndicator () {
    api.chartType({ primary_indicator_id: this.data.indicatorSelected[0].id }, null, {'cache-control': 'no-cache'}).then(res => {
      let availableCharts = res.objects.map(chart => {
        return chart.name
      })
      this.data.chartTypeFilteredList = builderDefinitions.charts.filter(chart => {
        return _.includes(availableCharts, chart.name)
      })

      if (!_.includes(availableCharts, this.data.chartDef.type)) {
        this.onChangeChart(this.data.chartTypeFilteredList[0].name)
      }
    })
  },

  applyChartDef (chartDef) {
    this.data.locationLevelValue = Math.max(_.findIndex(builderDefinitions.locationLevels, { value: chartDef.locations }), 0)
    this.data.locationSelected = builderDefinitions.locationLevels[this.data.locationLevelValue].getAggregated(this.data.location, this.locationIndex)
    this.data.groupByValue = Math.max(_.findIndex(builderDefinitions.groups, { value: chartDef.groupBy }), 0)
    this.data.timeValue = Math.max(_.findIndex(this.data.timeRangeFilteredList, { json: chartDef.timeRange }), 0)
    this.data.yFormatValue = Math.max(_.findIndex(builderDefinitions.formats, { value: chartDef.yFormat }), 0)
    this.data.xFormatValue = Math.max(_.findIndex(builderDefinitions.formats, { value: chartDef.xFormat }), 0)
  },

  integrateChartOption (chartOption) {
    if (!chartOption.yFormat) {
      chartOption.yFormat = d3.format(builderDefinitions.formats[this.data.yFormatValue].value)
    }
    if (!chartOption.xFormat) {
      chartOption.xFormat = d3.format(builderDefinitions.formats[this.data.xFormatValue].value)
    }
    return chartOption
  },

  getInitialState () {
    return this.data
  },

  onInitialize (chartDef) {
    this.data.chartDef = _.clone(chartDef)

    Promise.all([api.locations(), api.campaign(), api.office()])
      .then(([locations, campaigns, offices]) => {
        this.locationIndex = _.indexBy(locations.objects, 'id')
        this.data.locationList = _(locations.objects)
          .map(location => {
            return {
              'title': location.name,
              'value': location.id,
              'parent': location.parent_location_id
            }
          })
          .sortBy('title')
          .reverse()
          .thru(_.curryRight(treeify)('value'))
          .map(ancestryString)
          .value()

        this.data.location = chartDef.locationValue && this.locationIndex[chartDef.locationValue]
          ? this.locationIndex[chartDef.locationValue]
          : this.locationIndex[this.data.locationList[0].value]

        let officeId = this.data.location.office_id

        api.indicatorsTree({ office_id: officeId }).then(indicators => {
          this.indicatorIndex = _.indexBy(indicators.flat, 'id')
          this.data.indicatorList = _.sortBy(indicators.objects, 'title')
          this.data.indicatorSelected = chartDef.indicators.map(id => {
            return this.indicatorIndex[id]
          })
          this.previewChart()
        })

        let officeIndex = _.indexBy(offices.objects, 'id')
        this.campaignList = _(campaigns.objects)
          .map(campaign => {
            return _.assign({}, campaign, {
              'start_date': moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
              'end_date': moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
              'office': officeIndex[campaign.office_id]
            })
          })
          .sortBy(_.method('start_date.getTime'))
          .reverse()
          .value()

        this.campaignIndex = _.indexBy(this.campaignList, 'id')
        this.data.campaignFilteredList = this.filterCampaignByLocation(this.campaignList, this.data.location)
        this.data.timeRangeFilteredList = this.filterTimeRangeByChartType(builderDefinitions.times, this.data.chartDef.type)
        this.data.chartTypeFilteredList = builderDefinitions.charts

        if (chartDef.campaignValue && this.campaignIndex[chartDef.campaignValue]) {
          this.data.campaign = this.campaignIndex[chartDef.campaignValue]
        } else{
          this.data.campaign = this.data.campaignFilteredList.length > 0
            ? this.campaignIndex[this.data.campaignFilteredList[0].id]
            : null
        }

        if (this.data.indicatorSelected.length > 0) {
          this.filterChartTypeByIndicator()
        }

        this.applyChartDef(chartDef)

        this.previewChart()
    })
  },

  onEditTitle (value) {
    this.data.chartDef.title = value
  },

  onAddLocation (index) {
    this.data.location = this.locationIndex[index]
    this.data.locationSelected = builderDefinitions.locationLevels[this.data.locationLevelValue].getAggregated(this.data.location, this.locationIndex)

    api.indicatorsTree({ office_id: this.data.location.office_id }).then(indicators => {
      this.indicatorIndex = _.indexBy(indicators.flat, 'id')
      this.data.indicatorList = _.sortBy(indicators.objects, 'title')
      this.data.indicatorSelected = this.data.chartDef.indicators.map(id => {
        return this.indicatorIndex[id]
      })

      this.data.campaignFilteredList = this.filterCampaignByLocation(this.campaignList, this.data.location)
      let newCampaign = this.data.campaignFilteredList.filter(campaign => {
        return moment(campaign.start_date).format() === moment(this.data.campaign.start_date).format()
      })
      this.data.campaign = newCampaign.length > 0 ? newCampaign[0] : this.data.campaignFilteredList[0]
      this.previewChart()
    })
  },

  onAddFirstIndicator(index) {
    this.data.indicatorSelected[0] = this.indicatorIndex[index]
    this.filterChartTypeByIndicator()
    this.previewChart()
  },

  onAddIndicator(index) {
    if (this.data.indicatorSelected.map(indicator => indicator.id).indexOf(index) >= 0) return
    this.data.indicatorSelected.push(this.indicatorIndex[index])
    this.previewChart()
  },

  onRemoveIndicator(id) {
    _.remove(this.data.indicatorSelected, {id: id})
    this.previewChart()
  },

  onAddCampaign (index) {
    this.data.campaign = this.campaignIndex[index]
    this.previewChart()
  },

  onChangeChart (value) {
    this.data.chartDef.type = value
    this.data.timeRangeFilteredList = this.filterTimeRangeByChartType(builderDefinitions.times, this.data.chartDef.type)
    this.data.timeValue = Math.min(this.data.timeValue, this.data.timeRangeFilteredList.length - 1)

    if (value === 'ChoroplethMap') {
      this.data.locationLevelValue = _.findIndex(builderDefinitions.locationLevels, {value: 'sublocations'})
    }

    this.data.locationSelected = builderDefinitions.locationLevels[this.data.locationLevelValue].getAggregated(this.data.location, this.locationIndex)
    this.data.chartData = []
    this.previewChart()
  },

  onChangeGroupRadio (value) {
    this.data.groupByValue = value
    this.previewChart()
  },

  onChangeLocationLevelRadio (value) {
    this.data.locationLevelValue = value
    this.data.locationSelected = builderDefinitions.locationLevels[value].getAggregated(this.data.location, this.locationIndex)
    this.previewChart()
  },

  onChangeTimeRadio (value) {
    this.data.timeValue = value
    this.previewChart()
  },

  onChangeYFormatRadio (value) {
    this.data.yFormatValue = value
    this.previewChart()
  },

  onChangeXFormatRadio (value) {
    this.data.xFormatValue = value
    this.previewChart()
  },

  onChangeXAxis (value) {
    this.data.chartDef.x = value
    this.previewChart()
  },

  onChangeYAxis (value) {
    this.data.chartDef.y = value
    this.previewChart()
  },

  onSaveChart (callback) {
    callback(
      _.merge(
        this.data.chartDef,
        {
          indicators: this.data.indicatorSelected.map(item => {
            return item.id
          }),
          groupBy: builderDefinitions.groups[this.data.groupByValue].value,
          locations: builderDefinitions.locationLevels[this.data.locationLevelValue].value,
          locationValue: this.data.location.id,
          campaignValue: this.data.campaign.id,
          timeRange: this.data.timeRangeFilteredList[this.data.timeValue].json,
          yFormat: builderDefinitions.formats[this.data.yFormatValue].value,
          xFormat: builderDefinitions.formats[this.data.xFormatValue].value
        }, (source, override) => {
          return override
        }
      )
    )
  },

  previewChart () {
    if (!this.data.indicatorSelected.length) {
      this.data.canDisplayChart = false
      this.data.isLoading = false
      this.trigger(this.data)
      return
    }

    this.data.isLoading = true
    this.trigger(this.data)

    let chartType = this.data.chartDef.type
    let groupBy = builderDefinitions.groups[this.data.groupByValue].value
    let indicatorIndex = _.indexBy(this.data.indicatorSelected, 'id')
    let locationIndex = _.indexBy(this.data.locationSelected, 'id')
    let groups = this.data.groupByValue === 0 ? indicatorIndex : locationIndex
    let start = moment(this.data.campaign.start_date)
    let lower = this.data.timeRangeFilteredList[this.data.timeValue].getLower(start)
    let upper = start.clone().startOf('month')
    let indicatorArray = _.map(this.data.indicatorSelected, _.property('id'))
    let query = {
      indicator__in: indicatorArray,
      location__in: _.map(this.data.locationSelected, _.property('id')),
      campaign_start: (lower ? lower.format('YYYY-MM-DD') : null),
      campaign_end: upper.format('YYYY-MM-DD')
    }

    processChartData.init(api.datapoints(query),
      chartType,
      this.data.indicatorSelected,
      this.data.locationSelected,
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
        this.data.chartOptions = this.integrateChartOption(chart.options)
        this.data.chartData = chart.data
      }
      this.data.isLoading = false
      this.trigger(this.data)
    })
  }
})

export default ChartWizardStore
