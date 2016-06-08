import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import { handleActions } from 'redux-actions'

import campaigns from 'reducers/campaigns_reducer'
import dashboards from 'reducers/dashboards_reducer'
import charts from 'reducers/charts_reducer'
import indicators from 'reducers/indicators_reducer'
import locations from 'reducers/locations_reducer'
import users from 'reducers/users_reducer'

const superuser = handleActions({
  FETCH_ALL_META: (state, action) => action.payload.data.objects[0].is_superuser
}, false)

const selected_campaign = handleActions({
  FETCH_ALL_META: (state, action) => action.payload.data.objects[0].campaigns[0],
  SELECT_GLOBAL_CAMPAIGN: (state, action) => action.payload
}, null)

const selected_locations = handleActions({
  SELECT_GLOBAL_LOCATION: (state, action) => {
    // This might not be the best practice. Look into using Object.assign({}) in redux
    state.push(action.payload)
    return state
  }
}, [])

const selected_indicators = handleActions({
  SET_GLOBAL_INDICATORS: (state, action) => action.payload
}, [])

const selected_indicator_tag = handleActions({
  SET_GLOBAL_INDICATOR_TAG: (state, action) => action.payload
}, null)

const reducers = {
  superuser,
  selected_campaign,
  selected_locations,
  selected_indicators,
  selected_indicator_tag,
  charts,
  dashboards,
  campaigns,
  indicators,
  locations,
  users
}

const rootReducer = combineReducers({
  ...reducers,
  routing: routerReducer
})

export default rootReducer
