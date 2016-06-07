import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'
import { selectGlobalCampaign } from 'actions/global_actions'

const mapStateToProps = (state) => ({
	campaigns: state.campaigns,
	indicators: state.indicators,
	locations: state.locations,
	selected_campaign: state.selected_campaign
})

const mapDispatchToProps = (dispatch) => bindActionCreators({selectGlobalCampaign}, dispatch)

const EnterDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(EnterDataPage)

export default EnterDataPageContainer
