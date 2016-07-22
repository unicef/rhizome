import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import CampaignDetail from 'components/organisms/campaigns/CampaignDetail'
import { updateCampaign, getAllCampaignTypes } from 'actions/campaign_actions'

const mapStateToProps = (state, ownProps) => {
	return {
		campaign: state.campaigns.raw ? state.campaigns.index[ownProps.params.campaign_id] : [],
		campaign_types: state.campaign_types,
		indicators: state.indicators,
		locations: state.locations
	}
}

const mapDispatchToProps = (dispatch) => bindActionCreators({
	getAllCampaignTypes,
	updateCampaign
}, dispatch)

const CampaignContainer = connect(mapStateToProps, mapDispatchToProps)(CampaignDetail)

export default CampaignContainer
