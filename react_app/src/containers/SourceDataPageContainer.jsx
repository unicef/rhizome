import moment from 'moment'
import format from 'utilities/format'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import SourceDataPage from 'components/pages/SourceDataPage'
import { selectGlobalCampaign, selectGlobalLocation } from 'actions/global_actions'

const mapStateToProps = state => {
  return {
    campaigns: state.campaigns,
    indicators: state.indicators,
    locations: state.locations,
  }
}

const mapDispatchToProps = (dispatch) => bindActionCreators({
  // selectGlobalCampaign,
  // selectGlobalLocation
}, dispatch)

const SourceDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(SourceDataPage)

export default SourceDataPageContainer
