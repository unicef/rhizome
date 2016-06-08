import _ from 'lodash'
import { handleActions } from 'redux-actions'

const dashboards = handleActions({
  FETCH_DASHBOARDS: (state, action) => {
    return getDashboardIndex(action.payload.data.objects)
  },
  FETCH_ALL_META: (state, action) => {
    return getDashboardIndex(action.payload.data.objects[0].dashboards)
  }
}, {})

const getDashboardIndex = function (dashboards) {
  const flattened_dashboards = _.map(dashboards, dashboard => flattenDashboard(dashboard))
  return _.keyBy(flattened_dashboards, 'id')
}

const flattenDashboard = function (dashboard) {
  const rows = JSON.parse(dashboard.rows)
  delete dashboard.rows
  return Object.assign(dashboard, rows)
}

export default dashboards
