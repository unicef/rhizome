import moment from 'moment'
import _ from 'lodash'
import { handleActions } from 'redux-actions'

const data = {
  start_date: moment().format('YYYY-MM-DD'),
  end_date: moment().format('YYYY-MM-DD'),
  entry_type: 'date',
  selected_campaign: null,
  selected_locations: [],
  selected_indicators: [],
  selected_indicator_tag: null,
  datapoints: {meta: null, raw: null, flattened: null},
  dataParamsChanged: false
}

const data_entry = handleActions({
  SET_DATA_ENTRY_DATE_RANGE: (state, action) => {
    return Object.assign({}, state, {
      start_date: action.payload.start,
      end_date: action.payload.end
    })
  },
  TOGGLE_DATA_ENTRY_TYPE: (state, action) => {
    return Object.assign({}, state, {
      entry_type: state.entry_type === 'campaign' ? 'date' : 'campaign'
    })
  },
  GET_INITIAL_DATA_SUCCESS: (state, action) => {
    return Object.assign({}, state, {
      selected_campaign: action.payload.data.objects[0].campaigns[0]
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
  }
}, data)

export default data_entry
