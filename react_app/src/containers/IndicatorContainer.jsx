import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import IndicatorDetail from 'components/organisms/indicators/IndicatorDetail'
import { updateIndicator } from 'actions/indicator_actions'

const mapStateToProps = (state, ownProps) => {
	return {
		indicator: state.indicators.raw ? state.indicators.index[ownProps.params.indicator_id] : [],
		real_indicator: state.indicator,
		indicators: state.indicators
	}
}

const mapDispatchToProps = dispatch => bindActionCreators({	updateIndicator }, dispatch)

const IndicatorContainer = connect(mapStateToProps, mapDispatchToProps)(IndicatorDetail)

export default IndicatorContainer
