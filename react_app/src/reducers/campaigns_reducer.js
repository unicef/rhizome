import _ from 'lodash'
import { handleActions } from 'redux-actions'

const data = {raw: null, index: null}

const campaigns = handleActions({
  FETCH_CAMPAIGNS_REQUEST: (state, action) => processCampaigns(action.payload.data.objects),
  FETCH_ALL_META_REQUEST: (state, action) => processCampaigns(action.payload.data.objects[0].campaigns)
}, {})

const processCampaigns = (campaigns) => {
  data.raw = campaigns
  data.index = _.keyBy(campaigns, 'id')
  return data
}

export default campaigns
