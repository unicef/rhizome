import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'

const mapStateToProps = (state) => ({
	campaigns: state.campaigns,
	indicators: state.indicators,
	locations: state.locations,
	selected_campaign: state.selected_campaign
})

const EnterDataPageContainer = connect(mapStateToProps)(EnterDataPage)

export default EnterDataPageContainer
