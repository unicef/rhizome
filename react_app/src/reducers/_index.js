import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import { handleActions } from 'redux-actions'

import data_entry from 'reducers/data_entry_reducer'
import campaigns from 'reducers/campaigns_reducer'
import dashboards from 'reducers/dashboards_reducer'
import charts from 'reducers/charts_reducer'
import indicators from 'reducers/indicators_reducer'
import locations from 'reducers/locations_reducer'
import users from 'reducers/users_reducer'

const superuser = handleActions({
  GET_INITIAL_DATA_SUCCESS: (state, action) => action.payload.data.objects[0].is_superuser
}, false)

const reducers = {
  superuser,
  charts,
  dashboards,
  data_entry,
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
