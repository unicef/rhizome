import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'
import { selectGlobalCampaign, selectGlobalLocation } from 'actions/global_actions'

const mapStateToProps = (state) => ({
	campaigns: state.campaigns,
	indicators: state.indicators,
	locations: state.locations,
	selected_campaign: state.selected_campaign,
	selected_location: state.selected_location
})

const mapDispatchToProps = (dispatch) => bindActionCreators({
	selectGlobalCampaign, selectGlobalLocation
}, dispatch)

const EnterDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(EnterDataPage)

export default EnterDataPageContainer
