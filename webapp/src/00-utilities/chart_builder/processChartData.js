import _ from 'lodash'
import processLineChart from '00-utilities/chart_builder/LineChart'
import processPieChart from '00-utilities/chart_builder/PieChart'
import processChoroplethMap from '00-utilities/chart_builder/ChoroplethMap'
import processColumnChart from '00-utilities/chart_builder/ColumnChart'
import processScatterChart from '00-utilities/chart_builder/ScatterChart'
import processBarChart from '00-utilities/chart_builder/BarChart'
import processTableChart from '00-utilities/chart_builder/TableChart'

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

const processChartData = {
  init: function (dataPromise, chartType, indicators, locations, lower, upper, groups, chartDef, layout) {
    let indicatorArray = indicators.map(_.property('id'))
    let meltPromise = dataPromise.then(data => { return melt(data, indicatorArray) })
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
        para: [dataPromise, locations, indicators, chartDef, layout]
      },
      BarChart: {
        fn: processBarChart,
        para: [dataPromise, locations, indicators, chartDef, layout]
      },
      TableChart: {
        fn: processTableChart,
        para: [dataPromise, locations, indicators, chartDef, layout]
      }
    }
    return chartProcessors[chartType].fn(...chartProcessors[chartType].para)
  }

}
const tooltipDiv = document.createElement('div')
document.body.appendChild(tooltipDiv)

export default processChartData
