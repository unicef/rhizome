import Reflux from 'reflux'

const CampaignSelectorActions = Reflux.createActions({
  'selectCampaign': 'selectCampaign',
  'deselectCampaign': 'deselectCampaign',
  'reorderCampaign': 'reorderCampaign',
  'setSelectedCampaigns': 'setSelectedCampaigns',
  'clearSelectedCampaigns': 'clearSelectedCampaigns'
})

export default CampaignSelectorActions
