import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import CampaignTable from 'components/organisms/campaigns/CampaignTable'
import { getAllCampaigns } from 'actions/campaign_actions'

const mapStateToProps = (state) => ({ campaigns: state.campaigns })

const mapDispatchToProps = (dispatch) => {
	return bindActionCreators({ getAllCampaigns }, dispatch)
}

const CampaignTableContainer = connect(mapStateToProps, mapDispatchToProps)(CampaignTable)

export default CampaignTableContainer
