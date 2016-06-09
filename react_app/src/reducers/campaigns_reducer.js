import _ from 'lodash'
import { handleActions } from 'redux-actions'

const data = {raw: null, index: null}

const campaigns = handleActions({
  FETCH_CAMPAIGNS: (state, action) => processCampaigns(action.payload.data.objects),
  GET_INITIAL_DATA_SUCCESS: (state, action) => processCampaigns(action.payload.data.objects[0].campaigns)
}, data)

const processCampaigns = (campaigns) => {
  data.raw = campaigns
  data.index = _.keyBy(campaigns, 'id')
  return data
}

export default campaigns
