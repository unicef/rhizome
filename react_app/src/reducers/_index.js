import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'

import campaigns from 'reducers/campaigns_reducer'
import charts from 'reducers/charts_reducer'
import indicators from 'reducers/indicators_reducer'
import locations from 'reducers/locations_reducer'
import users from 'reducers/users_reducer'

const reducers = {campaigns, charts, indicators, locations, users}

const rootReducer = combineReducers({
  ...reducers,
  routing: routerReducer
})

export default rootReducer
