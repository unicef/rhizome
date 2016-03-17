import _ from 'lodash'
import api from 'data/api'
import aspects from 'components/molecules/charts_d3/utils/aspects'

const ChartStoreHelpers = {
  getTableChartData (datapoints, locations_index, indicators_index, chartOptions) {
    return datapoints.map(datapoint => {
      const values = []
      datapoint.indicators.forEach(i => {
        if (i.value != null) {
          let displayValue = i.value
          if (indicators_index[i.indicator].data_format === 'pct') {
            displayValue = (i.value * 100).toFixed(1) + ' %'
          } else if (indicators_index[i.indicator].data_format === 'bool' && i.value === 0) {
            displayValue = 'No'
            i.value = -1 // temporary hack to deal with coloring the booleans.
          } else if (indicators_index[i.indicator].data_format === 'bool' && i.value > 0) {
            displayValue = 'Yes'
            i.value = 2 // temporary hack to deal with coloring the booleans.
          }
          values.push({
            indicator: indicators_index[i.indicator],
            value: i.value,
            campaign: datapoint.campaign,
            displayValue: displayValue,
            location: locations_index[datapoint.location]
          })
        }
      })

      const data = {
        name: locations_index[datapoint.location].name,
        parent_location_id: locations_index[datapoint.location].parent_location_id,
        values: values,
        campaign_id: datapoint.campaign.id
      }
      return data
    })
  },

  getLineChartData (meltPromise, lower, upper, groups, chart_def, layout) {
    // TO DO
    return null
  },

  getPieChartData (meltPromise, selected_indicators, layout) {
    // TO DO
    return null
  },

  getChoroplethMapData (datapoints, selected_locations_index, selected_indicators, chart_def, layout, features) {
    console.log('---------------------------- getChoroplethMapData ---------------------------')
    let xAxis = chart_def.x
    let yAxis = chart_def.y
    let zAxis = chart_def.z

    var chartOptions = {
      aspect: aspects[layout].choroplethMap,
      name: d => _.get(selected_locations_index, '[' + d.properties.location_id + '].name', ''),
      border: features
    }
    if (!datapoints || datapoints.length === 0) {
      return { options: chartOptions, data: features }
    }

    let indicatorIndex = _(datapoints).groupBy('indicator').value()
    let index = _.indexBy(indicatorIndex[xAxis], 'location')
    let bubbleIndex = null
    let gradientIndex = null
    // if (yAxis) {
    //   let maxValue = 5000
    //   let bubbleValues = indicatorIndex[yAxis].map(v => v.value)
    //   bubbleIndex = _.indexBy(indicatorIndex[yAxis], 'location')
    //   chartOptions.maxBubbleValue = Math.min(Math.max(...bubbleValues), maxValue)
    //   chartOptions.bubbleValue = _.property('properties.bubbleValue')
    // }
    // if (zAxis) {
    //   gradientIndex = _.indexBy(indicatorIndex[zAxis], 'location')
    //   chartOptions.indicatorName = _.result(_.find(selected_indicators, indicator => indicator.id === zAxis), 'short_name')
    //   chartOptions.stripeValue = _.property('properties.stripeValue')
    // }

    var chartData = features.map(feature => {
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
  },

  getColumnChartData (meltPromise, lower, upper, groups, chart_def, layout) {
    // TO DO
    return null
  },

  getScatterChartData (datapoints, selected_locations_index, selected_indicators_index, chart_def, layout) {
    // TO DO
    return null
  },

  getBarChartData () {
    // TO DO
    return null
  }
}

export default ChartStoreHelpers
