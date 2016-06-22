import moment from 'moment'
import _ from 'lodash'
import { handleActions } from 'redux-actions'

const data = {
  start_date: moment().format('YYYY-MM-DD'),
  end_date: moment().format('YYYY-MM-DD'),
  data_type: 'campaign', // or date
  location_depth: 0,
  selected_campaign: null,
  selected_locations: [],
  selected_indicators: [],
  selected_indicator_tag: null,
  indicator_filter: { id: 0, value: 0, title: 'All Districts', type: 'LPD Status' },
  datapoints: {meta: null, raw: null, flattened: null},
  dataParamsChanged: false
}

const data_entry = handleActions({
  SET_DATA_ENTRY_START_DATE: (state, action) => {
    return Object.assign({}, state, {
      start_date: action.payload,
      dataParamsChanged: true
    })
  },
  SET_DATA_ENTRY_END_DATE: (state, action) => {
    return Object.assign({}, state, {
      end_date: action.payload,
      dataParamsChanged: true
    })
  },
  TOGGLE_DATA_ENTRY_TYPE: (state, action) => {
    return Object.assign({}, data, {
      data_type: state.data_type === 'campaign' ? 'date' : 'campaign'
    })
  },
  GET_INITIAL_DATA_SUCCESS: (state, action) => {
    return Object.assign({}, state, {
      selected_campaign: action.payload.data.objects[0].campaigns[0]
    })
  },
  CLEAR_DATAPOINTS: (state, action) => {
    return Object.assign({}, state, {
      datapoints: {meta: null, raw: null, flattened: null},
      dataParamsChanged: false
    })
  },
  GET_DATAPOINTS_SUCCESS: (state, action) => {
    return Object.assign({}, state, {
      datapoints: {
        meta: action.payload.data.meta,
        raw: action.payload.data.objects,
        flattened: action.payload.data.objects
      },
      dataParamsChanged: false
    })
  },
  UPDATE_DATAPOINT_FAILURE: (state, action) => {
    return Object.assign({}, state, {
      dataParamsChanged: true
    })
  },
  SELECT_GLOBAL_CAMPAIGN: (state, action) => {
    return Object.assign({}, state, {
      selected_campaign: action.payload,
      dataParamsChanged: true
    })
  },
  SELECT_GLOBAL_LOCATION: (state, action) => {
    return Object.assign({}, state, {
      selected_locations: [...state.selected_locations, action.payload],
      dataParamsChanged: true
    })
  },
  SELECT_GLOBAL_LOCATION_DEPTH: (state, action) => {
    return Object.assign({}, state, {
      location_depth: action.payload
    })
  },
  SET_GLOBAL_LOCATIONS: (state, action) => {
    return Object.assign({}, state, {
      selected_locations: _.isArray(action.payload) ? action.payload : [action.payload],
      dataParamsChanged: true
    })
  },
  SET_GLOBAL_INDICATORS: (state, action) => {
    return Object.assign({}, state, {
      selected_indicators: _.isArray(action.payload) ? action.payload : [action.payload],
      dataParamsChanged: true
    })
  },
  SET_GLOBAL_INDICATOR_TAG: (state, action) => {
    return Object.assign({}, state, {
      selected_indicator_tag: action.payload
    })
  },
  SET_GLOBAL_INDICATOR_FILTER: (state, action) => {
    return Object.assign({}, state, {
      indicator_filter: action.payload,
      dataParamsChanged: true
    })
  }
}, data)

export default data_entry
