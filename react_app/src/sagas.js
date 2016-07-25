import { watchGetInitialData } from 'actions/global_actions'

import { watchGetAllCampaigns } from 'actions/campaign_actions'
import { watchUpdateCampaign } from 'actions/campaign_actions'
import { watchGetAllCampaignTypes } from 'actions/campaign_actions'
import { watchGetAllIndicators } from 'actions/indicator_actions'
import { watchUpdateIndicator } from 'actions/indicator_actions'
import { watchGetAllLocations } from 'actions/location_actions'
import { watchGetAllLocationTypes } from 'actions/location_actions'
import { watchUpdateLocation } from 'actions/location_actions'
import { watchGetAllCharts } from 'actions/chart_actions'
import { watchGetAllDashboards } from 'actions/dashboard_actions'
import { watchGetAllUsers } from 'actions/user_actions'

import { watchGetDatapoints } from 'actions/datapoint_actions'
import { watchUpdateDatapoint } from 'actions/datapoint_actions'
import { watchRemoveDatapoint } from 'actions/datapoint_actions'

export const rootSaga = function * () {
  yield [
    watchGetDatapoints(),
    watchUpdateDatapoint(),
    watchRemoveDatapoint(),
    watchGetInitialData(),
    watchGetAllCampaigns(),
    watchUpdateCampaign(),
    watchGetAllCampaignTypes(),
    watchGetAllIndicators(),
    watchUpdateIndicator(),
    watchGetAllLocations(),
    watchGetAllLocationTypes(),
    watchUpdateLocation(),
    watchGetAllCharts(),
    watchGetAllDashboards(),
    watchGetAllUsers()
  ]
}
