import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import DashboardTable from 'components/organisms/dashboards/DashboardTable'
import { getAllDashboards } from 'actions/dashboard_actions'

const mapStateToProps = (state) => ({ dashboards: state.dashboards })

const mapDispatchToProps = (dispatch) => bindActionCreators({getAllDashboards}, dispatch)

const DashboardTableContainer = connect(mapStateToProps, mapDispatchToProps)(DashboardTable)

export default DashboardTableContainer
