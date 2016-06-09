import { watchGetInitialData } from 'actions/global_actions'
import { watchGetAllCampaigns } from 'actions/campaign_actions'

export const rootSaga = function * () {
  yield [
    watchGetInitialData(),
    watchGetAllCampaigns()
  ]
}
