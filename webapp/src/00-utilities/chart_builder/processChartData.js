import _ from 'lodash'
import processLineChart from '00-utilities/chart_builder/LineChart'
import processPieChart from '00-utilities/chart_builder/PieChart'
import processChoroplethMap from '00-utilities/chart_builder/ChoroplethMap'
import processColumnChart from '00-utilities/chart_builder/ColumnChart'
import processScatterChart from '00-utilities/chart_builder/ScatterChart'
import processBarChart from '00-utilities/chart_builder/BarChart'
import processTableChart from '00-utilities/chart_builder/TableChart'

import d3 from 'd3'
import palettes from '00-utilities/palettes'
import moment from 'moment'

const prepChartData = (chartDef, datapoints, selectedLocations, selectedIndicators) => {

  const selectedLocationIndex = _.indexBy(selectedLocations, 'id')
  const selectedIndicatorsIndex = _.indexBy(selectedIndicators, 'id')
  const groups = chartDef.groupBy === 'indicator' ? selectedIndicatorsIndex : selectedLocationIndex
  const lower = moment(chartDef.startDate, 'YYYY-MM-DD')
  const upper = moment(chartDef.endDate, 'YYYY-MM-DD')
  const layout = 1 // hard coded for now

  let indicatorOrder = null
  let chart = {}
  if (selectedIndicators) {
    indicatorOrder = selectedIndicators.map(indicator => { return indicator.short_name })
    chart = processChartData.init(datapoints, chartDef, selectedIndicators, selectedLocations, lower, upper, groups, layout)
  }

  if (!chart.data) {
    return { data: [], options: null }
  }
  let newOptions = _.clone(chart.options)
  newOptions.indicatorsSelected = selectedIndicators
  newOptions.color = chartDef.palette ? palettes[chartDef.palette] : null
  newOptions.chartInDashboard = true
  if (chart.options) {
    newOptions.yFormat = !chart.options.yFormat ? d3.format(chartDef.yFormat) : null
    newOptions.xFormat = !chart.options.xFormat ? d3.format(chartDef.xFormat) : null
    newOptions.xDomain = !chart.options.xDomain ? indicatorOrder : null
  }

  return { data: chart.data, options: newOptions }
}

const processChartData = {
  init: function (datapoints, chartDef, indicators, locations, lower, upper, groups, layout) {
    let indicatorArray = indicators.map(_.property('id'))
    let meltPromise = melt(datapoints, indicatorArray)
    let chartProcessors = {
      LineChart: {
        fn: processLineChart,
        para: [meltPromise, lower, upper, groups, chartDef, layout]
      },
      PieChart: {
        fn: processPieChart,
        para: [meltPromise, indicators, layout]
      },
      ChoroplethMap: {
        fn: processChoroplethMap,
        para: [meltPromise, locations, indicators, chartDef, layout]
      },
      ColumnChart: {
        fn: processColumnChart,
        para: [meltPromise, lower, upper, groups, chartDef, layout]
      },
      ScatterChart: {
        fn: processScatterChart,
        para: [datapoints, locations, indicators, chartDef, layout]
      },
      BarChart: {
        fn: processBarChart,
        para: [datapoints, locations, indicators, chartDef, layout]
      },
      TableChart: {
        fn: processTableChart,
        para: [datapoints, locations, indicators, chartDef, layout]
      }
    }
    return chartProcessors[chartDef.type].fn(...chartProcessors[chartDef.type].para)
  }
}

const melt = (data, indicatorArray) => {
  const dataset = data.objects
  const baseIndicators = indicatorArray.map(indicator => {
    return { indicator: indicator + '', value: 0 }
  })
  const o = _(dataset).map(d => {
    const base = _.omit(d, 'indicators')
    const indicatorFullList = _.assign(_.cloneDeep(baseIndicators), d.indicators)
    return indicatorFullList.map(indicator => {
      return _.assign({}, base, indicator)
    })
  })
  .flatten()
  .value()

  return o
}

const tooltipDiv = document.createElement('div')
document.body.appendChild(tooltipDiv)

export default prepChartData
