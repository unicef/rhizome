import _ from 'lodash'
import moment from 'moment'
import d3 from 'd3'

import builderDefinitions from 'stores/chartBuilder/builderDefinitions'
import ChartInfo from 'components/molecules/charts_d3/ChartInfo'

import api from 'data/api'
import treeify from 'data/transform/treeify'
import ancestryString from 'data/transform/ancestryString'
import palettes from 'components/molecules/charts_d3/utils/palettes'

const getSelectedLocations = (location_ids, locationIndex) => {
  if (location_ids) {
    if (Array.isArray(location_ids)) {
      return location_ids.map(id => locationIndex[id])
    } else {
      return [locationIndex[location_ids]]
    }
  } else {
    return []
  }
}

const getSelectedIndicators = (indicator_ids, indicatorIndex) => {
  if (indicator_ids) {
    if (Array.isArray(indicator_ids)) {
      return indicator_ids.map(id => indicatorIndex[id])
    } else {
      return [indicatorIndex[indicator_ids]]
    }
  } else {
    return []
  }
}

const getSelectedCampaign = (campaign_id, campaignIndex) => {
  if (campaign_id && campaignIndex[campaign_id]) {
    return campaignIndex[campaign_id]
  } else {
    return campaignIndex[0]
  }
}

const getLocationList = (locations) => {
  return _(locations.objects).map(location => {
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
}

const getCampaignList = (locations) => {
  return _(campaigns.objects).map(campaign => {
    return _.assign({}, campaign, {
      'start_date': moment(campaign.start_date, 'YYYY-MM-DD').toDate(),
      'end_date': moment(campaign.end_date, 'YYYY-MM-DD').toDate(),
      'office': officeIndex[campaign.office_id]
    })
  })
  .sortBy(_.method('start_date.getTime'))
  .reverse()
  .value()
}

export default {
  async getPromises () {
    return [ await api.locations(), await api.campaign(), await api.office(), await api.indicators(null, null, { 'cache-control': 'no-cache' }) ]
  },

  fetchChart (chartDef, layout, responses) {
    console.log('chartDef', chartDef)
    console.log('layout', layout)
    console.log('responses', responses)
    const [locations, campaigns, offices, indicators] = responses

    const locationLevelValue = _.findIndex(builderDefinitions.locationLevels, { value: chartDef.location_depth })

    const indicatorIndex = _.indexBy(indicators.objects, 'id')
    const locationIndex = _.indexBy(locations.objects, 'id')
    const officeIndex = _.indexBy(offices.objects, 'id')
    const campaignIndex = _.indexBy(campaigns.objects, 'id')

    const selectedIndicators = chartDef.selectedIndicators ? chartDef.selectedIndicators : getSelectedIndicators(chartDef.indicator_ids, indicatorIndex)
    const selectedLocations = chartDef.selectedLocations ? chartDef.selectedLocations : getSelectedLocations(chartDef.location_ids, locationIndex)
    const selectedCampaign = getSelectedCampaign(chartDef.campaign_id, campaignIndex)

    const selectedLocationIndex = _.indexBy(selectedLocations, 'id')
    const groups = chartDef.groupBy === 'indicator' ? indicatorIndex : selectedLocationIndex

    const indicatorOrder = selectedIndicators.map(indicator => { return indicator.short_name })

    const lower = moment(chartDef.startDate, 'YYYY-MM-DD')
    const upper = moment(chartDef.endDate, 'YYYY-MM-DD')


    let query = {
      indicator__in: chartDef.indicator_ids,
      campaign_start: chartDef.startDate,
      campaign_end: chartDef.endDate,
      chart_type: chartDef.type
    }

    // a map should always query for the sub locations of the selected //
    if ( chartDef.type === 'ChoroplethMap' ){
      query['parent_location_id__in'] = _.map(selectedLocations, _.property('id'))
    } else {
      query['location_id__in'] = _.map(selectedLocations, _.property('id'))
    }

    console.log('this', this)

    return ChartInfo.getChartInfo(api.datapoints(query),
      chartDef.type,
      selectedIndicators,
      selectedLocations,
      layout
    ).then(chart => {
      if (!chart.data) {
        return { data: [], options: null }
      }
      let newOptions = _.clone(chart.options)
        newOptions.indicatorsSelected = selectedIndicators
      if (chart.options && !chart.options.yFormat) {
        newOptions.yFormat = d3.format(chartDef.yFormat)
      }
      if (chart.options && !chart.options.xFormat) {
        newOptions.xFormat = d3.format(chartDef.xFormat)
      }
      if (chart.options && !chart.options.xDomain) {
        newOptions.xDomain = indicatorOrder
      }
      if (chartDef.palette) {
        newOptions.color = palettes[chartDef.palette]
      }
      newOptions.chartInDashboard = true
      return { data: chart.data, options: newOptions }
    })
  }
}
