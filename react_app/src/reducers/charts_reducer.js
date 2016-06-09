import _ from 'lodash'
import { handleActions } from 'redux-actions'

const charts = handleActions({
  FETCH_CHARTS: (state, action) => {
    return getChartIndex(action.payload.data.objects)
  },
  GET_INITIAL_DATA_SUCCESS: (state, action) => {
    return getChartIndex(action.payload.data.objects[0].charts)
  }
}, {})

const getChartIndex = function (charts) {
  const flattened_charts = _.map(charts, chart => flattenChart(chart))
  return _.keyBy(flattened_charts, 'id')
}

const flattenChart = function (chart) {
  const chart_json = JSON.parse(chart.chart_json)
  delete chart.chart_json
  return Object.assign(chart, chart_json)
}

export default charts
