import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import BasePage from 'components/pages/BasePage'

import { fetchAllMeta } from 'actions/meta_actions'

const mapDispatchToProps = (dispatch) => bindActionCreators({fetchAllMeta}, dispatch)

const BasePageContainer = connect(null, mapDispatchToProps)(BasePage)

export default BasePageContainer
