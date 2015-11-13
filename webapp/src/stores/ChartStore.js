import _ from 'lodash'
import moment from 'moment'

import api from 'data/api'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'
import treeify from 'data/transform/treeify'
import ancestryString from 'data/transform/ancestryString'

function prepareChartData (chartDef) {
  let data = {}

  data.chartDef = _.clone(chartDef)

  Promise.all([
    api.locations(),
    api.campaign(),
    api.office()
  ])
  .then(([locations, campaigns, offices]) => {
    let locationIndex = _.indexBy(locations.objects, 'id')
    data.locationList = _(locations.objects)
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

  data.location = chartDef.locationValue && locationIndex[chartDef.locationValue]
    ? locationIndex[chartDef.locationValue]
    : locationIndex[data.locationList[0].value]

  let officeId = data.location.office_id
  api.indicatorsTree({ office_id: officeId }).then(indicators => {
    let indicatorIndex = _.indexBy(indicators.flat, 'id')
    data.indicatorList = _.sortBy(indicators.objects, 'title')
    data.indicatorSelected = chartDef.indicators.map(id => {
      return indicatorIndex[id]
    })
    // previewChart() // do something here
  })

  let officeIndex = _.indexBy(offices.objects, 'id')
  let campaignList = _(campaigns.objects)
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

  let campaignIndex = _.indexBy(campaignList, 'id')
  data.campaignFilteredList = filterCampaignByLocation(campaignList, data.location)
  data.timeRangeFilteredList = filterTimeRangeByChartType(builderDefinitions.times, data.chartDef.type)
  data.chartTypeFilteredList = builderDefinitions.charts

  if (chartDef.campaignValue && campaignIndex[chartDef.campaignValue]) {
    data.campaign = campaignIndex[chartDef.campaignValue]
  } else {
    data.campaign = data.campaignFilteredList.length > 0
      ? campaignIndex[data.campaignFilteredList[0].id]
      : null
  }

  if (data.indicatorSelected.length > 0) {
    return filterChartTypeByIndicator(data)
  }
}

function filterChartTypeByIndicator (data) {
  return api.chartType(
    {primary_indicator_id: data.indicatorSelected[0].id },
    null,
    {'cache-control': 'no-cache'})
    .then(res => {
      let availableCharts = res.objects.map(chart => {
        return chart.name
      })
      data.chartTypeFilteredList = builderDefinitions.charts.filter(chart => {
        return _.includes(availableCharts, chart.name)
      })
      if (!_.includes(availableCharts, data.chartDef.type)) {
        this.onChangeChart(data.chartTypeFilteredList[0].name)
      }
    })
},

