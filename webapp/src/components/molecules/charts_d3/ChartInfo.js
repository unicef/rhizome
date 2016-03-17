import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'

import palettes from 'components/molecules/charts_d3/utils/palettes'
import LineChartInfo from 'components/molecules/charts_d3/line_chart/LineChartInfo'
import PieChartInfo from 'components/molecules/charts_d3/pie_chart/PieChartInfo'
import ChoroplethMapInfo from 'components/molecules/charts_d3/choropleth_map/ChoroplethMapInfo'
import ColumnChartInfo from 'components/molecules/charts_d3/column_chart/ColumnChartInfo'
import ScatterChartInfo from 'components/molecules/charts_d3/scatter_chart/ScatterChartInfo'
import BarChartInfo from 'components/molecules/charts_d3/bar_chart/BarChartInfo'
import TableChartInfo from 'components/molecules/charts_d3/table_chart/TableChartInfo'

const ChartInfo = {

  // here, datapoints is the full api response, not just the .objects
  getChartInfo: function (chartDef, datapoints, selectedLocations, selectedIndicators, layout) {
    const indicatorOrder = selectedIndicators.map(indicator => indicator.short_name)
    const chartInfo = this.getInfoForChartType(chartDef, datapoints, selectedLocations, selectedIndicators, layout)
    if (!chartInfo.data) {
      return { data: [], options: null }
    }
    let newOptions = _.clone(chartInfo.options)
    newOptions.selected_indicators = selectedIndicators
    newOptions.color = chartDef.palette ? palettes[chartDef.palette] : palettes['traffic_light']
    newOptions.chartInDashboard = true
    if (chartInfo.options) {
      newOptions.yFormat = !chartInfo.options.yFormat ? d3.format(chartDef.yFormat) : null
      newOptions.xFormat = !chartInfo.options.xFormat ? d3.format(chartDef.xFormat) : null
      newOptions.xDomain = !chartInfo.options.xDomain ? indicatorOrder : null
    }

    return { data: chartInfo.data, options: newOptions }
  },

  getInfoForChartType: function (chartDef, datapoints, selectedLocations, selectedIndicators) {
    const selectedLocationIndex = _.indexBy(selectedLocations, 'id')
    const selectedIndicatorIndex = _.indexBy(selectedIndicators, 'id')
    const groups = chartDef.groupBy === 'indicator' ? selectedIndicatorIndex : selectedLocationIndex
    const lower = moment(chartDef.startDate, 'YYYY-MM-DD')
    const upper = moment(chartDef.endDate, 'YYYY-MM-DD')
    const layout = 1 // hard coded for now
    let indicatorArray = selectedIndicators.map(_.property('id'))
    let meltPromise = this.melt(datapoints, indicatorArray)

    switch (chartDef.type) {
      case 'LineChart':
        return LineChartInfo.getChartInfo(meltPromise, lower, upper, groups, chartDef, layout)
      case 'PieChart':
        return PieChartInfo.getChartInfo(meltPromise, selectedIndicators, layout)
      case 'ChoroplethMap':
        return ChoroplethMapInfo.getChartInfo(meltPromise, selectedLocations, selectedIndicators, chartDef, layout)
      case 'ColumnChart':
        return ColumnChartInfo.getChartInfo(meltPromise, lower, upper, groups, chartDef, layout)
      case 'ScatterChart':
        return ScatterChartInfo.getChartInfo(datapoints, selectedLocations, selectedIndicators, chartDef, layout)
      case 'BarChart':
        return BarChartInfo.getChartInfo(datapoints, selectedLocations, selectedIndicators, chartDef, layout)
      case 'TableChart':
        return TableChartInfo.getChartInfo(datapoints, selectedLocations, selectedIndicators, chartDef, layout)
      default:
        console.log('No such chart type: ' + chartDef.type)
    }
  },

  melt: function (data, indicatorArray) {
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
}

const tooltipDiv = document.createElement('div')
document.body.appendChild(tooltipDiv)

export default ChartInfo
