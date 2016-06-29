import moment from 'moment'
import format from 'utilities/format'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import DataEntryPage from 'components/pages/DataEntryPage'
import { selectGlobalCampaign, selectGlobalLocation, setGlobalLocations, setGlobalIndicators, setGlobalIndicatorFilter, setGlobalIndicatorTag, setGlobalLocationDepth } from 'actions/global_actions'
import { toggleEntryType, setDataEntryStartDate, setDataEntryEndDate } from 'actions/data_entry_actions'
import { getDatapoints, updateDatapoint, removeDatapoint } from 'actions/datapoint_actions'

const mapStateToProps = state => {
  const datapoints = {
    raw: state.data_entry.datapoints.raw,
    flattened: _flatten(state.data_entry.datapoints.raw, state.indicators, state.locations, state.campaigns)
  }
  if (state.data_entry.data_type === 'campaign') {
    datapoints.including_missing =  fillMissingDatapoints(state.data_entry.datapoints, state.indicators, state.locations, state.campaigns)
  }
  return {
    datapoints: datapoints,
    campaigns: state.campaigns,
    indicators: state.indicators,
    locations: state.locations,
    location_depth: state.data_entry.location_depth,
    indicator_filter: state.data_entry.indicator_filter,
    start_date: state.data_entry.start_date,
    end_date: state.data_entry.end_date,
    data_type: state.data_entry.data_type,
    dataParamsChanged: state.data_entry.dataParamsChanged,
    selected_campaign: state.data_entry.selected_campaign,
    selected_locations: state.data_entry.selected_locations,
    selected_indicators: state.data_entry.selected_indicators,
    selected_indicator_tag: state.data_entry.selected_indicator_tag
  }
}

const mapDispatchToProps = (dispatch) => bindActionCreators({
  setDataEntryStartDate,
  setDataEntryEndDate,
  toggleEntryType,
  selectGlobalCampaign,
  selectGlobalLocation,
  setGlobalLocations,
  setGlobalLocationDepth,
  setGlobalIndicators,
  setGlobalIndicatorTag,
  setGlobalIndicatorFilter,
  removeDatapoint,
  updateDatapoint,
	getDatapoints
}, dispatch)

const DataEntryPageContainer = connect(mapStateToProps, mapDispatchToProps)(DataEntryPage)

// =========================================================================== //
//                             DATAPOINT UTILITIES                             //
// =========================================================================== //

const fillMissingDatapoints = (datapoints, indicators, locations, campaigns) => {
  if (!datapoints.raw)
    return null
  const selected_locations = datapoints.meta.location_ids.map(id => locations.index[id])
  const selected_indicators = datapoints.meta.indicator_ids.map(id => indicators.index[id])
  const indexDatapoints = _.keyBy(datapoints.location_id)
  const missing_datapoints = []

  selected_locations.forEach(location => {
    selected_indicators.forEach(indicator => {
      const datapointExists = datapoints.raw.filter(datapoint => {
        return datapoint.location_id === location.id && datapoint.indicator_id === indicator.id
      }).length <= 0
      if (datapointExists) {
        const placeholder_datapoint = {
          campaign_id: parseInt(datapoints.meta.campaign_ids[0]),
          value: null,
          location_id: location.id,
          indicator_id: indicator.id
        }
        missing_datapoints.push(placeholder_datapoint)
      }
    })
  })
  const all_datapoints = missing_datapoints.concat(datapoints.raw)
  return _flatten(all_datapoints, indicators, locations, campaigns)
}


const _flatten = (datapoints, indicators, locations, campaigns) => {
  if (!datapoints)
    return null
  const flattened = datapoints.map(d => {
    const indicator = indicators.index[d.indicator_id]
    const datapoint = {
      id: d.id,
      value: d.value,
      display_value: format.autoFormat(d.value, indicator.data_format),
      location: locations.index[d.location_id],
      indicator: indicator
    }
    if (d.data_date) { datapoint.data_date = d.data_date }
    if (d.campaign_id) {
      datapoint.campaign = campaigns.index[d.campaign_id] || _createYearCampaign(d.campaign_id)
    }
    return datapoint
  })
  return flattened
}

const _createYearCampaign = (year) => {
  return {
    id: year,
    name: year,
    start_date: moment(year + '-01-01', 'YYYY-MM-DD').toDate(),
    end_date: moment(year + '-12-31', 'YYYY-MM-DD').toDate()
  }
}

export default DataEntryPageContainer
