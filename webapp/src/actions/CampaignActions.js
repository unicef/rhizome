import Reflux from 'reflux'
import CampaignAPI from 'data/requests/CampaignAPI'

const CampaignActions = Reflux.createActions({
  'fetchCampaigns': { children: ['completed', 'failed'], asyncResult: true }
})

CampaignActions.fetchCampaigns.listenAndPromise(() => {
  return CampaignAPI.getCampaigns()
})

export default CampaignActions
