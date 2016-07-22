import _ from 'lodash'
import moment from 'moment'
import { handleActions } from 'redux-actions'

const initial_state = {raw: null, index: null}

export const campaigns = handleActions({
  GET_ALL_CAMPAIGNS_SUCCESS: (state, action) => ({
    raw: action.payload,
    index: _.keyBy(action.payload, 'id')
  })
}, initial_state)

export const campaign_types = handleActions({
  GET_ALL_CAMPAIGN_TYPES_SUCCESS: (state, action) => ({
    raw: action.payload,
    index: _.keyBy(action.payload, 'id')
  })
}, {raw: null, index: null})

export const campaign = handleActions({
  UPDATE_CAMPAIGN_SUCCESS: (state, action) => {
    console.log('action', action)
    // return Object.assign({}, state, {name: action.payload})
  }
}, {
  id: null,
  name: '',
  start_date: moment().format('YYYY-MM-DD'),
  end_date: moment().format('YYYY-MM-DD'),
  campaign_type_id: null,
  top_lvl_indicator_tag_id: null,
  top_lvl_location_id: null,
  pct_complete: 0
})
