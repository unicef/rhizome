import { handleActions } from 'redux-actions'

const data = {
  selected_campaign: null,
  selected_locations: [],
  selected_indicators: [],
  selected_indicator_tag: null,
  datapoints: null
}

const data_entry = handleActions({
  GET_INITIAL_DATA_SUCCESS: (state, action) => {
    return Object.assign({}, state, {
      selected_campaign: action.payload.data.objects[0].campaigns[0]
    })
  },
  FETCH_DATAPOINTS: (state, action) => {
    return Object.assign({}, state, {
      datapoints: action.payload.data.objects
    })
  },
  SELECT_GLOBAL_CAMPAIGN: (state, action) => {
    return Object.assign({}, state, {
      selected_campaign: action.payload
    })
  },
  SELECT_GLOBAL_LOCATION: (state, action) => {
    return Object.assign({}, state, {
      selected_locations: [...state.selected_locations, action.payload]
    })
  },
  SET_GLOBAL_INDICATORS: (state, action) => {
    return Object.assign({}, state, {
      selected_indicators: action.payload
    })
  },
  SET_GLOBAL_INDICATOR_TAG: (state, action) => {
    return Object.assign({}, state, {
      selected_indicator_tag: action.payload
    })
  }
}, data)

export default data_entry
