// import _ from 'lodash'

const processTableChart = (datapoints, locations, indicators, chartDef, layout) => {
  let defaultSortOrder = locations.map(item => item.name)
  // console.log('locations: ', locations)
  console.log('defaultSortOrder: ', defaultSortOrder)
  // defaultSortOrder: datapoints.meta.default_sort_order

  // const indicators_map = _.indexBy(indicators, 'id')
  // const locations_map = _.indexBy(locations, 'id')

  if (!datapoints || datapoints.length === 0) {
    return { options: null, data: null }
  } else {
    const chartOptions = {
      cellSize: 36,
      fontSize: 14,
      margin: { top: 40, right: 40, bottom: 40, left: 40 },
      cellFontSize: 14,
      headers: [],
      // parentLocationMap: _.indexBy(datapoints.meta.parent_location_list, 'name'),
      parentLocationMap: defaultSortOrder,
      defaultSortOrder: defaultSortOrder
    }
    const addedHeaders = {}
    // const chartData = datapoints.objects.map(d => {
    const chartData = datapoints.map(d => {
      const values = []

      let ind = d.indicator
      // d.indicators.forEach(i => {
      if (d.value != null) {
        var displayValue = d.value
          // if (indicators_map[i.indicator].data_format === 'pct') {
          //   displayValue = (i.value * 100).toFixed(1) + ' %'
          // } else if (indicators_map[i.indicator].data_format === 'bool' && i.value === 0) {
          //   displayValue = 'No'
          //   i.value = -1 // temporary hack to deal with coloring the booleans.
          // } else if (indicators_map[i.indicator].data_format === 'bool' && i.value > 0) {
          //   displayValue = 'Yes'
          //   i.value = 2 // temporary hack to deal with coloring the booleans.
          // }

          values.push({
            indicator: ind, // indicators_map[i.indicator],
            value: d.value,
            campaign: d.campaign,
            displayValue: displayValue,
            location: d.location // locations_map[d.location]
          })

          if (!(ind in addedHeaders)) {
            chartOptions.headers.push(ind)
            addedHeaders[ind] = true
          }
        }
      // })

      return {
        name: d.location.name, // locations_map[d.location].name,
        parent_location_id: d.location.parent_location_id, // locations_map[d.location].parent_location_id,
        values: values,
        campaign_id: d.campaign.id
      }
    })
    return { options: chartOptions, data: chartData.slice(0,1) }
  }
}

export default processTableChart
