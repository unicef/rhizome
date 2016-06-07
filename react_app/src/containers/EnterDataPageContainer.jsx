import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import EnterDataPage from 'components/pages/EnterDataPage'

import { fetchAllMeta } from 'actions/meta_actions'

const mapStateToProps = (state) => ({
	campaigns: state.campaigns,
	indicators: state.indicators,
	locations: state.locations
})

const mapDispatchToProps = (dispatch) => bindActionCreators({fetchAllMeta}, dispatch)

const EnterDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(EnterDataPage)

export default EnterDataPageContainer
