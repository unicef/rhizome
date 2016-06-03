import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import ChartTable from 'components/organisms/charts/ChartTable'
import { fetchCharts } from 'actions/chart_actions'

const mapStateToProps = (state) => ({ charts: state.charts })

const mapDispatchToProps = (dispatch) => bindActionCreators({fetchCharts}, dispatch)

const ChartTableContainer = connect(mapStateToProps, mapDispatchToProps)(ChartTable)

export default ChartTableContainer
