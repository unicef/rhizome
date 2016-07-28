import moment from 'moment'
import format from 'utilities/format'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import SourceDataPage from 'components/pages/SourceDataPage'
import { getAllSourceDocs } from 'actions/source_data_actions'

const mapStateToProps = state => {
  return {
    campaigns: state.campaigns,
    indicators: state.indicators,
    locations: state.locations,
    source_docs: state.source_docs
  }
}

const mapDispatchToProps = dispatch => bindActionCreators({
  getAllSourceDocs
}, dispatch)

const SourceDataPageContainer = connect(mapStateToProps, mapDispatchToProps)(SourceDataPage)

export default SourceDataPageContainer
