import _ from 'lodash'
import { handleActions } from 'redux-actions'

const campaigns = handleActions({
  FETCH_CAMPAIGNS_REQUEST: (state, action) => _.keyBy(action.payload.data.objects, 'id'),
  FETCH_ALL_META_REQUEST: (state, action) => _.keyBy(action.payload.data.objects[0].campaigns, 'id')
}, {})

export default campaigns
