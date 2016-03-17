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

  getChoroplethMapData (meltPromise, selected_locations_index, selected_indicators, chart_def, layout) {
    // TO DO
    return null
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
