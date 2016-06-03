import { connect } from 'react-redux'
import IndicatorDetail from 'components/organisms/indicators/IndicatorDetail'

const mapStateToProps = (state, ownProps) => {
	return { indicator: state.indicators[ownProps.indicator_id] }
}

const IndicatorDetailContainer = connect(mapStateToProps)(IndicatorDetail)

export default IndicatorDetailContainer
