import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import IndicatorTable from 'components/organisms/indicators/IndicatorTable'
import { getAllIndicators } from 'actions/indicator_actions'

const mapStateToProps = (state) => ({ indicators: state.indicators })

const mapDispatchToProps = (dispatch) => bindActionCreators({getAllIndicators}, dispatch)

const IndicatorTableContainer = connect(mapStateToProps, mapDispatchToProps)(IndicatorTable)

export default IndicatorTableContainer
