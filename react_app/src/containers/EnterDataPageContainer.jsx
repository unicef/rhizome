import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'
import { selectGlobalCampaign, selectGlobalLocation, setGlobalIndicators, setGlobalIndicatorTag } from 'actions/global_actions'

const mapStateToProps = (state) => ({
	campaigns: state.campaigns,
	indicators: state.indicators,
	locations: state.locations,
	selected_campaign: state.selected_campaign,
	selected_locations: state.selected_locations,
	selected_indicators: state.selected_indicators,
	selected_indicator_tag: state.selected_indicator_tag
})

const mapDispatchToProps = (dispatch) => bindActionCreators({
	selectGlobalCampaign, selectGlobalLocation, setGlobalIndicators, setGlobalIndicatorTag
}, dispatch)

const EnterDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(EnterDataPage)

export default EnterDataPageContainer
