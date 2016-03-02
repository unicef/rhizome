import _ from 'lodash'

const processTableChart = (datapoints, locations, indicators, chartDef, layout) => {

  const indicators_map = _.indexBy(indicators, 'id')
  const locations_map = _.indexBy(locations, 'id')

  if (!datapoints || datapoints.length === 0) {
    return { options: null, data: null }
  } else {
    const chartOptions = {
      cellSize: 36,
      fontSize: 14,
      margin: { top: 40, right: 40, bottom: 40, left: 40 },
      cellFontSize: 14,
      headers: [],
      parentLocationMap: _.indexBy(datapoints.meta.parent_location_list, 'name'),
      defaultSortOrder: datapoints.meta.default_sort_order
    }
    const addedHeaders = {}

    const chartData = datapoints.objects.map(d => {
      const values = []

      d.indicators.forEach(i => {
        if (i.value != null) {
          var displayValue = i.value
          if (indicators_map[i.indicator].data_format === 'pct') {
            displayValue = (i.value * 100).toFixed(1) + ' %'
          } else if (indicators_map[i.indicator].data_format === 'bool' && i.value === 0) {
            displayValue = 'No'
            i.value = -1 // temporary hack to deal with coloring the booleans.
          } else if (indicators_map[i.indicator].data_format === 'bool' && i.value > 0) {
            displayValue = 'Yes'
            i.value = 2 // temporary hack to deal with coloring the booleans.
          }
          values.push({
            indicator: indicators_map[i.indicator],
            value: i.value,
            campaign: d.campaign,
            displayValue: displayValue,
            location: locations_map[d.location]
          })

          if (!(i.indicator in addedHeaders)) {
            chartOptions.headers.push(indicators_map[i.indicator])
            addedHeaders[i.indicator] = true
          }
        }
      })

      return {
        name: locations_map[d.location].name,
        parent_location_id: locations_map[d.location].parent_location_id,
        values: values,
        campaign_id: d.campaign.id
      }
    })
    return { options: chartOptions, data: chartData }
  }
}

export default processTableChart
