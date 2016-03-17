import Reflux from 'reflux'
import api from 'data/api'

const CampaignActions = Reflux.createActions({
  'fetchCampaigns': { children: ['completed', 'failed'], asyncResult: true }
})

CampaignActions.fetchCampaigns.listenAndPromise(() => {
  return api.campaign(null, null, {'cache-control': 'no-cache'})
})

export default CampaignActions
