import _ from 'lodash'
import aspects from 'components/molecules/charts_d3/utils/aspects'
import api from 'data/api'

const processChoroplethMap = (dataPromise, locations, indicators, chartDef, layout) => {
  let xAxis = chartDef.x
  let yAxis = chartDef.y
  let zAxis = chartDef.z

  var locationsIndex = _.indexBy(locations, 'id')
  return Promise.all([dataPromise, api.geo({ parent_location_id__in: locations.map(location => { return location.id }) }, null, {'cache-control': 'max-age=604800, public'})])
  .then(_.spread((data, border) => {
    var chartOptions = {
      aspect: aspects[layout].choroplethMap,
      name: d => _.get(locationsIndex, '[' + d.properties.location_id + '].name', ''),
      border: border.objects.features
    }
    if (!data || data.length === 0) {
      return { options: chartOptions, data: border.objects.features }
    }

    let indicatorIndex = _(data).groupBy('indicator').value()
    let index = _.indexBy(indicatorIndex[xAxis], 'location')
    let bubbleIndex = null
    let gradientIndex = null
    if (yAxis) {
      let maxValue = 5000
      let bubbleValues = indicatorIndex[yAxis].map(v => v.value)
      bubbleIndex = _.indexBy(indicatorIndex[yAxis], 'location')
      chartOptions.maxBubbleValue = Math.min(Math.max(...bubbleValues), maxValue)
      chartOptions.bubbleValue = _.property('properties.bubbleValue')
    }
    if (zAxis) {
      gradientIndex = _.indexBy(indicatorIndex[zAxis], 'location')
      chartOptions.indicatorName = _.result(_.find(indicators, d => { return d.id === zAxis }), 'short_name')
      chartOptions.stripeValue = _.property('properties.stripeValue')
    }

    var chartData = border.objects.features.map(feature => {
      var location = _.get(index, feature.properties.location_id)
      let properties = {value: _.get(location, 'value')}
      if (yAxis) {
        let bubbleLocation = _.get(bubbleIndex, feature.properties.location_id)
        properties.bubbleValue = _.get(bubbleLocation, 'value')
      }
      if (zAxis) {
        let gradientLocation = _.get(gradientIndex, feature.properties.location_id)
        properties.stripeValue = _.get(gradientLocation, 'value')
      }
      return _.merge({}, feature, {properties: properties})
    })

    return { options: chartOptions, data: chartData }
  }))
}

export default processChoroplethMap
