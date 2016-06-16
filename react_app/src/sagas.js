import { watchGetInitialData } from 'actions/global_actions'

import { watchGetAllCampaigns } from 'actions/campaign_actions'
import { watchGetAllIndicators } from 'actions/indicator_actions'
import { watchGetAllLocations } from 'actions/location_actions'
import { watchGetAllCharts } from 'actions/chart_actions'
import { watchGetAllDashboards } from 'actions/dashboard_actions'
import { watchGetAllUsers } from 'actions/user_actions'

import { watchGetDatapoints } from 'actions/datapoint_actions'
import { watchUpdateDatapoint } from 'actions/datapoint_actions'

export const rootSaga = function * () {
  yield [
    watchGetDatapoints(),
    watchUpdateDatapoint(),
    watchGetInitialData(),
    watchGetAllCampaigns(),
    watchGetAllIndicators(),
    watchGetAllLocations(),
    watchGetAllCharts(),
    watchGetAllDashboards(),
    watchGetAllUsers()
  ]
}
