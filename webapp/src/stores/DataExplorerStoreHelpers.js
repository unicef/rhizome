import _ from 'lodash'

const DataExplorerStoreHelpers = {
  // =========================================================================== //
  //                                 TABLE CHART                                 //
  // =========================================================================== //
  formatTableChart (datapoints, chart, locations_index, indicators_index) {
    console.log('----- DataExplorerStoreHelpers.formatTableChart')
    const selected_campaign_id = chart.selected_campaigns[0].id
    const filtered_datapoints = datapoints.filter(datapoint => datapoint.campaign.id === selected_campaign_id)
    chart.data = filtered_datapoints.map(datapoint => {
      const values = []
      datapoint.indicators.forEach(i => {
        if (i.value != null) {
          const indicator_id = i.indicator
          let displayValue = i.value
          if (indicators_index[indicator_id].data_format === 'pct') {
            displayValue = (i.value * 100).toFixed(1) + ' %'
          } else if (indicators_index[indicator_id].data_format === 'bool' && i.value === 0) {
            displayValue = 'No'
            i.value = -1 // temporary hack to deal with coloring the booleans.
          } else if (indicators_index[indicator_id].data_format === 'bool' && i.value > 0) {
            displayValue = 'Yes'
            i.value = 2 // temporary hack to deal with coloring the booleans.
          }
          values.push({
            indicator: indicators_index[indicator_id],
            value: i.value,
            campaign: datapoint.campaign,
            displayValue: displayValue,
            location: locations_index[datapoint.location]
          })
        }
      })

      return {
        name: locations_index[datapoint.location].name,
        parent_location_id: locations_index[datapoint.location].parent_location_id,
        values: values,
        campaign_id: datapoint.campaign.id
      }
    })

    return chart
  },

  // =========================================================================== //
  //                                  LINE CHART                                 //
  // =========================================================================== //
  formatLineChart (datapoints, chart, groups, layout) {
    if (!datapoints || datapoints.length === 0) {
      return chart
    }

    chart.data = _(datapoints).groupBy(chart.groupBy)
      .map(datapoint => {
        return {
          name: groups[datapoint[0].indicator.id].name,
          values: _.sortBy(datapoint, _.method('campaign.start_date.getTime'))
        }
      })
      .value()

    return chart
  },

  // =========================================================================== //
  //                                CHOROPLETH MAP                               //
  // =========================================================================== //
  formatChoroplethMap (datapoints, chart, locations_index, indicators_index, layout) {
    const selected_indicators = chart.selected_indicators
    const x = selected_indicators[0] ? selected_indicators[0].id : 0
    if (!datapoints || datapoints.length === 0) {
      chart.data = chart.features
      return chart
    }

    const xAxis = x
    // const yAxis = chart.y
    // const zAxis = chart.z
    const groupedDatapoints = _(datapoints).groupBy('indicator.id').value()
    const index = _.indexBy(groupedDatapoints[xAxis], 'location.id')
    // let bubbleIndex = null
    // let gradientIndex = null

    // if (yAxis) {
    //   let maxValue = 5000
    //   let bubbleValues = groupedDatapoints[yAxis].map(datapoint => datapoint.value)
    //   bubbleIndex = _.indexBy(groupedDatapoints[yAxis], 'location.id')
    //   chart.maxBubbleValue = Math.min(Math.max(...bubbleValues), maxValue)
    //   chart.bubbleValue = _.property('properties.bubbleValue')
    // }
    // if (zAxis) {
    //   gradientIndex = _.indexBy(groupedDatapoints[zAxis], 'location.id')
    //   chart.indicatorName = _.result(_.find(selected_indicators_index, indicator => indicator.id === zAxis), 'short_name')
    //   chart.stripeValue = _.property('properties.stripeValue')
    // }

    // Make sure we only get data for the current campaign maps can't
    // display historical data. Index by location for quick lookup.
    const dataIdx = _(datapoints)
      .filter(d => d.campaign.id === chart.selected_campaigns[0])
      .indexBy('location.id')
      .value()

    chart.features.forEach(feature => {
      var datapoint = dataIdx[feature.properties.location_id]
      if (datapoint) {
        feature.properties[datapoint.indicator.id] = datapoint.value
      }
    })

    chart.data = chart.features.map(feature => {
      const datapoint = index[feature.properties.location_id]
      const properties = _.merge({}, datapoint.location, { value: datapoint['value'] })
      // if (yAxis) {
      //   const bubbleLocation = bubbleIndex[feature.properties.location_id]
      //   properties.bubbleValue = bubbleLocation['value']
      // }
      // if (zAxis) {
      //   const gradientLocation = gradientIndex[feature.properties.location_id]
      //   properties.stripeValue = gradientLocation['value']
      // }
      return _.merge({}, feature, {properties: properties}, datapoint.location)
    })

    return chart
  },

  // =========================================================================== //
  //                                   PIE CHART                                 //
  // =========================================================================== //
  formatPieChart (meltPromise, selected_indicators, layout) {
    // TO DO
    return null
  },

  formatColumnChart (meltPromise, lower, upper, groups, chart_def, layout) {
    // TO DO
    return null
  },

  formatScatterChart (datapoints, selected_locations_index, selected_indicators_index, chart_def, layout) {
    // TO DO
    return null
  },

  formatBarChart () {
    // TO DO
    return null
  }
}

export default DataExplorerStoreHelpers
