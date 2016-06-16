import moment from 'moment'
import format from 'utilities/format'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'
import { selectGlobalCampaign, selectGlobalLocation, setGlobalIndicators, setGlobalIndicatorTag } from 'actions/global_actions'
import { toggleEntryType, setDataEntryStartDate, setDataEntryEndDate } from 'actions/data_entry_actions'
import { getDatapoints, updateDatapoint } from 'actions/datapoint_actions'

const mapStateToProps = state => {
  const datapoints = {
    raw: state.data_entry.datapoints.raw,
    flattened: _flatten(state.data_entry.datapoints.raw, state.indicators, state.locations, state.campaigns)
  }
  return {
    datapoints: datapoints,
    campaigns: state.campaigns,
    indicators: state.indicators,
    locations: state.locations,
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
  setGlobalIndicators,
  setGlobalIndicatorTag,
  updateDatapoint,
	getDatapoints
}, dispatch)

const EnterDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(EnterDataPage)

// =========================================================================== //
//                             DATAPOINT UTILITIES                             //
// =========================================================================== //

const _flatten = (datapoints, indicators, locations, campaigns) => {
	if (!datapoints)
		return null
  const flattened = datapoints.map(d => {
    const indicator = indicators.index[d.indicator_id]
    const datapoint = {
      id: d.id,
      value: format.autoFormat(d.value, indicator.data_format),
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

export default EnterDataPageContainer
