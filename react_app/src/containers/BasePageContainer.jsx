import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import BasePage from 'components/pages/BasePage'
import { getInitialData } from 'actions/global_actions'

const mapStateToProps = (state) => ({
	superuser: state.superuser,
	dashboards: state.dashboards,
	charts: state.charts
})

const mapDispatchToProps = (dispatch) => bindActionCreators({getInitialData}, dispatch)

const BasePageContainer = connect(mapStateToProps, mapDispatchToProps)(BasePage)

export default BasePageContainer
