import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import MultiChart from 'components/organisms/charts/MultiChart'

const mapStateToProps = (state, ownProps) => {
	return { chart: state.charts[ownProps.chart_id] }
}

const MultiChartContainer = connect(mapStateToProps)(MultiChart)

export default MultiChartContainer
