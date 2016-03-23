import d3 from 'd3'
import _ from 'lodash'
import moment from 'moment'
import LocationSelectorActions from 'actions/LocationSelectorActions'
import chartOptionsHelpers from 'components/molecules/charts/utils/chartOptionsHelpers'
import aspects from 'components/molecules/charts/utils/aspects'

const ChartStoreHelpers = {
  // =========================================================================== //
  //                                 TABLE CHART                                 //
  // =========================================================================== //
  formatTableChart (datapoints, chart, locations_index, indicators_index) {
    chart.data = datapoints.map(datapoint => {
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
  //                                CHOROPLETH MAP                               //
  // =========================================================================== //
  formatChoroplethMap (datapoints, chart, locations_index, indicators_index, layout) {
    const selected_locations = chart.def.location_ids.map(id => locations_index[id])
    const selected_indicators = chart.def.indicator_ids.map(id => indicators_index[id])
    const selected_locations_index = _.indexBy(selected_locations, 'id')
    const selected_indicators_index = _.indexBy(selected_indicators, 'id')
    const mapIndicator = selected_indicators_index[chart.def.x]
    chart.def.aspect = aspects[layout].choroplethMap
    chart.def.name = d => _.get(selected_locations_index, '[' + d.properties.location_id + '].name', '')
    chart.def.border = chart.def.features
    chart.def.data_format = mapIndicator.data_format
    chart.def.domain = () => [mapIndicator.bad_bound, mapIndicator.good_bound]
    chart.def.value = _.property(`properties[${mapIndicator.id}]`)
    chart.def.xFormat = this._getChartFormat(mapIndicator)
    // chart.def.onClick = d => DashboardActions.navigate({ location: d })
    if (!datapoints || datapoints.length === 0) {
      return { data: chart.def.features, def: chart.def }
    }

    const xAxis = chart.def.x
    const yAxis = chart.def.y
    const zAxis = chart.def.z
    const groupedDatapoints = _(datapoints).groupBy('indicator.id').value()
    const index = _.indexBy(groupedDatapoints[xAxis], 'location.id')
    let bubbleIndex = null
    let gradientIndex = null

    if (yAxis) {
      let maxValue = 5000
      let bubbleValues = groupedDatapoints[yAxis].map(datapoint => datapoint.value)
      bubbleIndex = _.indexBy(groupedDatapoints[yAxis], 'location.id')
      chart.def.maxBubbleValue = Math.min(Math.max(...bubbleValues), maxValue)
      chart.def.bubbleValue = _.property('properties.bubbleValue')
    }
    if (zAxis) {
      gradientIndex = _.indexBy(groupedDatapoints[zAxis], 'location.id')
      chart.def.indicatorName = _.result(_.find(selected_indicators_index, indicator => indicator.id === zAxis), 'short_name')
      chart.def.stripeValue = _.property('properties.stripeValue')
    }

    // Make sure we only get data for the current campaign maps can't
    // display historical data. Index by location for quick lookup.
    const dataIdx = _(datapoints)
      .filter(d => d.campaign.id === chart.def.campaign_ids[0])
      .indexBy('location.id')
      .value()

    chart.def.features.forEach(feature => {
      var datapoint = dataIdx[feature.properties.location_id]
      if (datapoint) {
        feature.properties[datapoint.indicator.id] = datapoint.value
      }
    })

    chart.data = chart.def.features.map(feature => {
      const datapoint = index[feature.properties.location_id]
      const properties = _.merge({}, datapoint.location, { value: datapoint['value'] })
      if (yAxis) {
        const bubbleLocation = bubbleIndex[feature.properties.location_id]
        properties.bubbleValue = bubbleLocation['value']
      }
      if (zAxis) {
        const gradientLocation = gradientIndex[feature.properties.location_id]
        properties.stripeValue = gradientLocation['value']
      }
      return _.merge({}, feature, {properties: properties}, datapoint.location)
    })

    return chart
  },

  // =========================================================================== //
  //                                  LINE CHART                                 //
  // =========================================================================== //
  formatLineChart (datapoints, chart, groups, layout) {
    // The LineChart has its own logic that determines the domain and it seems to work
    // more correctly than this code.
    // let lower = moment(chart.def.start_date, 'YYYY-MM-DD')
    // let upper = moment(chart.def.end_date, 'YYYY-MM-DD')
    // if (!lower) { // set the lower bound from the lowest datapoint value
    //   const sortedDates = _.sortBy(datapoints, _.method('campaign.start_date.getTime'))
    //   lower = moment(_.first(sortedDates).campaign.start_date)
    // }
    // chart.def.domain = _.constant([lower.toDate(), upper.toDate()])

    chart.def.aspect = aspects[layout].lineChart
    chart.def.values = _.property('values')
    chart.def.x = _.property('campaign.start_date')
    chart.def.xFormat = d => moment(d).format('MMM YYYY')
    chart.def.y = _.property('value')
    chart.def.xLabel = chart.def.xLabel
    chart.def.yLabel = chart.def.yLabel
    chart.def.height = 350

    const def = chartOptionsHelpers.generateMarginForAxisLabel(chart.def)

    if (!datapoints || datapoints.length === 0) {
      return chart
    }

    const data = _(datapoints).groupBy(chart.def.groupBy)
      .map(datapoint => {
        return {
          name: groups[datapoint[0].indicator.id].name,
          values: _.sortBy(datapoint, _.method('campaign.start_date.getTime'))
        }
      })
      .value()

    return {data: data, def: def}
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
  },
  _getChartFormat (indicator) {
    let d3Format = d3.format('')
    if (indicator.data_format === 'pct') {
      d3Format = d3.format(',.1%')
    }
    return d3Format
  }
}

export default ChartStoreHelpers
