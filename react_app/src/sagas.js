import { watchGetInitialData } from 'actions/global_actions'
import { watchGetAllCampaigns } from 'actions/campaign_actions'
import { watchGetAllIndicators } from 'actions/indicator_actions'
import { watchGetAllLocations } from 'actions/location_actions'
import { watchGetAllCharts } from 'actions/chart_actions'
import { watchGetAllDashboards } from 'actions/dashboard_actions'
import { watchGetAllUsers } from 'actions/user_actions'

export const rootSaga = function * () {
  yield [
    watchGetInitialData(),
    watchGetAllCampaigns(),
    watchGetAllIndicators(),
    watchGetAllLocations(),
    watchGetAllCharts(),
    watchGetAllDashboards(),
    watchGetAllUsers()
  ]
}
