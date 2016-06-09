import _ from 'lodash'
import { handleActions } from 'redux-actions'

const initial_state = {raw: null, index: null}

const charts = handleActions({
  GET_ALL_CHARTS_SUCCESS: (state, action) => ({
    raw: action.payload,
    index: getChartIndex(action.payload)
  })
}, initial_state)

const getChartIndex = function (charts) {
  const flattened_charts = _.map(charts, chart => flattenChart(chart))
  return _.keyBy(flattened_charts, 'id')
}

const flattenChart = function (chart) {
  const chart_json = chart.chart_json
  delete chart.chart_json
  return Object.assign(chart, chart_json)
}

export default charts
