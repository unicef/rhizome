import { connect } from 'react-redux'
import CampaignDetail from 'components/organisms/campaigns/CampaignDetail'

const mapStateToProps = (state, ownProps) => {
	return {
		campaign: state.campaigns.raw ? state.campaigns.index[ownProps.campaign_id] : []
	}
}

const CampaignDetailContainer = connect(mapStateToProps)(CampaignDetail)

export default CampaignDetailContainer
