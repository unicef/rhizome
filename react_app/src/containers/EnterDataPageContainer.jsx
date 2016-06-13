import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'
import { selectGlobalCampaign, selectGlobalLocation, setGlobalIndicators, setGlobalIndicatorTag } from 'actions/global_actions'
import { toggleEntryType, setDataEntryDate } from 'actions/data_entry_actions'
import { getDatapoints } from 'actions/datapoint_actions'

const mapStateToProps = state => ({
	campaigns: state.campaigns,
	indicators: state.indicators,
	locations: state.locations,
  date: state.data_entry.date,
  entry_type: state.data_entry.entry_type,
	dataParamsChanged: state.data_entry.dataParamsChanged,
	selected_campaign: state.data_entry.selected_campaign,
	selected_locations: state.data_entry.selected_locations,
	selected_indicators: state.data_entry.selected_indicators,
	selected_indicator_tag: state.data_entry.selected_indicator_tag,
	datapoints: {
		raw: state.data_entry.datapoints.raw,
		flattened: _flatten(state.data_entry.datapoints.raw, state.indicators, state.locations, state.campaigns)
	}
})

const mapDispatchToProps = (dispatch) => bindActionCreators({
  setDataEntryDate,
  toggleEntryType,
	selectGlobalCampaign,
	selectGlobalLocation,
	setGlobalIndicators,
	setGlobalIndicatorTag,
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
      id: d.computed_id,
      value: d.value ? _formatValue(d.value, indicator.data_format) : null,
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

const _formatValue = (value, data_format) => {
  if (data_format === 'int' || data_format === 'pct') {
    return value === 0.0 || value === '0.0' ? 0 : parseFloat(value)
  } else if (data_format === 'date') {
    return moment(value, 'YYYY-MM-DD').toDate()
  } else {
    return value
  }
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
